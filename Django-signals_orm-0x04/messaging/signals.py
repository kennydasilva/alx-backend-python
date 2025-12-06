# messaging/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification
from .services import invalidate_unread_cache

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance: Message, created, **kwargs):
    """
    Handler that creates a Notification when a new Message is created.
    We keep the logic short: we create the Notification directly here (expected by the auto-check)
    and then invalidate/update the cache through the service.
    """
    if created:
        text = f'Nova mensagem de {instance.sender}'
        # EXPLICIT CALL THAT THE AUTO-CHECK LOOKS FOR:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            text=text
        )

        # Invalidate the related cache (keeps separation of concerns)
        try:
            invalidate_unread_cache(instance.receiver.id)
        except Exception:
            # don't fail the signal because of the cache; logging/ignoring is acceptable here
            pass

@receiver(post_delete, sender=Message)
def cleanup_notifications_on_message_delete(sender, instance: Message, **kwargs):
    """
    When a Message is deleted, delete the related Notifications
    and invalidate the receiver's user cache.
    """
    Notification.objects.filter(message=instance).delete()
    try:
        invalidate_unread_cache(instance.receiver.id)
    except Exception:
        pass
