# Django-Middleware-0x03/chats/middleware.py

from datetime import datetime
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import os

class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware simples que regista cada request num ficheiro.
    Regista: timestamp, utilizador (ou 'Anonymous') e request.path
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        # caminho para o ficheiro de logs — usa BASE_DIR se disponível
        base_dir = getattr(settings, "BASE_DIR", None)
        if base_dir is not None:
            self.logfile = os.path.join(str(base_dir), "requests.log")
        else:
            # fallback: ficheiro na pasta actual
            self.logfile = "requests.log"

        # garante que o ficheiro existe
        try:
            open(self.logfile, "a").close()
        except Exception:
            # se não for possível criar, usa um fallback em /tmp
            self.logfile = "/tmp/requests.log"
            open(self.logfile, "a").close()

    def __call__(self, request):
        # executa antes da view
        user = getattr(request, "user", None)
        if user is not None and user.is_authenticated:
            user_repr = f"{user.username} (id:{getattr(user, 'id', 'N/A')})"
        else:
            user_repr = "Anonymous"

        timestamp = datetime.now().isoformat(sep=" ", timespec="seconds")
        line = f"{timestamp} - User: {user_repr} - Path: {request.path}\n"

        # escreve no ficheiro (append)
        try:
            with open(self.logfile, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception:
            # não falhar o request só por logging — silenciosamente ignorar erro de I/O
            pass

        # prosseguir com o fluxo normal
        response = self.get_response(request)

        # (Opcional) poderias também registar a response.status_code aqui
        # Exemplo: escrever status
        # try:
        #     with open(self.logfile, "a", encoding="utf-8") as f:
        #         f.write(f"{timestamp} - Response status: {response.status_code}\n")
        # except Exception:
        #     pass

        return response
