from rest_framework import serializers

from users.serializers import RecruiterSerializer
from .models import JobPosting, Skill, JobApplicationFormTemplate, JobPostingSkill
from users.models import Recruiter

from rest_framework import serializers

from rest_framework import serializers


class FieldSerializer(serializers.Serializer):
    FIELD_TYPE_CHOICES = [
        ("text", "text"),
        ("textarea", "textarea"),
        ("checkbox", "checkbox"),
        ("select", "select"),
        ("radio", "radio"),
        ("number", "number"),
        ("date", "date"),
        ("file", "file"),
    ]

    name = serializers.CharField(
        min_length=1,
        error_messages={
            "blank": "Field name required",
            "min_length": "Field name required",
        },
    )
    label = serializers.CharField(
        min_length=1,
        error_messages={
            "blank": "Label required",
            "min_length": "Label required",
        },
    )
    type = serializers.ChoiceField(choices=FIELD_TYPE_CHOICES)
    required = serializers.BooleanField()
    options = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
    )


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class JobApplicationFormTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplicationFormTemplate
        fields = ["id", "template"]


class JobPostingSerializer(serializers.ModelSerializer):
    recruiter = RecruiterSerializer(read_only=True)

    form_template = JobApplicationFormTemplateSerializer(read_only=True)
    skills = serializers.SerializerMethodField()

    def get_skills(self, obj):
        skills = [ps.skill for ps in obj.posting_skills.all()]
        return SkillSerializer(skills, many=True).data

    class Meta:
        model = JobPosting
        fields = [
            "id",
            "title",
            "department",
            "description",
            "responsibilities",
            "employment_type",
            "location",
            "salary",
            "recruiter",
            "skills",
            "form_template",
            "is_active",
            "created_at",
            "updated_at",
        ]


class JobPostingCreateUpdateSerializer(serializers.ModelSerializer):
    # Accept list of skill names; create if missing
    skills = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True,
        help_text="List of skill names",
    )
    form_template = serializers.JSONField(write_only=True)

    # read-only nested serializer for output
    form_template_data = JobApplicationFormTemplateSerializer(
        source="form_template", read_only=True
    )

    class Meta:
        model = JobPosting
        fields = [
            "title",
            "department",
            "description",
            "responsibilities",
            "employment_type",
            "location",
            "salary",
            "form_template",  # input (write_only)
            "form_template_data",
            "skills",
        ]

    def _handle_skills(self, posting, skill_names):
        # Normalize and dedupe
        normalized = set(name.strip().lower() for name in skill_names if name.strip())
        skills = []
        for name in normalized:
            skill, created = Skill.objects.get_or_create(
                name__iexact=name, defaults={"name": name}
            )
            skills.append(skill)
        # Reset links
        posting.posting_skills.all().delete()
        links = [JobPostingSkill(job_posting=posting, skill=skill) for skill in skills]
        JobPostingSkill.objects.bulk_create(links, ignore_conflicts=True)

    def create(self, validated_data):
        skill_names = validated_data.pop("skills", [])

        form_template = validated_data.get("form_template", [])

        field_serializer = FieldSerializer(data=form_template, many=True)
        field_serializer.is_valid(raise_exception=True)
        validated_form_template = field_serializer.validated_data

        currentjobtemplate = JobApplicationFormTemplate.objects.create(
            template=validated_form_template
        )
        newdata = {**validated_data, "form_template": currentjobtemplate}

        posting = super().create(newdata)
        self._handle_skills(posting, skill_names)
        return posting

    def update(self, instance, validated_data):
        skill_names = validated_data.pop("skills", None)
        posting = super().update(instance, validated_data)
        if skill_names is not None:
            self._handle_skills(posting, skill_names)
        return posting
