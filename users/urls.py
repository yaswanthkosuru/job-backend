from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'skills', views.SkillViewSet, basename='skill')
router.register(r'user/recruiter', views.RecruiterViewSet, basename='recruiter')
router.register(r'user/interviewer', views.InterviewerViewSet, basename='interviewer')
router.register(r'user/candidate', views.CandidateViewSet, basename='candidate')




# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('user/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/me/', views.MeView.as_view(), name='me'),
]