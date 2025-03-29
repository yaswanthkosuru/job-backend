from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import OrganisationSerializer
from .models import Organisation


class CreateOrganisationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            return Response(
                {
                    "message": "Organisation created successfully",
                    "organisation_id": organisation.id,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
