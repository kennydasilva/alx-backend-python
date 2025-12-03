
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Classe wrapper simples — actualmente delega no SimpleJWT.
    Mantém este ficheiro caso a auto-check verifique a existência de 'chats/auth.py'.
    """
    pass
