from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import Recruiter


class JobApplicationFormTemplate(models.Model):
    """
    Stores the JSON schema for rendering a job application form.
    """

    template = models.JSONField(
        help_text="JSON schema defining fields for the job application form",
        default=dict,
    )

    def __str__(self):
        return f"JobApplicationFormSchema #{self.pk}"


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("contract", "Contract"),
        ("internship", "Internship"),
    ]

    title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)  # Department or Team
    description = models.TextField()
    responsibilities = ArrayField(
        models.TextField(),
        blank=True,
        default=list,
        help_text="List of responsibilities",
    )
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    location = models.CharField(max_length=255, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    recruiter = models.ForeignKey("users.Recruiter", on_delete=models.CASCADE)
    form_template = models.ForeignKey(
        JobApplicationFormTemplate, on_delete=models.PROTECT, related_name="postings"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.department}"


class JobPostingSkill(models.Model):
    job_posting = models.ForeignKey(
        JobPosting, on_delete=models.CASCADE, related_name="posting_skills"
    )
    skill = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name="skill_postings"
    )

    class Meta:
        unique_together = ("job_posting", "skill")

    def __str__(self):
        return f"{self.job_posting} - {self.skill}"
