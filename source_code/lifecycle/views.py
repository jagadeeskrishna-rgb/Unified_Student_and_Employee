from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CertificationForm, CompanyForm, EducationRecordForm, EmployeeProfileForm,
    EmploymentRecordForm, InternshipForm, PlacementForm, SalaryQueryForm,
    SalaryRecordForm, SkillForm, StudentProfileForm, UserRegistrationForm
)
from .models import (
    Certification, Company, EducationRecord, EmployeeProfile, EmploymentRecord,
    Internship, Placement, Role, SalaryQuery, SalaryRecord, Skill, StudentProfile,
    VerificationIssue
)
from .services import dashboard_metrics, rebuild_verification_issues


def role_required(*roles):
    def decorator(view_func):
        @login_required
        def wrapped(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            profile = getattr(request.user, "profile", None)
            if profile and profile.role in roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied("You do not have permission to access this page.")
        return wrapped
    return decorator


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


def register(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Registration completed. Please log in.")
        return redirect("login")
    return render(request, "lifecycle/form.html", {"form": form, "title": "Register User"})


@login_required
def dashboard(request):
    metrics = dashboard_metrics()
    degree_stats = StudentProfile.objects.values("degree").annotate(total=Count("id")).order_by("degree")
    return render(request, "lifecycle/dashboard.html", {"metrics": metrics, "degree_stats": degree_stats})


@role_required(Role.ADMIN)
def run_verification(request):
    created = rebuild_verification_issues()
    messages.success(request, f"Verification completed. {len(created)} issues created.")
    return redirect("verification_issues")


def list_view(request, model, template_title, allow_roles):
    if not request.user.is_authenticated:
        return redirect("login")
    qs = model.objects.all()
    query = request.GET.get("q", "").strip()
    if query:
        if model in [Company]:
            qs = qs.filter(name__icontains=query)
        elif model in [StudentProfile, EmployeeProfile]:
            qs = qs.filter(full_name__icontains=query)
    return render(request, "lifecycle/list.html", {"items": qs[:50], "title": template_title, "model_name": model.__name__, "query": query, "allow_roles": allow_roles})


def crud_create(request, form_class, title, redirect_name, roles):
    return _form_view(request, form_class, None, title, redirect_name, roles)


def crud_update(request, form_class, model, pk, title, redirect_name, roles):
    obj = get_object_or_404(model, pk=pk)
    return _form_view(request, form_class, obj, title, redirect_name, roles)


@login_required
def _form_view(request, form_class, instance, title, redirect_name, roles):
    profile = getattr(request.user, "profile", None)
    if not (request.user.is_superuser or (profile and profile.role in roles)):
        raise PermissionDenied
    form = form_class(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        if hasattr(obj, "user") and not obj.pk:
            obj.user = request.user
        if hasattr(obj, "owner") and not obj.pk:
            obj.owner = request.user
        obj.save()
        form.save_m2m()
        messages.success(request, "Record saved successfully.")
        return redirect(redirect_name)
    return render(request, "lifecycle/form.html", {"form": form, "title": title})


@role_required(Role.ADMIN, Role.STUDENT)
def students(request):
    return list_view(request, StudentProfile, "Students", [Role.ADMIN, Role.STUDENT])


@role_required(Role.ADMIN, Role.COMPANY, Role.EMPLOYEE)
def employees(request):
    return list_view(request, EmployeeProfile, "Employees", [Role.ADMIN, Role.COMPANY, Role.EMPLOYEE])


@role_required(Role.ADMIN, Role.COMPANY)
def companies(request):
    return list_view(request, Company, "Companies", [Role.ADMIN, Role.COMPANY])


@role_required(Role.ADMIN, Role.COMPANY, Role.EMPLOYEE)
def salary_records(request):
    return list_view(request, SalaryRecord, "Salary Records", [Role.ADMIN, Role.COMPANY])


@role_required(Role.ADMIN, Role.EMPLOYEE)
def salary_queries(request):
    return list_view(request, SalaryQuery, "Salary Queries", [Role.ADMIN, Role.EMPLOYEE])


@role_required(Role.ADMIN)
def verification_issues(request):
    return list_view(request, VerificationIssue, "Verification Issues", [Role.ADMIN])


@login_required
def resume(request):
    return render(request, "lifecycle/resume.html")


def reports_api(request):
    return JsonResponse(dashboard_metrics())


def salary_api(request, pk):
    record = get_object_or_404(SalaryRecord, pk=pk)
    return JsonResponse({
        "employee": record.employee.full_name,
        "company": record.company.name,
        "month": record.month,
        "year": record.year,
        "expected_salary": str(record.expected_salary),
        "paid_salary": str(record.paid_salary),
        "has_mismatch": record.has_mismatch,
    })


student_create = role_required(Role.ADMIN, Role.STUDENT)(lambda request: crud_create(request, StudentProfileForm, "Student Profile", "students", [Role.ADMIN, Role.STUDENT]))
student_update = role_required(Role.ADMIN, Role.STUDENT)(lambda request, pk: crud_update(request, StudentProfileForm, StudentProfile, pk, "Edit Student", "students", [Role.ADMIN, Role.STUDENT]))
employee_create = role_required(Role.ADMIN, Role.COMPANY, Role.EMPLOYEE)(lambda request: crud_create(request, EmployeeProfileForm, "Employee Profile", "employees", [Role.ADMIN, Role.COMPANY, Role.EMPLOYEE]))
employee_update = role_required(Role.ADMIN, Role.COMPANY, Role.EMPLOYEE)(lambda request, pk: crud_update(request, EmployeeProfileForm, EmployeeProfile, pk, "Edit Employee", "employees", [Role.ADMIN, Role.COMPANY, Role.EMPLOYEE]))
company_create = role_required(Role.ADMIN, Role.COMPANY)(lambda request: crud_create(request, CompanyForm, "Company", "companies", [Role.ADMIN, Role.COMPANY]))
salary_create = role_required(Role.ADMIN, Role.COMPANY)(lambda request: crud_create(request, SalaryRecordForm, "Salary Record", "salary_records", [Role.ADMIN, Role.COMPANY]))
query_create = role_required(Role.ADMIN, Role.EMPLOYEE)(lambda request: crud_create(request, SalaryQueryForm, "Salary Query", "salary_queries", [Role.ADMIN, Role.EMPLOYEE]))
education_create = role_required(Role.ADMIN, Role.STUDENT)(lambda request: crud_create(request, EducationRecordForm, "Education Record", "students", [Role.ADMIN, Role.STUDENT]))
skill_create = role_required(Role.ADMIN, Role.STUDENT)(lambda request: crud_create(request, SkillForm, "Skill", "students", [Role.ADMIN, Role.STUDENT]))
certification_create = role_required(Role.ADMIN, Role.STUDENT)(lambda request: crud_create(request, CertificationForm, "Certification", "students", [Role.ADMIN, Role.STUDENT]))
internship_create = role_required(Role.ADMIN, Role.STUDENT)(lambda request: crud_create(request, InternshipForm, "Internship", "students", [Role.ADMIN, Role.STUDENT]))
placement_create = role_required(Role.ADMIN, Role.STUDENT)(lambda request: crud_create(request, PlacementForm, "Placement", "students", [Role.ADMIN, Role.STUDENT]))
employment_create = role_required(Role.ADMIN, Role.COMPANY)(lambda request: crud_create(request, EmploymentRecordForm, "Employment Record", "employees", [Role.ADMIN, Role.COMPANY]))
