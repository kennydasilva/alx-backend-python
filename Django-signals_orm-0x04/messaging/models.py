from django.conf import settings
from django.db import models 
from django.utils import timezone

user = settings.Auth_USER_MODEL

class Message(models.Model):
    sender=model.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver =models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content= models.TextField()
    timestamp=models.DateTimeField(default=timezone.now)
    read=models.BooleanField(default=False)


    class Meta:
        ordering=['-timestamp']
    
    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} at {self.timestamp}'
    
class Notification(models.Model):
    user=models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message= models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    text=models.CharField(max_length=255)
    created_at= models.DateTimeField(default=timezone.now)
    is_read=models.BooleanField(default=False)

    class Meta:
        ordering=['-created_at']

    def __str__(self):
        return f'Notification for {self.user}: {self.text}'
    