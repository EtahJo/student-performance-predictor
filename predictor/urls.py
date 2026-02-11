from django.urls import path
from . import views

urlpatterns = [
    path("attempts/", views.list_attempts),
    path("attempts-create/", views.create_attempt),
    path("predict/", views.predict),
]