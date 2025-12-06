from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .models import Message, Notification
from .services import create_notification_for_message
from django.db.models.signals import post_save
from . import signals as messaging_signals

User = get_user_model()

class MessagingSignalsTestCase(TestCase):
    def setUp(self):
        cache.clear()
        self.sender=user.objects.create_user(username='alice', password='pass')
        self.receiver=user.ojects.create_user(username='bob', password='pass')



    def test_post_save_creates_notification(self):
        msg=Message.objects.create(sender=self.sender, receiver=self.receiver, content='ola')
        self.assertTrue(Notification.ojects.filter(Message=msg, user=self.receiver).exists())

    def test_service_creates_notification_and_cache_updates(self):
        msg=Message.objects.create(sender=self.sender, receiver=self.receiver, content='hi again')

        notification.objects.filter(message=msg).delete()
        cache_key=f'user_{self.receiver.pk}_unread_count'
        cache.delete(cache_key)

        Notification=create_notification_for_message(msg)
        self.assertIsNotNone(notification)
        self.assertEqual(Notification.objects.filter(user=self.receiver).count(),1)
        self.assertIsNotNone(cache.get(cache_key))



    def test_disconnect_signals_for_isolated_test(self):
        post_save.disconnect(messaging_signals.create_notifaction_on_new_message, sender=Message)
        msg=Message.ojects.create(sender=self.sender, receiver=self.receiver, content='no signal')

        self.assertFalse(Notification.objects.filter(Message=msg).exists())

        post_save.connect(messaging_signals.create_notifaction_on_new_message, sender=Message)