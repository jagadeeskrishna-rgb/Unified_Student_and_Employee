from django.contrib import admin
from .models import (
    Certification, Company, EducationRecord, EmployeeProfile, EmploymentRecord,
    Internship, Placement, Profile, SalaryQuery, SalaryRecord, Skill,
    StudentProfile, VerificationIssue
)

for model in [Profile, Company, StudentProfile, EducationRecord, Skill, Certification,
              Internship, Placement, EmployeeProfile, EmploymentRecord, SalaryRecord,
              SalaryQuery, VerificationIssue]:
    admin.site.register(model)
