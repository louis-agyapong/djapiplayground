from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account.api.throttling import ReviewCreateThrottling, ReviewListThrottling
from apps.watchlist.api.permissions import ReviewUserOrReadOnly
from apps.watchlist.models import Movie, Review, StreamingPlatform

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
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"Error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
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
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottling]

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
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({"Error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({"Error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({"Error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class MovieReviewList(APIView):
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ["review_user__username", "active "]
#     # permission_classes = [IsAuthenticated]
#     # throttle_classes = [ReviewListThrottling]

#     def get(self, request, pk):
#         movie_review = Review.objects.filter(movie=pk)
#         serializer = ReviewSerializer(movie_review, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class MovieReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["review_user__username", "active"]
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottling]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Review.objects.filter(movie=pk)


class ReviewCreate(APIView):
    # throttle_classes = [ReviewCreateThrottling]

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


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     username = self.kwargs["username"]
    #     # username = self.request.user
    #     return Review.objects.filter(review_user__username=username)

    def get_queryset(self):
        """
        Filtering against a query param in the URL
        """
        username = self.request.query_params.get("username", None)
        # username = self.request.user
        return Review.objects.filter(review_user__username=username)


@api_view(["GET"])
def user_review(request, username):
    if request.method == "GET":
        reviews = Review.objects.filter(review_user__username=username)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
