# messaging/views.py
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db import connection

from .models import Message

@login_required
@require_POST
def delete_user(request):
    """
    View que permite ao utilizador apagar a sua conta.
    Chama request.user.delete() depois de fazer logout.
    """
    user = request.user
    logout(request)
    user.delete()
    return redirect('/')


@login_required
def edit_message(request, message_id):
    """
    Edita uma mensagem (apenas o sender pode editar).
    Antes de salvar, setamos instance._edited_by para que o signal registre quem editou.
    """
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
    """
    Mostra a mensagem e o seu histórico de edições.
    """
    message = get_object_or_404(Message, pk=message_id)
    history = message.history.all()
    return render(request, "messaging/message_detail.html", {"message": message, "history": history})


# ------------------ Threaded conversation view ------------------

def build_thread_tree(messages):
    """
    Constrói uma árvore de mensagens a partir de uma lista ordenada de mensagens.
    Retorna (root_message, children_map) onde children_map é um dict: parent_id -> [child_msgs].
    """
    # map id -> message
    msg_by_id = {m.pk: m for m in messages}
    children_map = {m.pk: [] for m in messages}

    root = None
    for m in messages:
        parent_id = m.parent_message_id
        if parent_id and parent_id in children_map:
            children_map[parent_id].append(m)
        else:
            # top-level dentro da lista (pode ser root)
            if parent_id is None:
                root = m
    return root, children_map


@login_required
def thread_view(request, message_id):
    """
    Mostra uma thread inteira (todas as mensagens com o mesmo thread_root).
    Faz 1 query para trazer todas as mensagens da thread + joins para sender/receiver.
    """
    # busca a mensagem (pode ser root ou reply)
    message = get_object_or_404(Message, pk=message_id)
    thread_root = message.thread_root or message

    # --- Query otimizada: traz todas as mensagens da thread numa única query ---
    qs = (
        Message.objects
        .filter(thread_root=thread_root)
        .select_related('sender', 'receiver', 'parent_message')
        .prefetch_related('history', 'notifications')
        .order_by('timestamp')  # crescente para montar a thread cronologicamente
    )

    messages = list(qs)  # avalia a queryset (uma só consulta ao BD)

    # Monta a árvore em memória
    root_message, children_map = build_thread_tree(messages)

    # (opcional) DEBUG: número de queries feitas durante esta view (apenas se DEBUG=True)
    query_count = len(connection.queries)

    context = {
        'root': root_message,
        'children_map': children_map,
        'query_count': query_count,
    }
    return render(request, 'messaging/thread.html', context)
