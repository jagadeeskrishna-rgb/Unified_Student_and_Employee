from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import Client, TestCase

from .models import Company, EmployeeProfile, EmploymentRecord, Profile, Role, SalaryRecord
from .services import rebuild_verification_issues


class LifecycleModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("employee1", "employee@example.com", "pass12345")
        Profile.objects.create(user=self.user, role=Role.EMPLOYEE, mobile="9000000001", demo_identity_number="DEMO-1")
        self.company = Company.objects.create(name="DemoTech", registration_number="REG-001", industry="IT", contact_email="hr@demo.test", contact_mobile="9000000002")
        self.employee = EmployeeProfile.objects.create(user=self.user, full_name="Demo Employee", ulin="ULIN001", designation="Developer", expected_salary=30000)

    def test_salary_mismatch_flag(self):
        salary = SalaryRecord.objects.create(employee=self.employee, company=self.company, month=4, year=2026, expected_salary=30000, paid_salary=25000)
        self.assertTrue(salary.has_mismatch)

    def test_month_validation(self):
        salary = SalaryRecord(employee=self.employee, company=self.company, month=13, year=2026, expected_salary=30000, paid_salary=30000)
        with self.assertRaises(ValidationError):
            salary.clean()

    def test_multiple_active_employment_detection(self):
        EmploymentRecord.objects.create(employee=self.employee, company=self.company, designation="Developer", start_date="2026-01-01", status="ACTIVE")
        other = Company.objects.create(name="OtherCo", registration_number="REG-002", industry="IT", contact_email="hr@other.test", contact_mobile="9000000003")
        EmploymentRecord.objects.create(employee=self.employee, company=other, designation="Consultant", start_date="2026-02-01", status="ACTIVE")
        issues = rebuild_verification_issues()
        self.assertTrue(any(issue.issue_type == "MULTIPLE_ACTIVE" for issue in issues))


class LifecycleViewTests(TestCase):
    def test_login_required_for_dashboard(self):
        response = Client().get("/dashboard/")
        self.assertEqual(response.status_code, 302)
