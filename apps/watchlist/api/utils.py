from rest_framework import status
from rest_framework.response import Response


def validate_name_and_description(name: str, description: str) -> Response:
    """
    Check if the name and description are the same and return a bad request response
    with an error message if they are.
    """
    if name == description:
        return Response(
            {"Error": "Name and description must not be the same"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return None
