from http import HTTPStatus

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Choice, Poll, Vote
from .serializer import ChoiceSerializer, PollSerializer, VoteSerializer


class PollList(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PollDetail(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
        return queryset

    serializer_class = ChoiceSerializer


class CreateVote(APIView):
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]


    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {"choice": choice_pk, "poll": pk, "voted_by": voted_by}
        serializer = VoteSerializer(data=data)
        try:
            vote = Vote.objects.get(poll=pk, voted_by=voted_by)
            return Response(
                {"error": "You have already voted for this poll."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Vote.DoesNotExist:
            serializer = VoteSerializer(data=data)
            if serializer.is_valid():
                vote = serializer.save()
                vote.votes += 1
                vote.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
