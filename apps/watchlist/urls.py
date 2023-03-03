from django.urls import include, path

from . import views

app_name = "movies"

urlpatterns = [
    path("movies/", views.movie_list, name="list"),
    path("movies/<int:pk>/", views.movie_detail, name="detail"),
]
