from datetime import datetime, timedelta
from django.http import JsonResponse
import time
from collections import deque, defaultdict
import threading
import json
# --- RolepermissionMiddleware ---
from django.http import HttpResponseForbidden

# --- RestrictAccessByTimeMiddleware ---
class RestrictAccessByTimeMiddleware:
    """
    Blocks access to chat endpoints outside the required time:
    allows only between 18:00 (6PM) and 21:00 (9PM) server time.
    Returns 403 Forbidden outside this interval.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # fixed hours per requirement: open 18 (6PM), close 21 (9PM)
        self.open_hour = 18
        self.close_hour = 21

    def __call__(self, request):
        # apply only to chat endpoints (adjust if needed)
        path = getattr(request, "path", "") or ""
        is_chat_path = "/api/messages" in path or "/api/conversations" in path or path.startswith("/chat")
        if is_chat_path:
            now = datetime.now()
            hour = now.hour
            # allow only if hour in [18, 21)
            if not (self.open_hour <= hour < self.close_hour):
                return JsonResponse(
                    {"detail": "Chat accessible only between 18:00 and 21:00 (server time)."},
                    status=403
                )
        return self.get_response(request)


# --- Rate limit middleware by IP (5 messages per 60 seconds) ---
class RateLimitMiddleware:
    """
    Limits POSTs of messages per IP: 5 messages per 60 seconds.
    In-memory implementation (exercise). Use Redis in production.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.max_messages = 5
        self.window_seconds = 60
        self._lock = threading.Lock()
        self.ip_timestamps = defaultdict(lambda: deque())

    def _get_ip(self, request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "unknown")

    def _clean_old(self, dq, now_ts):
        while dq and (now_ts - dq[0]) > self.window_seconds:
            dq.popleft()

    def __call__(self, request):
        method = request.method.upper()
        path = getattr(request, "path", "") or ""
        is_message_post = method == "POST" and ("/api/messages" in path or "/api/conversations" in path and path.endswith("/messages"))

        if is_message_post:
            ip = self._get_ip(request)
            now_ts = int(time.time())
            with self._lock:
                dq = self.ip_timestamps[ip]
                self._clean_old(dq, now_ts)
                if len(dq) >= self.max_messages:
                    return JsonResponse({"detail": "Rate limit exceeded: 5 messages per 60s."}, status=403)
                dq.append(now_ts)

            # optional: simple offensive language check (comment/use real list if needed)
            # try:
            #     body = request.body.decode('utf-8', errors='ignore')
            #     data = json.loads(body) if body else {}
            #     message_text = data.get('message_body') if isinstance(data, dict) else body
            #     if message_text and 'badword' in message_text.lower():
            #         return JsonResponse({"detail": "Message contains offensive language."}, status=403)
            # except Exception:
            #     pass

        return self.get_response(request)



class RolepermissionMiddleware:
    """
    Allows access only to users with role 'admin' or 'moderator'.
    As a fallback, also allows user.is_staff or user.is_superuser.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        # If the user is not authenticated → deny
        if not user or not getattr(user, "is_authenticated", False):
            return HttpResponseForbidden("Access denied: authentication required")

        # Try to get the 'role' attribute
        role = getattr(user, "role", None)

        # Allow if role is 'admin' or 'moderator'
        if role in ("admin", "moderator"):
            return self.get_response(request)

        # Fallback: allow if is_staff or is_superuser
        if getattr(user, "is_staff", False) or getattr(user, "is_superuser", False):
            return self.get_response(request)

        # Otherwise deny
        return HttpResponseForbidden("Access denied: insufficient permissions")
