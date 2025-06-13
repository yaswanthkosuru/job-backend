from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GenerateUploadUrlView,
    JobPostingViewSet,
    SkillViewSet,
    JobApplicationFormTemplateViewSet,
)

router = DefaultRouter()
router.register(r"jobposting", JobPostingViewSet, basename="jobposting")
router.register(r"skills", SkillViewSet, basename="skill")
router.register(
    r"form-templates", JobApplicationFormTemplateViewSet, basename="template"
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "candidate/generateuploadurl",
        GenerateUploadUrlView.as_view(),
        name="generate-upload-url",
    ),
]
