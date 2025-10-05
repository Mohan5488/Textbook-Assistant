from django.urls import path
from .views import LoginView, DocumentParser

urlpatterns = [
    path("login/", LoginView.as_view()),
    path('ingest/', DocumentParser.as_view(), name='document-ingest'),
]
