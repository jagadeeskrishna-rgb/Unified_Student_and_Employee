from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from lifecycle.models import Company, EmployeeProfile, EmploymentRecord, Profile, Role, SalaryQuery, SalaryRecord, StudentProfile
from lifecycle.services import rebuild_verification_issues


class Command(BaseCommand):
    help = "Create demo users and lifecycle records for academic demonstration."

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(username="admin", defaults={"email": "admin@example.test", "is_staff": True, "is_superuser": True})
        admin.set_password("Admin@12345")
        admin.save()
        Profile.objects.get_or_create(user=admin, defaults={"role": Role.ADMIN, "mobile": "9000000000", "demo_identity_number": "ADMIN-DEMO"})

        hr, _ = User.objects.get_or_create(username="hr_demo", defaults={"email": "hr@example.test"})
        hr.set_password("Hr@12345")
        hr.save()
        Profile.objects.get_or_create(user=hr, defaults={"role": Role.COMPANY, "mobile": "9000000001", "demo_identity_number": "HR-DEMO"})
        company, _ = Company.objects.get_or_create(name="DemoTech Solutions", defaults={"owner": hr, "registration_number": "DT-2026", "industry": "Software", "contact_email": "hr@demotech.test", "contact_mobile": "9000000001", "address": "Academic demo address"})

        student_user, _ = User.objects.get_or_create(username="student_demo", defaults={"email": "student@example.test", "first_name": "Asha", "last_name": "Kumar"})
        student_user.set_password("Student@12345")
        student_user.save()
        Profile.objects.get_or_create(user=student_user, defaults={"role": Role.STUDENT, "mobile": "9000000002", "demo_identity_number": "SID-100"})
        StudentProfile.objects.get_or_create(user=student_user, defaults={"full_name": "Asha Kumar", "roll_number": "CS2026001", "degree": "B.Sc Computer Science", "department": "Computer Science", "batch_year": 2026, "career_status": "PLACED", "expected_salary": 30000, "current_company": company})

        emp_user, _ = User.objects.get_or_create(username="employee_demo", defaults={"email": "employee@example.test", "first_name": "Ravi", "last_name": "Menon"})
        emp_user.set_password("Employee@12345")
        emp_user.save()
        Profile.objects.get_or_create(user=emp_user, defaults={"role": Role.EMPLOYEE, "mobile": "9000000003", "demo_identity_number": "EMP-100"})
        employee, _ = EmployeeProfile.objects.get_or_create(user=emp_user, defaults={"full_name": "Ravi Menon", "ulin": "ULIN-2026-001", "designation": "Junior Developer", "expected_salary": 30000})
        EmploymentRecord.objects.get_or_create(employee=employee, company=company, designation="Junior Developer", start_date="2026-04-01", status="ACTIVE")
        salary, _ = SalaryRecord.objects.get_or_create(employee=employee, company=company, month=4, year=2026, defaults={"expected_salary": 30000, "paid_salary": 25000})
        SalaryQuery.objects.get_or_create(employee=employee, salary_record=salary, subject="Salary mismatch", defaults={"description": "Paid amount differs from expected monthly salary."})
        rebuild_verification_issues()
        self.stdout.write(self.style.SUCCESS("Demo data created. Login: admin/Admin@12345, hr_demo/Hr@12345, student_demo/Student@12345, employee_demo/Employee@12345"))
