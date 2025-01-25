from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from ms_active_directory import ADDomain
import logging

logger = logging.getLogger(__name__)

class ActiveDirectoryBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            # Connect to AD using provided credentials
            domain = ADDomain(domain_name=settings.AD_DOMAIN)
            user = domain.authenticate_user(username, password)
            
            if user:
                # Get or create Django user
                django_user, created = User.objects.get_or_create(
                    username=username,
                    defaults={'email': f"{username}@{settings.AD_DOMAIN}"}
                )
                return django_user
            
        except Exception as e:
            logger.error(f"AD Authentication error: {str(e)}")
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None