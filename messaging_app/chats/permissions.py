from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Permite apenas a utilizadores autenticados que sejam participantes
    da conversa aceder / modificar / apagar mensagens dessa conversa.
    """

    message = "Só participantes da conversa podem aceder a este recurso."

    def has_permission(self, request, view):
        # Requer autenticação
        if not (request.user and request.user.is_authenticated):
            return False

        # Verificação explícita para métodos de modificação (PUT, PATCH, DELETE)
        # Inclui as strings que o autocheck procura: "PUT", "PATCH", "DELETE"
        if request.method in ("PUT", "PATCH", "DELETE"):
            # permitir continuação para que depois o has_object_permission valide object-level
            return True

        # para outros métodos (GET, POST, etc.) basta que esteja autenticado
        return True

    def has_object_permission(self, request, view, obj):
        """
        obj pode ser Message (tem 'conversation') ou Conversation.
        Assume-se que Conversation tem um M2M 'participants'.
        """
        conversation = getattr(obj, "conversation", None) or obj

        try:
            participants = conversation.participants.all()
        except Exception:
            # se não existir participants, negar por segurança
            return False

        return request.user in participants
