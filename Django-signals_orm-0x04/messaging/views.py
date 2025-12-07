# messaging/views.py
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Message

@login_required
@require_POST
def delete_user(request):
    """
    View que permite ao utilizador apagar a sua conta.
    Chama request.user.delete() depois de fazer logout.
    """
    user = request.user
    # opcional: confirmar via form hidden ou senha
    logout(request)
    user.delete()
    # redirecionar para homepage (ajusta conforme teu projecto)
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
            # atribuimos o editor para o pre_save (é lido pelo signal)
            message.content = new_content
            message._edited_by = request.user
            message.save()
            return redirect("messaging:message_detail", message_id=message.pk)
    # GET -> render form de edição
    return render(request, "messaging/edit_message.html", {"message": message})


@login_required
def message_detail(request, message_id):
    """
    Mostra a mensagem e o seu histórico de edições.
    """
    message = get_object_or_404(Message, pk=message_id)
    history = message.history.all()  # MessageHistory via related_name='history'
    return render(request, "messaging/message_detail.html", {"message": message, "history": history})
