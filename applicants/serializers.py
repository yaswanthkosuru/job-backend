from rest_framework import serializers
from .models import JobApplication
from jobpostings.models import JobPosting
from users.models import Candidate, User
from users.serializers import CandidateSerializer
from jobpostings.serializers import JobPostingSerializer
from rest_framework.exceptions import ValidationError
from .validators import validate_user_data


class CandidateJobApplicationSerializer(serializers.ModelSerializer):
    # Match model field name (jobposting), but keep external field name jobposting_id
    jobposting_id = serializers.PrimaryKeyRelatedField(  # model field
        queryset=JobPosting.objects.all(),
        required=True,
    )

    def validate(self, data):
        jobposting = data.get("jobposting")  # because of source="jobposting"
        user_details = data.get("user_details", {})

        if jobposting:
            # Ensure you're accessing the actual template list (not the model)
            form_template = jobposting.form_template.template  # adjust if needed
            result = validate_user_data(form_template, user_details)

            if not result.get("valid"):
                raise serializers.ValidationError(
                    {"user_details": result.get("error", "Invalid form data")}
                )

        return data

    def create(self, validated_data):
        # 1. Pull out “user_details” so we can register/find a User + Candidate
        user_details = validated_data.pop("user_details", {})

        print(user_details, "user_details")

        # 2. Create (or get) a User with role=candidate
        user_obj, _ = User.objects.get_or_create(
            email=user_details.get("Email"),  # be careful: Email vs email
            defaults={
                "role": "candidate",
                "phone": user_details.get("phone_number"),
                "username": user_details.get("Email"),
            },
        )

        # 3. Create (or get) a Candidate tied to that User
        candidate_obj, _ = Candidate.objects.get_or_create(user=user_obj)

        # 4. Inject “candidate” back into validated_data
        validated_data["candidate"] = candidate_obj

        instance = JobApplication.objects.create(
            jobposting=validated_data.get("jobposting_id"),
            candidate=candidate_obj,
            user_details=user_details,
        )

        return instance

    class Meta:
        model = JobApplication
        fields = [
            "jobposting_id",  # public name
            "applied_at",
            "status",
            "cover_letter",
            "user_details",
            "additional_notes",
        ]
        read_only_fields = ["applied_at", "status"]


class RecruiterJobApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobApplication
        fields = [
            "user_details",
            "additional_notes",
            "applied_at",
            "status",
            "cover_letter",
            "id",
        ]
