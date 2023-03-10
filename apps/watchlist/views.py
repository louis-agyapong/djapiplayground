from django.http import Http404, JsonResponse
from django.shortcuts import render

from .models import Movie


def movie_list(request):
    movies = Movie.objects.all()
    data = {
        "movies": list(movies.values("name", "description", "active")),
    }
    return JsonResponse(data)


def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        raise Http404("Movie does not exist")
    data = {
        "name": movie.title,
        "description": movie.description,
        "active": movie.active,
    }
    print(movie)
    return JsonResponse(data)
