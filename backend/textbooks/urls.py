from django.urls import path
from .views import LoginView, DocumentParser, GetTokenView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path('ingest/', DocumentParser.as_view(), name='document-ingest'),
    path("get-token/", GetTokenView.as_view(), name="get-token"),
]
