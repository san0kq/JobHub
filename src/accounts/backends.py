from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authentication backend to allow users to authenticate with either their email or username.

    Inherits:
        ModelBackend: Django's default ModelBackend for authentication.

    Methods:
        authenticate(request, username=None, password=None, **kwargs): Method to authenticate users.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate users with either their email or username.

        Args:
            request: The HTTP request object.
            username (str): The username or email address provided by the user.
            password (str): The password provided by the user.
            **kwargs: Additional keyword arguments.

        Returns:
            User: The authenticated user object if authentication is successful, else None.
        """
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                UserModel().set_password(password)
                return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
