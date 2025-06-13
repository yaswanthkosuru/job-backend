# views.py
import os
import requests
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


from users.models import Recruiter
from .models import JobPosting, Skill, JobApplicationFormTemplate


from .serializers import (
    JobPostingSerializer,
    JobPostingCreateUpdateSerializer,
    SkillSerializer,
    JobApplicationFormTemplateSerializer,
)


class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = (
        JobPosting.objects.all()
        .select_related("recruiter", "form_template")
        .prefetch_related("posting_skills__skill")
    )

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_authentication(self, request):
        if self.action in ["create", "update", "partial_update"]:
            super().perform_authentication(request)
        else:
            pass

    # filter_backends = [
    #     DjangoFilterBackend,
    #     filters.SearchFilter,
    #     filters.OrderingFilter,
    # ]
    # filterset_fields = ["employment_type", "location", "is_active"]
    # search_fields = ["title", "department", "description", "responsibilities"]
    # ordering_fields = ["created_at", "salary"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return JobPostingCreateUpdateSerializer
        return JobPostingSerializer

    def perform_create(self, serializer):
        # Automatically assign request.user as recruiter
        print(self.request.user)
        recruiter = Recruiter.objects.get(user=self.request.user)
        serializer.save(recruiter=recruiter)


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "name"  # allow fetching by skill name


class JobApplicationFormTemplateViewSet(viewsets.ModelViewSet):
    queryset = JobApplicationFormTemplate.objects.all()
    serializer_class = JobApplicationFormTemplateSerializer
    permission_classes = [permissions.IsAdminUser]


class GenerateUploadUrlView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        token = "vercel_blob_rw_F5O4DmqJBHartY1S_SupnBvyBgKwrWevE9u3vyE71ePD2Hu"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        try:
            payload = {
                "pathname": request.data.get("pathname"),
                "contentType": request.data.get("contentType"),
                "clientPayload": request.data.get("clientPayload", {}),
                "multipart": request.data.get("multipart", False),
            }
            print(payload, "payload")
            print(headers)

            resp = requests.post(
                "https://blob.vercel-storage.com/v2/upload-url",
                headers=headers,
                json=payload,
            )

            co
            return Response(resp.json(), status=resp.status_code)

        except Exception as exc:
            return Response({"error": str(exc)}, status=500)
