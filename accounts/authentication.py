from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailOrUsernameBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(email=username)  # try email
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(username=username)  # fallback to username
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password) and user.is_active:
            return user
        return None
