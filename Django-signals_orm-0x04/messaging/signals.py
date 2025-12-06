from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification
from .services import create_notification_for_message, invalidate_unread_cache

@receiver(post_save, sender=Message)
def create_notifaction_on_new_message(sender, instance:Message, created, **kwargs):
    """
    Handler to create a notification when a new message is created.
    Keeping a low handler: delegate a logic ao 
    """

    if created:
        # don't execute a long tasks 
        create_notification_for_message(instance)

@receiver(post_delete, sender=Notification)
def cleanup_notifications_on_message_delete(sender, instance: Message, **kwargs):
    """
    if the message being deleted, delete the notifications related.
    """ 
    Notification.objects.filter(message=instance).delete()
    invalidate_unread_cache(instance.receiver.id)