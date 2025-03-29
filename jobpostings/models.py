from django.db import models

from users.models import Recruiter


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
    responsibilities = models.TextField()
    required_skills = models.ManyToManyField("users.Skill", blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    location = models.CharField(max_length=255, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    recruiter = models.ForeignKey("users.Recruiter", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.department}"
