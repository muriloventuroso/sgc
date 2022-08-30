from django.contrib.auth.hashers import check_password
from users.models import User


class UsernameAuthBackend(object):
    def authenticate(self, request, username=None, password=None, domain=None):
        try:
            user = User.objects.select_related(
                'congregation').get(email=username)
            if check_password(password, user.password):
                return user
            else:
                return None
        except User.DoesNotExist as e:
            # No user was found, return None - triggers default login failed
            return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
