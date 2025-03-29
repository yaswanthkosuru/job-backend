from rest_framework import serializers
from .models import JobApplication
from jobpostings.models import JobPosting
from users.models import Candidate
from users.serializers import CandidateSerializer
from jobpostings.serializers import JobPostingSerializer

class JobApplicationSerializer(serializers.ModelSerializer):
    candidate_id = serializers.PrimaryKeyRelatedField(queryset=Candidate.objects.all(), required=True)
    jobposting_id = serializers.PrimaryKeyRelatedField(
        queryset=JobPosting.objects.all(),
        required=True
    )

    candidate = CandidateSerializer(read_only=True)
    # jobposting = JobPostingSerializer(read_only=True)
    
    class Meta:
        model = JobApplication
        fields = ['id', 'jobposting_id', 'candidate_id', 'applied_at', 'status', 'cover_letter', 'candidate', 'jobposting', 'additional_notes']
        read_only_fields = ['id', 'applied_at', 'status']

class BulkJobApplicationCreateSerializer(serializers.Serializer):
    jobposting_id = serializers.PrimaryKeyRelatedField(
        queryset=JobPosting.objects.all(),
        required=True
    )
    candidate_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )