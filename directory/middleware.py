# Middleware to register logs
import logging
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

class ActiveDirectoryLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            User = get_user_model()
            user, created = User.objects.get_or_create(username=request.user.username)
            
            # Atualizar informações do AD no banco local
            user.username = getattr(request.user, 'username', user.username)
            user.first_name = getattr(request.user, 'first_name', user.first_name)
            user.last_name = getattr(request.user, 'last_name', user.last_name)
            user.email = getattr(request.user, 'email', user.email)
            user.department = getattr(request.user, 'department', user.department)
            user.title = getattr(request.user, 'title', user.title)
            user.enabled = getattr(request.user, 'is_active', user.enabled)
            user.save()
            
            logger.info(f"Usuário autenticado: {user.username} - {user.email}")

        return None
