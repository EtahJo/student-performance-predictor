from django.core.management.base import BaseCommand
from predictor.models import QuizAttempt
import random


def band_from_score(score:float)->str:
    if score>=80:return "A"
    if score >=65: return "B"
    if score >=50: return "C"
    return "D"


class Command(BaseCommand):
    help = "Seed synthetic quiz attempts for testing/training"

    def add_arguments(self, parser):
        parser.add_argument("--n",type=int,default=200)

    def handle(self,*args, **options):
        n= options["n"]
        rows= []
        for _ in range(n):
            quiz_score = random.uniform(0,100)
            topic_accuracy= max(0,min(1,random.gauss(mu=quiz_score/100,sigma=0.15)))
            attempts = random.randint(1,6)
            time_spent_sec= random.randint(60,2400)

            actual_band= band_from_score(quiz_score+(topic_accuracy*10)-(attempts*1.5))

            rows.append(QuizAttempt(
                quiz_score=quiz_score,
                topic_accuracy=topic_accuracy,
                attempts=attempts,
                time_spent_sec=time_spent_sec,
                actual_band=actual_band
            ))

        QuizAttempt.objects.bulk_create(rows)
        self.stdout.write(self.style.SUCCESS(f"Seeded {n} rows."))