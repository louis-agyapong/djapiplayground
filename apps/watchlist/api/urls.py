from django.urls import path, include

from apps.watchlist.api import views


urlpatterns = [
    path("movie/", views.MovieListAPIView.as_view(), name="list"),
    path("movie/<int:pk>/", views.MovieDetailAPIView.as_view(), name="detail"),
    path("movie/platform/", views.PlatformListPIView.as_view(), name="platform_list"),
    path("movie/platform/<int:pk>/", views.PlatformDetailAPIVeiw.as_view(), name="platform_detail"),
    path("movie/review/", views.ReviewListAPIView.as_view(), name="review_list"),
    path("movie/review/<int:pk>/", views.ReviewDetailAPIView.as_view(), name="review_detail"),
    path("movie/<int:pk>/review/", views.MovieReviewList.as_view(), name="movie_reviews"),
    path("movie/<int:pk>/review-create/", views.ReviewCreate.as_view(), name="review_create"),
    path("movie/reviews/<str:username>/", views.UserReview.as_view(), name="user-review-detail")
]
