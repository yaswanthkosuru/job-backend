from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "Setup groups and assign permissions for Recruiters, Interviewers, and Candidates"

    def handle(self, *args, **options):
        # Create or get groups
        recruiters_group, _ = Group.objects.get_or_create(name="Recruiters")
        interviewers_group, _ = Group.objects.get_or_create(name="Interviewers")
        candidates_group, _ = Group.objects.get_or_create(name="Candidates")

        # Get content types for each model
        # jobposting_ct = ContentType.objects.get_for_model(JobPosting)
        # candidate_ct = ContentType.objects.get_for_model(Candidate)
        # interview_ct = ContentType.objects.get_for_model(Interview)

        # -------------------------------
        # Recruiters: Full access to JobPosting, Candidate, and Interview models.
        # (i.e., add, change, delete, and view permissions)
        # -------------------------------
        # recruiter_permissions = Permission.objects.filter(
        #     content_type__in=[jobposting_ct, candidate_ct, interview_ct]
        # )
        # recruiters_group.permissions.set(recruiter_permissions)

        # -------------------------------
        # Interviewers: Limited access.
        # They can view job postings and candidates, and update interview feedback.
        # -------------------------------
        # view_jobposting = Permission.objects.get(
        #     codename="view_jobposting", content_type=jobposting_ct
        # )
        # view_candidate = Permission.objects.get(
        #     codename="view_candidate", content_type=candidate_ct
        # )
        # change_interview = Permission.objects.get(
        #     codename="change_interview", content_type=interview_ct
        # )
        # interviewers_group.permissions.set(
        #     [
        #         view_jobposting,
        #         view_candidate,
        #         change_interview,
        #     ]
        # )

        # -------------------------------
        # Candidates: Limited actions.
        # They can add their candidate profile and view job postings.
        # -------------------------------
        # add_candidate = Permission.objects.get(
        #     codename="add_candidate", content_type=candidate_ct
        # )
        # candidate_view_jobposting = Permission.objects.get(
        #     codename="view_jobposting", content_type=jobposting_ct
        # )
        # candidates_group.permissions.set(
        #     [
        #         add_candidate,
        #         candidate_view_jobposting,
        #     ]
        # )

        self.stdout.write(
            self.style.SUCCESS("Groups and permissions have been set up successfully.")
        )
