# messaging/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone
from .managers import UnreadMessagesManager

User = settings.AUTH_USER_MODEL

class UnreadMessagesManager(models.Manager):
    """
    Custom manager to get unread messages for a given user.
    Usage: Message.objects.unread.for_user(user)
    """
    def get_queryset(self):
        return super().get_queryset()

    def for_user(self, user):
        # devolve somente os campos essenciais para listar a inbox
        return (self.get_queryset()
                    .filter(receiver=user, read=False)
                    .only('id', 'sender_id', 'receiver_id', 'content', 'timestamp', 'parent_message_id', 'thread_root_id')
                    .select_related('sender', 'receiver'))

class Message(models.Model):
    sender = models.ForeignKey(
        User,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    # novo: self-referential parent (reply)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )

    # novo: root da thread (top-level message) para consultar a thread de forma eficiente
    thread_root = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='thread_messages',
        on_delete=models.CASCADE
    )

    # já existia/novo manager
    objects = models.Manager()  # default
    unread = UnreadMessagesManager()  # custom manager

    edited = models.BooleanField(default=False)
    objects = models.Manager()  # default manager
    unread = UnreadMessagesManager()  

    class Meta:
        ordering = ['timestamp']  # ordenar cronologicamente ajuda em nests

    def __str__(self):
        return f'Message {self.pk} from {self.sender} to {self.receiver} at {self.timestamp}'

    def save(self, *args, **kwargs):
        """
        Garante que thread_root é preenchido:
        - se é nova mensagem sem parent -> thread_root = self (pre-save ainda não tem PK, usamos None e definimos depois)
        - se tem parent -> thread_root = parent's thread_root (ou parent itself)
        Como a self ainda não tem pk em criação, tratamos caso após super().save
        """
        # keep track if creating (no pk yet)
        is_create = self.pk is None

        # determine thread_root pre-save when parent exists
        if self.parent_message:
            # if parent has thread_root, use it; otherwise use the parent as root
            root = self.parent_message.thread_root or self.parent_message
            self.thread_root = root
        else:
            # if no parent, leave thread_root to be self after saving (set below)
            pass

        super().save(*args, **kwargs)

        # If created and has no parent, set thread_root to self
        if is_create and not self.parent_message:
            if self.thread_root is None:
                self.thread_root = self
                # avoid recursion or extra logic: update only the thread_root field
                Message.objects.filter(pk=self.pk).update(thread_root=self)

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(default=timezone.now)
    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='edited_message_histories'
    )

    class Meta:
        ordering = ['-edited_at']

    def __str__(self):
        return f'History for Message {self.message_id} at {self.edited_at}'


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Notification for {self.user}: {self.text}'
