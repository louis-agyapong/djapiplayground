from rest_framework import status
from rest_framework.response import Response
from apps.watchlist.models import Review


def validate_title_and_description(title: str, description: str) -> Response:
    """
    Check if the title and description are the same and return a bad  response
    with an error message if they are.
    """
    if title == description:
        return Response(
            {"Error": "Title and description must not be the same"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return None


def has_reviewed_movie(movie, user):
    """
    Returns True if the specified user has already reviewed the specified movie,
    and False otherwise.
    """
    return Review.objects.filter(movie=movie, review_user=user).exists()
