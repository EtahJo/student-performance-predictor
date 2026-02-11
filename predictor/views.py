from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import QuizAttempt
from .serializers import QuizAttemptSerializer, PredictRequestSerializer
from .ml import predict_band

@api_view(["POST"])
def create_attempt(request):
    serializer = QuizAttemptSerializer(data=request.data)
    if serializer.is_valid():
        attempt = serializer.save()
        return Response(QuizAttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def list_attempts(request):
    qs = QuizAttempt.objects.order_by("-created_at")[:200]
    return Response(QuizAttemptSerializer(qs, many=True).data)

@api_view(["POST"])
def predict(request):
    serializer = PredictRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    result = predict_band(serializer.validated_data)
    return Response(result)