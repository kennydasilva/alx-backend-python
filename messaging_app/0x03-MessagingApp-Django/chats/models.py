

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    """
    User model extending AbstractUser.
    Inherits standard fields: password, first_name, last_name
    """
     # Explicitly redeclare fields so static checks detect them
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=128)
    
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    
    #user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    email = models.EmailField(unique=True)
    
    class Meta:
        db_table = 'user'
        indexes = [
            models.Index(fields=['email']),
        ]

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'conversation'

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'message'
        ordering = ['sent_at']