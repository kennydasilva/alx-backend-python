# messaging/urls.py
from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('delete_user/', views.delete_user, name='delete_user'),
]
