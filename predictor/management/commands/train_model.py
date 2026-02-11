from django.core.management.base import BaseCommand
from predictor.models import QuizAttempt
from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report,accuracy_score

ARTIFACT_DIR = Path(__file__).resolve().parents[3]/"predictor" / "artifacts"
MODEL_PATH= ARTIFACT_DIR / "model.joblib"

FEATURES = ["quiz_score", "topic_accuracy","attempts","time_spent_sec"]
TARGET= "actual_band"

class Command(BaseCommand):
    help = "Train and save the student performance predictor model."

    def handle(self, *args,**options):
        ARTIFACT_DIR.mkdir(parents=True,exist_ok=True)

        qs = QuizAttempt.objects.exclude(actual_band__isnull=True).exclude(actual_band__exact="")
        if qs.count() <30:
            self.stdout.write(self.style.ERROR(
                f"Not enough labeled rows to train. Need 30+, found {qs.count()}."
            ))
            return

        data = list(qs.values(*FEATURES,TARGET))
        df= pd.DataFrame(data)

        X = df[FEATURES]
        y = df[TARGET].astype(str)

        X_train, X_test, y_train,y_test = train_test_split(
            X,y,test_size=0.2,random_state=42,stratify=y
        )

        model = Pipeline(steps=[
            ("scaler",StandardScaler()),
            ("clf",LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                C=1.0
            ))
        ])
        model.fit(X_train,y_train)
        preds= model.predict(X_test)
        
        acc = accuracy_score(y_test,preds)
        report = classification_report(y_test,preds)
        joblib.dump(model,MODEL_PATH)
        self.stdout.write(self.style.SUCCESS(f"Saved model to : {MODEL_PATH}"))
        self.stdout.write(self.style.SUCCESS(f"Accuracy:{acc:.4f}"))
        self.stdout.write(report)



