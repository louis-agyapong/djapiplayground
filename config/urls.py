from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.polls.urls")),
    path("watchlist/", include("apps.watchlist.urls")),
    path("api/", include("apps.watchlist.api.urls")),
    path("api/account/", include("apps.account.api.urls")),
]
