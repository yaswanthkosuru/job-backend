from django.contrib import admin
from .models import User, Recruiter, Interviewer, Candidate

# Register your models here.
admin.site.register(User)
admin.site.register(Recruiter)
admin.site.register(Interviewer)
admin.site.register(Candidate)
