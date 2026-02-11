from django.db import models

class QuizAttempt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    quiz_score = models.FloatField()         
    topic_accuracy = models.FloatField()     
    attempts = models.PositiveIntegerField()
    time_spent_sec = models.PositiveIntegerField()
    actual_band = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        return f"Attempt {self.id} score={self.quiz_score} band={self.actual_band}"