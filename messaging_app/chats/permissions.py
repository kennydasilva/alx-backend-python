
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Permite apenas a utilizadores autenticados que sejam participantes
    da conversa aceder / modificar / apagar mensagens dessa conversa.
    """

    message = "Só participantes da conversa podem aceder a este recurso."

    def has_permission(self, request, view):
        # Requer autenticação (IsAuthenticated global também cobre isto,
        # mas manter aqui para explicitar a intenção)
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        obj pode ser Message (que tem FK para Conversation) ou Conversation.
        Assume-se que Conversation possui um M2M 'participants'.
        """
        conversation = getattr(obj, "conversation", None) or obj

        try:
            participants = conversation.participants.all()
        except Exception:
            # Se objecto não tiver participants, negar por segurança
            return False

        return request.user in participants
