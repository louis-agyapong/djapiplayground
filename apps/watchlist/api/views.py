from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from apps.watchlist.models import Movie, Review, StreamingPlatform
from apps.watchlist.api.permissions import ReviewUserOrReadOnly

from .serializers import MovieSerializer, ReviewSerializer, StreamingPlatformSerializer
from .utils import has_reviewed_movie, validate_title_and_description


@api_view(["GET", "POST"])
def movie_list(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def movie_detail(request, pk):
    if request.method == "GET":
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"Error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "PUT":
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"Error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"Error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieListAPIView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description")
        active = request.data.get("active")

        error_response = validate_title_and_description(title, description)

        if error_response is not None:
            return error_response

        movie_data = Movie.objects.create(title=title, description=description, active=active)
        serializer = MovieSerializer(movie_data)
        if serializer:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailAPIView(APIView):
    def get(self, request, pk):
        movie = Movie.objects.filter(pk=pk).first()
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        title = request.data.get("title")
        description = request.data.get("description")

        error_response = validate_title_and_description(title, description)

        if error_response is not None:
            return error_response

        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"Error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"Error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"Error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlatformListPIView(APIView):
    def get(self, request):
        platform = StreamingPlatform.objects.all()
        serializer = StreamingPlatformSerializer(platform, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlatformDetailAPIVeiw(APIView):
    def get(self, request, pk):
        try:
            platform = StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist:
            return Response(
                {"Error": "Streaming Platform not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = StreamingPlatformSerializer(platform)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            platform = StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist:
            return Response(
                {"Error": "Streaming Platform not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = StreamingPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            platform = StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist:
            return Response(
                {"Error": "Streaming Platform not found"}, status=status.HTTP_404_NOT_FOUND
            )
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        review = Review.objects.all()
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailAPIView(APIView):
    permission_classes = [ReviewUserOrReadOnly]

    def get(self, request, pk):
        review = Review.objects.filter(pk=pk).first()
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        review = Review.objects.filter(pk=pk).first()
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = Review.objects.filter(pk=pk).first()
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieReviewList(APIView):
    def get(self, request, pk):
        movie_review = Review.objects.filter(movie=pk)
        serializer = ReviewSerializer(movie_review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewCreate(APIView):
    def post(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        review_user = self.request.user
        rating = request.data.get("rating")
        description = request.data.get("description")
        active = request.data.get("active")

        if has_reviewed_movie(movie, review_user):
            raise ValidationError("You have already reviewed this movie.")

        data = {
            "movie": movie.pk,
            "rating": rating,
            "description": description,
            "average_rating": movie.average_rating,
            "num_rating": movie.average_rating,
            "active": active,
            "review_user": review_user.pk,
        }

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            if movie.num_rating == 0:
                movie.average_rating = serializer.validated_data["rating"]
            else:
                movie.average_rating = (
                    movie.average_rating + serializer.validated_data["rating"]
                ) / 2

            movie.num_rating = movie.num_rating + 1
            movie.save()
            serializer.save(movie=movie, review_user=review_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
