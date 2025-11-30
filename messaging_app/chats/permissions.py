#
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Permite acesso apenas a utilizadores autenticados que sejam participantes
    da conversa. Funciona em object-level (has_object_permission).
    """

    message = "Só participantes da conversa podem aceder a este recurso."

    def has_permission(self, request, view):
        # exige autenticação básica; IsAuthenticated global já está activo,
        # mas devolvemos False se não autenticado.
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """
        obj pode ser um Message (com atributo conversation) ou uma Conversation.
        Assume-se que Conversation tem um m2m 'participants'.
        """
        # se for Message, obter conversation; caso contrário tratar obj como conversation
        conversation = getattr(obj, 'conversation', None) or obj

        # tenta obter o queryset de participants; em caso de erro, negar por segurança
        try:
            participants = conversation.participants.all()
        except Exception:
            return False

        return request.user in participants
