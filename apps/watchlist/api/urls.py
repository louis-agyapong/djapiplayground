from django.urls import path

from apps.watchlist.api import views


urlpatterns = [
    path("movie/", views.MovieListAPIView.as_view(), name="list"),
    path("movie/<int:pk>/", views.MovieDetailAPIView.as_view(), name="detail"),
    path("movie/streams/", views.StreamingListPIVeiw.as_view(), name="streams"),
]
