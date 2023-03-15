from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed


def get_tokens_for_user(user: AbstractBaseUser) -> dict:
    """
    Generate access and refresh tokens for the given user.
    Args:
        user: A Django user object.
    Returns:
        A dictionary containing the access and refresh tokens.
    """
    try:
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": f"{refresh}",
            "access": f"{refresh.access_token}",
        }
    except Exception as e:
        pass
