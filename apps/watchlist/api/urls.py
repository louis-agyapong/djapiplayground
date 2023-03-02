from django.urls import path

from apps.watchlist.api import views


urlpatterns = [
    path("movie/", views.MovieListAPIView.as_view(), name="list"),
    path("movie/<int:pk>/", views.MovieDetailAPIView.as_view(), name="detail"),
    path("movie/stream/", views.StreamListPIVeiw.as_view(), name="stream"),
    path("movie/stream/<int:pk>/", views.StreamDetailAPIVeiw.as_view(), name="stream_detail"),
    path("movie/review/", views.ReviewListAPIView.as_view(), name="review_list"),
    path("movie/review/<int:pk>/", views.ReviewDetailAPIView.as_view(), name="review_detail"),
]
