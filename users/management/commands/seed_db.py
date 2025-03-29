from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from faker import Faker
import random
from datetime import datetime, timedelta

from users.models import User, Recruiter, Interviewer, Candidate, Skill
from organisations.models import Organisation
from jobpostings.models import JobPosting
from applicants.models import JobApplication

class Command(BaseCommand):
    help = 'Seed the database with test data'

    def handle(self, *args, **options):
        fake = Faker()
        
        # Clear existing data
        JobApplication.objects.all().delete()
        JobPosting.objects.all().delete()
        Candidate.objects.all().delete()
        Interviewer.objects.all().delete()
        Recruiter.objects.all().delete()
        Organisation.objects.all().delete()
        Skill.objects.all().delete()
        User.objects.all().delete()

        # Create skills
        skills = [
            'Python', 'JavaScript', 'Java', 'C++', 'React', 'Node.js',
            'Django', 'Flask', 'SQL', 'MongoDB', 'AWS', 'Docker',
            'Kubernetes', 'Machine Learning', 'Data Analysis'
        ]
        skill_objects = []
        for skill in skills:
            skill_objects.append(Skill(name=skill))
        Skill.objects.bulk_create(skill_objects)

        # Create organisations
        organisations = []
        for _ in range(5):
            org = Organisation(
                name=fake.company(),
                location=fake.city(),
                industry=fake.random_element(elements=('Technology', 'Finance', 'Healthcare', 'Education', 'Manufacturing'))
            )
            organisations.append(org)
        Organisation.objects.bulk_create(organisations)

        # Create users and their profiles
        # Create recruiters
        for org in organisations:
            password = 'password123'
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=password,
                role='recruiter',
                phone=f'+1{fake.msisdn()[:10]}',
                is_active=True
            )
            Recruiter.objects.create(
                user=user,
                organisation=org
            )
            self.stdout.write(f"Recruiter created: {user.email} (Password: {password})")

        # Create interviewers
        for org in organisations:
            for _ in range(3):
                password = 'password123'
                user = User.objects.create_user(
                    username=fake.user_name(),
                    email=fake.email(),
                    password=password,
                    role='interviewer',
                    phone=f'+1{fake.msisdn()[:10]}',
                    is_active=True
                )
                Interviewer.objects.create(
                    user=user,
                    job_title=fake.job(),
                    department=fake.random_element(elements=('Engineering', 'Product', 'Design', 'Sales', 'Marketing')),
                    years_of_experience=random.randint(3, 15),
                    bio=fake.paragraph()
                )

        # Create candidates
        for _ in range(50):
            password = 'password123'
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=password,
                role='candidate',
                phone=f'+1{fake.msisdn()[:10]}',
                is_active=True
            )
            self.stdout.write(f"Candidate created: {user.email} (Password: {password})")
            
            candidate = Candidate(
                user=user,
                linkedin_profile=fake.url(),
                github_profile=fake.url(),
                degree=fake.random_element(elements=('B.E.', 'B.Tech', 'M.E.', 'M.Tech', 'B.Sc', 'M.Sc')),
                institution=fake.company(),
                year_of_completion=fake.year(),
                job_title=fake.job(),
                company=fake.company(),
                start_date=fake.date_between(start_date='-10y', end_date='-2y'),
                end_date=fake.date_between(start_date='-2y', end_date='today'),
                currently_working=random.choice([True, False]),
                job_type=fake.random_element(elements=('Full-time', 'Part-time', 'Contract')),
                expected_salary=random.randint(50000, 150000),
                notice_period=random.randint(15, 90),
                resume_file_url=fake.url()
            )
            candidate.save()
            
            # Add random skills to candidate
            random_skills = random.sample(list(Skill.objects.all()), random.randint(3, 7))
            candidate.skills.add(*random_skills)

        # Create job postings
        recruiters = list(Recruiter.objects.all())
        for _ in range(20):
            recruiter = random.choice(recruiters)
            job_posting = JobPosting(
                title=fake.job(),
                department=fake.random_element(elements=('Engineering', 'Product', 'Design', 'Sales', 'Marketing')),
                description=fake.paragraph(nb_sentences=5),
                responsibilities=fake.paragraph(nb_sentences=3),
                employment_type=fake.random_element(elements=('full_time', 'part_time', 'contract', 'internship')),
                location=fake.city(),
                salary=random.uniform(40000, 180000),
                recruiter=recruiter,
                is_active=random.choice([True, True, False])  # 2/3 chance of being active
            )
            job_posting.save()
            
            # Add random skills to job posting
            random_skills = random.sample(list(Skill.objects.all()), random.randint(3, 5))
            job_posting.required_skills.add(*random_skills)

        # Create job applications
        active_job_postings = JobPosting.objects.filter(is_active=True)
        candidates = list(Candidate.objects.all())
        
        for job_posting in active_job_postings:
            # Get candidates whose skills match at least 50% of job requirements
            matching_candidates = []
            for candidate in candidates:
                matching_skills = set(candidate.skills.all()) & set(job_posting.required_skills.all())
                if len(matching_skills) / len(job_posting.required_skills.all()) >= 0.5:
                    matching_candidates.append(candidate)
            
            # Create applications for matching candidates
            for candidate in random.sample(matching_candidates, min(3, len(matching_candidates))):
                application = JobApplication(
                    jobposting=job_posting,
                    candidate=candidate,
                    additional_notes=fake.paragraph(nb_sentences=2),
                    cover_letter=fake.paragraph(nb_sentences=5),
                    status=random.choice(['pending', 'interview', 'rejected', 'accepted'])
                )
                application.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))