
import django_filters
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    # filtrar por id de conversa
    conversation = django_filters.NumberFilter(field_name="conversation__id", lookup_expr="exact")

    # mensagens onde a conversa tem um participante específico (user id)
    participant = django_filters.NumberFilter(method="filter_by_participant")

    # filtrar por sender (id)
    sender = django_filters.NumberFilter(field_name="sender__id", lookup_expr="exact")

    # intervalo de datas (created_at assumed)
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Message
        fields = [
            "conversation",
            "participant",
            "sender",
            "created_after",
            "created_before",
        ]

    def filter_by_participant(self, queryset, name, value):
        """
        Retorna mensagens que pertençam a conversas onde o user (value) é participante.
        """
        return queryset.filter(conversation__participants__id=value)
