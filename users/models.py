from django.db import models
from django.contrib.auth.models import AbstractUser

# User Model (Base)
class User(AbstractUser):
    ROLE_CHOICES = [
        ("recruiter", "Recruiter"),
        ("interviewer", "Interviewer"),
        ("candidate", "Candidate"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True, unique=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    def __str__(self):
        return f"{self.email} - {self.role}"


# Recruiter Model
class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    organisation = models.OneToOneField("organisations.Organisation", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


# Interviewer Model
class Interviewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    job_title = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.email


# Skill Model
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Candidate Model
class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    linkedin_profile = models.URLField(blank=True, null=True)
    github_profile = models.URLField(blank=True, null=True)

    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    year_of_completion = models.IntegerField()

    job_title = models.CharField(max_length=200, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    currently_working = models.BooleanField(default=False)

    skills = models.ManyToManyField(Skill, blank=True)

    job_type = models.CharField(
        max_length=100,
        choices=[("Full-time", "Full-time"), ("Part-time", "Part-time"), ("Contract", "Contract")]
    )
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2)
    notice_period = models.IntegerField(help_text="Notice period in days")

    resume_file_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.job_title if self.job_title else 'No Job Title'}"
