from django.contrib import admin
from .models import CustomUser, CandidateProfile, CompanyProfile

admin.site.register(CustomUser)
admin.site.register(CandidateProfile)
admin.site.register(CompanyProfile)
