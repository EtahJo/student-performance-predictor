from rest_framework import serializers
from .models import QuizAttempt

class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = [
            "id",
            "created_at",
            "quiz_score",
            "topic_accuracy",
            "attempts",
            "time_spent_sec",
            "actual_band",
        ]
        read_only_fields = ["id", "created_at"]

class PredictRequestSerializer(serializers.Serializer):
    quiz_score = serializers.FloatField(min_value=0, max_value=100)
    topic_accuracy = serializers.FloatField(min_value=0, max_value=1)
    attempts = serializers.IntegerField(min_value=1)
    time_spent_sec = serializers.IntegerField(min_value=0)