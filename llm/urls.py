from django.urls import path
from .views import GenerateCandidateSummaryAPIView

urlpatterns = [
    path('llm/generatecandidatesummary/', GenerateCandidateSummaryAPIView.as_view(), name='generate-candidate-summary'),
]