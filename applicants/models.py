from django.db import models
from django.db.models import Q
from django.contrib.postgres.fields import JSONField


# Create your models here.
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("interview", "Interview Scheduled"),
        ("rejected", "Rejected"),
        ("accepted", "Accepted"),
    ]

    jobposting = models.ForeignKey("jobpostings.JobPosting", on_delete=models.CASCADE)
    candidate = models.ForeignKey("users.Candidate", on_delete=models.CASCADE)
    user_details = models.JSONField(
        help_text="Stores user-submitted form values based on job_form_labels",
        default=dict,
        blank=True,
        null=True,
    )
    additional_notes = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    cover_letter = models.TextField(blank=True, null=True)

    def __str__(self):
        try:
            return f"{self.candidate.name} applied for {self.jobposting.title}"
        except AttributeError:
            return f"JobApplication {self.id}"

    class Meta:
        ordering = ["-applied_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["jobposting", "candidate"], name="unique_active_job_application"
            )
        ]
