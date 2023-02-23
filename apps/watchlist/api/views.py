from django.http import Http404, JsonResponse
from django.shortcuts import render
from rest_framework.response import Response

from apps.watchlist.models import Movie

from .serializers import MovieSerializer


def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies)
    return Response(serializer.data)


def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        raise Http404("Movie does not exist")
    serializer = MovieSerializer(movie)
    return Response(serializer.data)
