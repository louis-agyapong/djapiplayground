from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.account.api import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", obtain_auth_token, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
