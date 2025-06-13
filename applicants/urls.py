from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CandidateJobApplicationViewSet, RecruiterJobApplicationViewSet

router = DefaultRouter()
router.register(
    r"candidate/jobapplication",
    CandidateJobApplicationViewSet,
    basename="candidate-jobapplication",
)

router.register(
    r"recruiter/jobapplication",
    RecruiterJobApplicationViewSet,
    basename="recruiter-jobapplication",
)


urlpatterns = [
    path("", include(router.urls)),
]
