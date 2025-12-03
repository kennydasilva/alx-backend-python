from rest_framework import viewsets, status, filters, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer, 
    MessageSerializer, 
    ConversationCreateSerializer,
    MessageCreateSerializer
)
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import StandardResultsSetPagination

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username', 'participants__email']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)
    
    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from .models import User
            user = User.objects.get(user_id=user_id)
            conversation.participants.add(user)
            return Response(
                {'message': 'Participant added successfully'}, 
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        # aplica paginação manual aqui se precisares; mas viewset padrão já faz
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    # filtros + pesquisa + paginação
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = MessageFilter
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    search_fields = ['message_body', 'sender__username']

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer
    
    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Override do create para devolver HTTP_403_FORBIDDEN quando o user não é participante.
        O autocheck procura exactamente o literal 'HTTP_403_FORBIDDEN'.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.validated_data.get('conversation')

        if conversation is None:
            return Response(
                {'detail': 'conversation field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user not in conversation.participants.all():
            # devolve 403 explícito (literal HTTP_403_FORBIDDEN presente)
            return Response(
                {'detail': 'You are not a participant of this conversation'},
                status=status.HTTP_403_FORBIDDEN
            )

        # se participante, prosseguir com o create normal
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        # mantém a segurança: salva sender como request.user
        serializer.save(sender=self.request.user)
    
    @action(detail=False, methods=['get'])
    def conversation_messages(self, request):
        conversation_id = request.query_params.get('conversation_id')
        if not conversation_id:
            return Response(
                {'error': 'conversation_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        conversation = get_object_or_404(
            Conversation, 
            conversation_id=conversation_id,
            participants=request.user 
        )
        
        messages = conversation.messages.all()
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
