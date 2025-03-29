from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from typing import Type
from .models import Recruiter, Interviewer, Candidate, User


@receiver(post_save, sender=Recruiter)
@receiver(post_save, sender=Interviewer)
@receiver(post_save, sender=Candidate)
def assign_user_to_group(sender, instance, created, **kwargs):
    """Handles assigning users to the correct group based on their role."""
    if created:
        group_mapping = {
            Recruiter: "Recruiters",
            Interviewer: "Interviewers",
            Candidate: "Candidates",
        }
        print(sender, instance, created)
        group_name = group_mapping.get(sender)
        if group_name:
            if instance.user:
                group, _ = Group.objects.get_or_create(name=group_name)
                instance.user.groups.add(group)
