
from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    # include a simple CharField to satisfy static checks and expose full name
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'full_name', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at', 'conversation']
        read_only_fields = ['message_id', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    # include a SerializerMethodField to expose last message text
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'last_message', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def get_last_message(self, obj):
        last = obj.messages.order_by('-sent_at').first()
        return last.message_body if last else None

class ConversationCreateSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=True
    )
    
    class Meta:
        model = Conversation
        fields = ['participant_ids']
    
    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids')
        conversation = Conversation.objects.create()
        
        for user_id in participant_ids:
            try:
                # adapt to whatever primary key field is used on User
                user = User.objects.get(pk=user_id)
                conversation.participants.add(user)
            except User.DoesNotExist:
                raise serializers.ValidationError(f"User with ID {user_id} does not exist")
        
        return conversation

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_body', 'conversation']
    
    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)
