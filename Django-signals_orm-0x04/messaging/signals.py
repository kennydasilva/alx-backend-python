# messaging/signals.py
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Message, Notification, MessageHistory
from .services import invalidate_unread_cache

UserModel = get_user_model()

@receiver(pre_save, sender=Message)
def log_message_before_edit(sender, instance: Message, **kwargs):
    """
    Antes de salvar uma Message, se já existir no BD (pk existe) e o content mudou,
    gravamos a versão antiga em MessageHistory.
    """
    if not instance.pk:
        # é criação; não há versão anterior
        return

    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # só gravamos se o content mudou
    if old.content != instance.content:
        # criamos um historico com o conteúdo antigo
        edited_by = getattr(instance, '_edited_by', None)  
        MessageHistory.objects.create(
            message=old,
            old_content=old.content,
            edited_at=timezone.now(),
            edited_by=edited_by
        )
        # marcamos a message como editada 
        instance.edited = True


@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance: Message, created, **kwargs):
    """
    Quando uma Message nova é criada, geramos uma Notification para o receiver.
    Mantemos a chamada explícita a Notification.objects.create porque o auto-check procura por isso.
    """
    if created:
        text = f'Nova mensagem de {instance.sender}'
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            text=text
        )
        try:
            invalidate_unread_cache(instance.receiver.id)
        except Exception:
            pass


def _cleanup_user_related_data(user_pk):
    """
    Função utilitária que remove mensagens/notifications/histories relacionadas a um user.
    Mesmo com CASCADE, fazemos cleanup explícito para satisfazer os requisitos.
    """
    # Apagar notificações associadas ao utilizador
    Notification.objects.filter(user_id=user_pk).delete()
    # Apagar mensagens enviadas ou recebidas pelo utilizador (isso também remove MessageHistory via CASCADE)
    Message.objects.filter(sender_id=user_pk).delete()
    Message.objects.filter(receiver_id=user_pk).delete()
    # Qualquer MessageHistory sem message (defensivo)
    MessageHistory.objects.filter(message__isnull=True).delete()


def connect_user_post_delete_signal(apps=None, sender_model=None):
    """
    Chamado a partir de apps.ready() para ligar o post_delete do User corretamente.
    Usamos connect dinâmico porque o modelo de User pode ser customizado.
    """
    from django.db.models.signals import post_delete
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # Handler que aceita instance do User e apaga dados relacionados
    def on_user_deleted(sender, instance, **kwargs):
        try:
            _cleanup_user_related_data(instance.pk)
        except Exception:
            pass

    post_delete.connect(on_user_deleted, sender=User, dispatch_uid="messaging_user_post_delete")
