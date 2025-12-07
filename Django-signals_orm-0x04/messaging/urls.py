# messaging/urls.py
from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('message/create/', views.create_message, name='create_message'),
    path('message/<int:parent_id>/reply/', views.reply_message, name='reply_message'),
    path('thread/<int:message_id>/', views.thread_view, name='thread_view'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('conversations/', conversation_list, name='conversation_list'),


]
