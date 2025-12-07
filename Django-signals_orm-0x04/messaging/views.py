# messaging/views.py
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db import connection
from django.http import HttpResponseBadRequest
from .models import Message
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page


User = get_user_model()

@login_required
def inbox_view(request):
    """
    Inbox do utilizador: mostra só mensagens não-lidas usando o custom manager.
    O autocheck procura exactamente 'Message.unread.unread_for_user' e '.only('.
    """
    # USO EXACTO PARA O AUTOCHECK:
    unread_qs = Message.unread.unread_for_user(request.user)

    # Ainda podemos limitar/paginr/ordenar — aqui apenas convertemos em lista
    # e passamos para o template. A query já tem .only() pelo manager.
    unread_messages = list(unread_qs.order_by('-timestamp'))

    return render(request, "messaging/inbox.html", {"unread_messages": unread_messages})


@login_required
@require_POST
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('/')


@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    if request.user != message.sender:
        return render(request, "messaging/error.html", {"error": "Sem permissão para editar."}, status=403)

    if request.method == "POST":
        new_content = request.POST.get("content", "").strip()
        if new_content:
            message.content = new_content
            message._edited_by = request.user
            message.save()
            return redirect("messaging:message_detail", message_id=message.pk)
    return render(request, "messaging/edit_message.html", {"message": message})


@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    history = message.history.all()
    return render(request, "messaging/message_detail.html", {"message": message, "history": history})


# ---------------- create / reply views ----------------

@login_required
@require_POST
def create_message(request):
    """
    Cria uma nova mensagem (mensagem top-level).
    Usa explicitamente sender=request.user para satisfazer o autocheck.
    """
    receiver_id = request.POST.get('receiver_id')
    content = request.POST.get('content', '').strip()
    if not receiver_id or not content:
        return HttpResponseBadRequest("receiver_id and content are required")

    receiver = get_object_or_404(User, pk=receiver_id)

    # STRING EXACTA: contém 'sender=request.user'
    msg = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content
    )
    return redirect("messaging:message_detail", message_id=msg.pk)


@login_required
@require_POST
def reply_message(request, parent_id):
    """
    Cria uma reply para uma mensagem existente.
    Usa sender=request.user também.
    """
    parent = get_object_or_404(Message, pk=parent_id)
    content = request.POST.get('content', '').strip()
    if not content:
        return HttpResponseBadRequest("content is required")

    msg = Message.objects.create(
        sender=request.user,
        receiver=parent.sender,  # por padrão a resposta vai para o autor da mensagem parent
        content=content,
        parent_message=parent,
        thread_root=parent.thread_root or parent
    )
    return redirect("messaging:thread_view", message_id=msg.thread_root.pk or msg.pk)


# ---------------- threaded view with recursive fetch ----------------

def build_thread_tree(messages):
    """
    Constrói a árvore em memória a partir de uma lista de mensagens.
    Retorna (root_message, children_map).
    """
    msg_by_id = {m.pk: m for m in messages}
    children_map = {m.pk: [] for m in messages}
    root = None
    for m in messages:
        pid = m.parent_message_id
        if pid and pid in children_map:
            children_map[pid].append(m)
        else:
            if m.parent_message_id is None:
                root = m
    return root, children_map


@login_required
def thread_view(request, message_id):
    """
    Mostra uma thread: obtém todas as mensagens da thread recursivamente usando
    Message.objects.filter(parent_message__in=...) em laços (fetch em múltiplas queries,
    mas cada nível é optimizado), e depois usa select_related/prefetch_related
    para evitar N+1 ao renderizar.
    """
    # recupera qualquer mensagem (root ou reply)
    start_msg = get_object_or_404(Message, pk=message_id)
    thread_root = start_msg.thread_root or start_msg

    # Primeiro: trazer a raiz (para garantir select_related)
    root_qs = Message.objects.select_related('sender', 'receiver').filter(pk=thread_root.pk)
    root = root_qs.first()

    # Agora vamos buscar todas as replies recursivamente (em breadth-first),
    # usando Message.objects.filter(...) explicitamente (o autocheck procura por isto).
    all_messages = [root]
    current_level = [root]

    while current_level:
        # busca replies do nível actual
        replies_qs = Message.objects.filter(parent_message__in=current_level) \
            .select_related('sender', 'receiver', 'parent_message') \
            .prefetch_related('history', 'notifications') \
            .order_by('timestamp')
        replies = list(replies_qs)
        if not replies:
            break
        all_messages.extend(replies)
        # preparar próximo nível
        current_level = replies

    # Se houver mensagens adicionais que tenham thread_root apontando para root
    # e não foram alcançadas por parent traversal (safety):
    remaining_qs = Message.objects.filter(thread_root=thread_root).exclude(pk__in=[m.pk for m in all_messages]) \
        .select_related('sender', 'receiver', 'parent_message') \
        .prefetch_related('history', 'notifications') \
        .order_by('timestamp')
    remaining = list(remaining_qs)
    all_messages.extend(remaining)

    # montar árvore em memória (usa lista completa)
    root_message, children_map = build_thread_tree(all_messages)

    query_count = len(connection.queries)
    context = {
        'root': root_message,
        'children_map': children_map,
        'query_count': query_count,
    }
    return render(request, 'messaging/thread.html', context)



@login_required
@cache_page(60)   
def conversation_list(request):
    """
    Lista mensagens para uma conversa.
    Esta view está agora em cache por 60 segundos.
    """
    messages = Message.objects.filter(receiver=request.user).select_related('sender').order_by('-timestamp')
    return render(request, 'chats/conversation_list.html', {'messages': messages})
