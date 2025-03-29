from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobApplicationViewSet

router = DefaultRouter()
router.register(r'recruiter/jobapplication', JobApplicationViewSet, basename='recruiter-jobapplication')
router.register(r'candidate/jobapplication', JobApplicationViewSet, basename='candidate-jobapplication')

urlpatterns = [
    path('', include(router.urls)),
]