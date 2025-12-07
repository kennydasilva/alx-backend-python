# messaging/apps.py
from django.apps import AppConfig


class MessagingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "messaging"

    def ready(self):
        # Importa signals para ligar handlers de Message (pre_save/post_save/post_delete)
        from . import signals  # noqa: F401

        # Ligar explicitamente o post_delete do User ao handler definido em signals
        # chamando a função helper que faz a conexão dinâmica.
        try:
            signals.connect_user_post_delete_signal()
        except Exception:
            # não falhar a subida do app caso haja algum problema aqui
            pass
