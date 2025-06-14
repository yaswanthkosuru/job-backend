# Generated by Django 5.1.7 on 2025-06-02 09:24

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplicationFormTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template', models.JSONField(default=dict, help_text='JSON schema defining fields for the job application form')),
            ],
        ),
        migrations.CreateModel(
            name='JobPostingSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobPosting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('department', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('responsibilities', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, default=list, help_text='List of responsibilities', size=None)),
                ('employment_type', models.CharField(choices=[('full_time', 'Full-time'), ('part_time', 'Part-time'), ('contract', 'Contract'), ('internship', 'Internship')], max_length=20)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('salary', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('form_template', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='postings', to='jobpostings.jobapplicationformtemplate')),
            ],
        ),
    ]
