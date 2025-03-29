from rest_framework import serializers
from users.serializers import RecruiterSerializer, SkillSerializer
from .models import JobPosting
from users.models import Recruiter, Skill
from organisations.models import Organisation
from users.models import User

class JobPostingSerializer(serializers.ModelSerializer):
    recruiter = RecruiterSerializer(read_only=True)
    required_skills = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        default=list()
    )
    skills = SkillSerializer(read_only=True, many=True, source='required_skills')

    class Meta:
        model = JobPosting
        fields = '__all__'
        read_only_fields = ['recruiter']

    def create(self, validated_data):
        required_skills = validated_data.pop('required_skills', [])
        
        # Create the job posting first
        job_posting = JobPosting.objects.create(**validated_data)
        
        # Add required_skills if any were provided
        if required_skills:
            skill_objects = []
            for skill_name in required_skills:
                skill_name = skill_name.lower()
                try:
                    skill_object = Skill.objects.get(name=skill_name)
                except Skill.DoesNotExist:
                    skill_object = Skill.objects.create(name=skill_name)
                skill_objects.append(skill_object)

            job_posting.required_skills.add(*skill_objects)
        
        return job_posting

    def update(self, instance, validated_data):
        required_skills = validated_data.pop('required_skills', [])

        # Update the job posting
        instance.title = validated_data.get('title', instance.title)
        instance.department = validated_data.get('department', instance.department)
        instance.description = validated_data.get('description', instance.description)
        instance.responsibilities = validated_data.get('responsibilities', instance.responsibilities)
        instance.employment_type = validated_data.get('employment_type', instance.employment_type)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.location = validated_data.get('location', instance.location)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        # Update required_skills if any were provided
        if required_skills:
            instance.required_skills.clear()
            skill_objects = []
            for skill_name in required_skills:
                skill_name = skill_name.lower()
                try:
                    skill_object = Skill.objects.get(name=skill_name)
                except Skill.DoesNotExist:
                    skill_object = Skill.objects.create(name=skill_name)
                skill_objects.append(skill_object)

            instance.required_skills.add(*skill_objects)

        return instance
