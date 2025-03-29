from rest_framework import generics, viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from applicants.models import JobApplication
from jobpostings.models import JobPosting

from .models import User, Recruiter, Interviewer, Candidate, Skill
from .serializers import (
    UserSerializer, RecruiterSerializer,
    InterviewerSerializer, CandidateSerializer, SkillSerializer,
    CustomTokenObtainPairSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView


class SkillViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ViewSet for managing skills."""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for managing users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Return the current user's details."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class RecruiterViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    """ViewSet for managing recruiters."""
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer

    def get_permissions(self):
        if self.action in ['update', 'retrieve']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        """Only current user can view their own profile."""
        return Recruiter.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        """Only the owner can update the recruiter profile."""
        instance = serializer.instance
        if instance.user != self.request.user:
            raise ValidationError("You don't have permission to update this profile")
        serializer.save()


class InterviewerViewSet(viewsets.ModelViewSet):
    """ViewSet for managing interviewers."""
    queryset = Interviewer.objects.all()
    serializer_class = InterviewerSerializer


class CandidateViewSet(viewsets.ModelViewSet):
    """ViewSet for managing candidates."""
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def get_permissions(self):
        if self.action in ['update', 'retrieve']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'recruiter':
            Jobposting_id = self.request.query_params.get('jobposting_id')
            show_applied = self.request.query_params.get('show_applied')
            
            if Jobposting_id:
                jobapplicationids = JobApplication.objects.filter(
                    jobposting_id=Jobposting_id
                ).values_list('candidate_id', flat=True)
                
                if show_applied:
                    return Candidate.objects.filter(id__in=jobapplicationids)
                else:
                    return Candidate.objects.exclude(id__in=jobapplicationids)
            
            return Candidate.objects.all()
        elif user.role == 'candidate':
            return Candidate.objects.filter(user=user)

    def perform_update(self, serializer):
        """Ensure only the owner or recruiters can update the candidate profile."""
        instance = serializer.instance
        if instance.user != self.request.user and self.request.user.role != 'recruiter':
            raise ValidationError("You don't have permission to update this profile")
        serializer.save()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user