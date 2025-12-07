# messaging/managers.py
from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Manager para mensagens não-lidas.
    Uso: Message.unread.unread_for_user(user)
    """
    def get_queryset(self):
        return super().get_queryset()

    def unread_for_user(self, user):
        """
        Devolve queryset com mensagens não-lidas para o utilizador `user`.
        Devolve apenas campos essenciais via .only() para optimização.
        """
        return (self.get_queryset()
                    .filter(receiver=user, read=False)
                    .only('id', 'sender_id', 'receiver_id', 'content', 'timestamp', 'parent_message_id', 'thread_root_id')
                    .select_related('sender', 'receiver'))
