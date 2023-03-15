from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.account.api.serializer import UserSerializer
from apps.account.utils import get_tokens_for_user


@api_view(["POST"])
def register_view(request):
    """
    Endpoint: /api/account/register/
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = get_tokens_for_user(user)
        response_data = {"token": token, "message": "Successfully registered user."}
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def logout_view(request):
    """
    Endpoint: /api/account/logout/
    """
    request.user.auth_token.delete()
    return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)
