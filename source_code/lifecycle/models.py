from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Role(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    STUDENT = "STUDENT", "Student"
    EMPLOYEE = "EMPLOYEE", "Employee"
    COMPANY = "COMPANY", "Company/HR"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices)
    mobile = models.CharField(max_length=15, blank=True)
    demo_identity_number = models.CharField(max_length=30, blank=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class Company(models.Model):
    owner = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="company_account")
    name = models.CharField(max_length=160, unique=True)
    registration_number = models.CharField(max_length=60, unique=True)
    industry = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_mobile = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    CAREER_STATUS = [
        ("STUDYING", "Studying"),
        ("SEARCHING", "Searching for Job"),
        ("INTERN", "Doing Internship"),
        ("PLACED", "Placed"),
        ("EMPLOYED", "Currently Employed"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    full_name = models.CharField(max_length=140)
    roll_number = models.CharField(max_length=40, unique=True)
    degree = models.CharField(max_length=120)
    department = models.CharField(max_length=120)
    batch_year = models.PositiveIntegerField()
    career_status = models.CharField(max_length=20, choices=CAREER_STATUS, default="STUDYING")
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class EducationRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="education_records")
    qualification = models.CharField(max_length=80)
    institution = models.CharField(max_length=160)
    year_of_passing = models.PositiveIntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        if self.percentage < 0 or self.percentage > 100:
            raise ValidationError("Percentage must be between 0 and 100.")


class Skill(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=80)
    proficiency = models.CharField(max_length=40, default="Intermediate")

    class Meta:
        unique_together = ("student", "name")


class Certification(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="certifications")
    title = models.CharField(max_length=140)
    issuer = models.CharField(max_length=140)
    issued_on = models.DateField()


class Internship(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="internships")
    company_name = models.CharField(max_length=140)
    role = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, default="Completed")


class Placement(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="placements")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    designation = models.CharField(max_length=120)
    offered_salary = models.DecimalField(max_digits=10, decimal_places=2)
    offer_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=30, default="Offered")


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile")
    full_name = models.CharField(max_length=140)
    ulin = models.CharField("Unique Lifecycle Identification Number", max_length=40, unique=True)
    designation = models.CharField(max_length=120)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} ({self.ulin})"


class EmploymentRecord(models.Model):
    STATUS = [
        ("ACTIVE", "Active"),
        ("RESIGNED", "Resigned"),
        ("TERMINATED", "Terminated"),
        ("NOTICE", "Notice Period"),
    ]
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="employment_records")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employment_records")
    designation = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="ACTIVE")

    @property
    def is_active(self):
        return self.status in {"ACTIVE", "NOTICE"}


class SalaryRecord(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="salary_records")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="salary_records")
    month = models.PositiveSmallIntegerField()
    year = models.PositiveIntegerField()
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2)
    paid_salary = models.DecimalField(max_digits=10, decimal_places=2)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "company", "month", "year")
        ordering = ["-year", "-month"]

    @property
    def has_mismatch(self):
        return self.paid_salary != self.expected_salary

    def clean(self):
        if self.month < 1 or self.month > 12:
            raise ValidationError("Month must be between 1 and 12.")
        if self.paid_salary < 0 or self.expected_salary < 0:
            raise ValidationError("Salary values cannot be negative.")


class SalaryQuery(models.Model):
    STATUS = [("OPEN", "Open"), ("IN_REVIEW", "In Review"), ("RESOLVED", "Resolved"), ("REJECTED", "Rejected")]
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="salary_queries")
    salary_record = models.ForeignKey(SalaryRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name="queries")
    subject = models.CharField(max_length=140)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default="OPEN")
    admin_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class VerificationIssue(models.Model):
    ISSUE_TYPES = [
        ("DUPLICATE_EMAIL", "Duplicate Email"),
        ("DUPLICATE_MOBILE", "Duplicate Mobile"),
        ("DUPLICATE_ID", "Duplicate Demo Identity"),
        ("MULTIPLE_ACTIVE", "Multiple Active Employment"),
        ("SALARY_MISMATCH", "Salary Mismatch"),
    ]
    issue_type = models.CharField(max_length=40, choices=ISSUE_TYPES)
    summary = models.CharField(max_length=220)
    details = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.summary
