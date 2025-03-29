from rest_framework import viewsets

from users.models import Recruiter
from .models import JobPosting
from .serializers import JobPostingSerializer
from rest_framework.permissions import IsAuthenticated

class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(recruiter__user=self.request.user)


    def perform_create(self, serializer):
        recruiter = self.request.user.recruiter
        serializer.save(recruiter=recruiter)