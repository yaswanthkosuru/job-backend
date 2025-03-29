from rest_framework import serializers
from .models import User, Recruiter, Interviewer, Candidate, Skill
from organisations.models import Organisation
from organisations.serializers import OrganisationSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']
        read_only_fields = ['id']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", 'email', 'phone', 'password', 'role', 'username']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'phone': {'required': True},
            "id": {'read_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class RecruiterSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    organisation_id = serializers.IntegerField(write_only=True)
    organisation = OrganisationSerializer(read_only=True)

    class Meta:
        model = Recruiter
        fields = ['user', 'organisation_id', 'organisation']
        read_only_fields = ['organisation']

    def create(self, validated_data):
        request_data = self.context['request'].data
        organisation_id = request_data.get('organisation_id', None)
        try:
            organisation = Organisation.objects.get(id=organisation_id)
        except Organisation.DoesNotExist:
            raise serializers.ValidationError({"organisation_id": "Invalid organisation ID."})

        user = User.objects.create_user(
            email=request_data['email'],
            password=request_data['password'],
            phone=request_data['phone'],
            role='recruiter',
            username=request_data.get('username', '')
        )
        recruiter = Recruiter.objects.create(user=user, organisation=organisation)
        return recruiter

class InterviewerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    job_title = serializers.CharField(required=False, allow_blank=True)
    department = serializers.CharField(required=False, allow_blank=True)
    years_of_experience = serializers.IntegerField(required=False, allow_null=True)
    bio = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Interviewer
        fields = ['user', 'job_title', 'department', 'years_of_experience', 'bio']
        read_only_fields = ['user']

class CandidateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'phone', 'username']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'phone': {'required': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(
            **validated_data,
            role='candidate'
        )

class CandidateSerializer(serializers.ModelSerializer):
    user = CandidateUserSerializer()
    skills = SkillSerializer(read_only=True, many=True)
    required_skills = serializers.ListField(child=serializers.CharField(), write_only=True)


    class Meta:
        model = Candidate
        fields = [
            'user', 'linkedin_profile', 'github_profile',
            'degree', 'institution', 'year_of_completion',
            'job_title', 'company', 'start_date', 'end_date', 'currently_working',
            'skills', 'job_type', 'expected_salary', 'notice_period', 'resume_file_url',"required_skills","id"
        ]
        read_only_fields = ['user','id']
        write_only_fields = ['required_skills']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        required_skills = validated_data.pop('required_skills', [])  
        user_serializer = CandidateUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        candidate = Candidate.objects.create(user=user, **validated_data)
        
        # Add required_skills to the candidate's skills
        skill_objects = []
        for skill_name in required_skills:
            skill_name = skill_name.lower()
            try:
                skill_object = Skill.objects.get(name=skill_name)
            except Skill.DoesNotExist:
                skill_object = Skill.objects.create(name=skill_name)
            skill_objects.append(skill_object)

        candidate.skills.add(*skill_objects)
        return candidate

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print(user,"user")
        token = super().get_token(user)
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        
        if user.role == 'recruiter':
            try:
                recruiter = Recruiter.objects.get(user=user)
                recruiter_serializer = RecruiterSerializer(recruiter)
                data['user_data'] = recruiter_serializer.data
            except Recruiter.DoesNotExist:
                pass
        
        return data
