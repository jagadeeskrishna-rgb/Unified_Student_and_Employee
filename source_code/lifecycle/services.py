from collections import Counter
from django.contrib.auth.models import User
from django.db.models import Count

from .models import EmploymentRecord, Profile, SalaryRecord, VerificationIssue


def rebuild_verification_issues():
    VerificationIssue.objects.all().delete()
    created = []

    for field, issue_type, label in [
        ("email", "DUPLICATE_EMAIL", "email address"),
    ]:
        duplicates = (
            User.objects.exclude(**{field: ""})
            .values(field)
            .annotate(total=Count("id"))
            .filter(total__gt=1)
        )
        for row in duplicates:
            created.append(VerificationIssue.objects.create(
                issue_type=issue_type,
                summary=f"Duplicate {label}: {row[field]}",
                details=f"{row['total']} users share the same {label}.",
            ))

    for field, issue_type, label in [
        ("mobile", "DUPLICATE_MOBILE", "mobile number"),
        ("demo_identity_number", "DUPLICATE_ID", "demo identity number"),
    ]:
        values = [value for value in Profile.objects.values_list(field, flat=True) if value]
        for value, total in Counter(values).items():
            if total > 1:
                created.append(VerificationIssue.objects.create(
                    issue_type=issue_type,
                    summary=f"Duplicate {label}: {value}",
                    details=f"{total} profiles share the same {label}.",
                ))

    active = EmploymentRecord.objects.filter(status__in=["ACTIVE", "NOTICE"]).values("employee__ulin", "employee__full_name").annotate(total=Count("id")).filter(total__gt=1)
    for row in active:
        created.append(VerificationIssue.objects.create(
            issue_type="MULTIPLE_ACTIVE",
            summary=f"Multiple active employment records for {row['employee__full_name']}",
            details=f"ULIN {row['employee__ulin']} has {row['total']} active/notice-period employment records.",
        ))

    for salary in SalaryRecord.objects.select_related("employee", "company"):
        if salary.has_mismatch:
            created.append(VerificationIssue.objects.create(
                issue_type="SALARY_MISMATCH",
                summary=f"Salary mismatch for {salary.employee.full_name}",
                details=f"{salary.company.name} uploaded INR {salary.paid_salary}; expected INR {salary.expected_salary}.",
            ))
    return created


def dashboard_metrics():
    from .models import Company, EmployeeProfile, SalaryQuery, StudentProfile
    employed_students = StudentProfile.objects.filter(career_status__in=["PLACED", "EMPLOYED"]).count()
    total_students = StudentProfile.objects.count()
    return {
        "total_users": User.objects.count(),
        "students": total_students,
        "employees": EmployeeProfile.objects.count(),
        "companies": Company.objects.count(),
        "open_queries": SalaryQuery.objects.exclude(status="RESOLVED").count(),
        "verification_issues": VerificationIssue.objects.filter(is_resolved=False).count(),
        "employment_ratio": round((employed_students / total_students) * 100, 2) if total_students else 0,
    }
