from django.core.cache import cache

CACHE_KEY_UNREAD_COUNT ="user_{user_id}_unread_count"

def create_notification_for_message(message):
    """
     the Logic that creates a notification and update related caching.
     Split that allow testing the logic without depending on signal directly
    """
    from .models import Notification
    text=f'New message from {message.sender}'

    notification=Notification.objects.create(
        user=message.receiver,
        message=message,
        text=text
    )

    # Invalidate the unread count cache for the receiver
    key=CACHE_KEY_UNREAD_COUNT.format(user_id=message.receiver.id)

    try:
        cache.incr(key)

    except ValueError:
        cache.set(key,1,timeout=3600)

    return notification


def invalidate_unread_cache(user_id):

    key= CACHE_KEY_UNREAD_COUNT.format(user_id=user_id)

    cache.delete(key)