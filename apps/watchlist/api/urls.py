from django.urls import path

from apps.watchlist.api import views


urlpatterns = [
    path("movies/", views.MovieListAPIView.as_view(), name="list"),
    path("movies/<int:pk>/", views.MovieDetailAPIView.as_view(), name="detail"),
]
