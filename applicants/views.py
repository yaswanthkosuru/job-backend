from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import JobApplication
from .serializers import (
    CandidateJobApplicationSerializer,
    RecruiterJobApplicationSerializer,
)

# views.py
import os
import requests
from rest_framework.views import APIView


class CandidateJobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = CandidateJobApplicationSerializer


class RecruiterJobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = RecruiterJobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        jobposting_id = self.request.query_params.get("jobposting")
        if jobposting_id:
            return JobApplication.objects.filter(jobposting=jobposting_id)
        return JobApplication.objects.all()
