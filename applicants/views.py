from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import JobApplication
from users.models import Candidate
from .serializers import JobApplicationSerializer, BulkJobApplicationCreateSerializer
from django.utils import timezone

class  JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Recruiters can see all applications

        if self.request.user.recruiter:
            return JobApplication.objects.all()
        # Candidates can only see their own applications
        return JobApplication.objects.filter(candidate=self.request.user.candidate)

    def perform_create(self, serializer):
        # Set the candidate to the current user for candidate submissions
        if not self.request.user.recruiter:
            serializer.save(candidate=self.request.user.candidate)
        else:
            serializer.save()

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def bulk_create(self, request):
        """
        Bulk create job applications for multiple candidates
        
        Request body example:
        {
            "jobposting_id": 1,
            "candidate_ids": [1, 2, 3]
        }
        """
        serializer = BulkJobApplicationCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        jobposting_id = serializer.validated_data['jobposting_id']
        candidate_ids = serializer.validated_data['candidate_ids']
        
        # Validate input
        if not jobposting_id or not candidate_ids:
            return Response({"error": "jobposting_id and candidate_ids are required"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Limit the number of applications to prevent abuse
        if len(candidate_ids) > 100:
            return Response({"error": "Too many candidates. Maximum 100 allowed per request"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Use select_related to optimize database queries
        candidates = Candidate.objects.filter(id__in=candidate_ids).select_related('user')
        
        # Check if all candidates exist
        if candidates.count() != len(candidate_ids):
            existing_ids = set(candidates.values_list('id', flat=True))
            missing_ids = set(candidate_ids) - existing_ids
            return Response({
                "error": "One or more candidate IDs do not exist",
                "missing_ids": list(missing_ids)
            }, status=status.HTTP_400_BAD_REQUEST)
            
        
        # Create job applications
        applications = []
        current_time = timezone.now()
        for candidate in candidates:
            applications.append(JobApplication(
                jobposting=jobposting_id,
                candidate=candidate,
                status='pending',
                applied_at=current_time
            ))
        
        try:
            # Use bulk_create with batch_size to handle large sets
            created_apps = JobApplication.objects.bulk_create(applications, batch_size=50)
            
            # Return the created applications with full details
            serializer = self.get_serializer(created_apps, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                "error": f"Failed to create applications: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        jobapplication = self.get_object()
        if 'status' in request.data:
            jobapplication.status = request.data['status']
        if 'additional_notes' in request.data:
            jobapplication.additional_notes = request.data.get('additional_notes')
        jobapplication.save()
        return Response({"id": jobapplication.id, "status": jobapplication.status, "additional_notes": jobapplication.additional_notes}, status=status.HTTP_200_OK)
