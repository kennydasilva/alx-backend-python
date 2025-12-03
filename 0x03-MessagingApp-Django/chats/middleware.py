from datetime import datetime
from django.conf import settings
import os

class RequestLoggingMiddleware:
    """
    Middleware requerido — define __init__ e __call__ e escreve linhas em requests.log
    """

    def __init__(self, get_response):
        self.get_response = get_response
        base_dir = getattr(settings, "BASE_DIR", None)
        if base_dir:
            self.logfile = os.path.join(str(base_dir), "requests.log")
        else:
            self.logfile = os.path.join(os.getcwd(), "requests.log")
        # garante que o ficheiro existe
        try:
            open(self.logfile, "a", encoding="utf-8").close()
        except Exception:
            self.logfile = "/tmp/requests.log"
            open(self.logfile, "a", encoding="utf-8").close()

    def __call__(self, request):
        # Formato pedido exactamente: f"{datetime.now()} - User: {user} - Path: {request.path}"
        user = getattr(request, "user", None)
        if user is not None and getattr(user, "is_authenticated", False):
            user_repr = getattr(user, "username", "User")
        else:
            user_repr = "Anonymous"

        line = f"{datetime.now()} - User: {user_repr} - Path: {request.path}\n"

        try:
            with open(self.logfile, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception:
            pass

        response = self.get_response(request)
        return response
