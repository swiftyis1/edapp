from datetime import timedelta
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Custom Token Authentication class that enforces an expiration policy.
    Tokens expire after 30 days of inactivity/creation.
    """
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        # Expire after 30 days
        if timezone.now() - token.created > timedelta(days=30):
            token.delete()
            raise AuthenticationFailed('Token has expired.')

        return (token.user, token)
