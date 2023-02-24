from django.urls import path

from apps.watchlist.api import views


urlpatterns = [
    path("movies/", views.movie_list, name="list"),
    path("movies/<int:pk>/", views.movie_detail, name="detail"),
]
