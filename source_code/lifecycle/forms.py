from django import forms
from django.contrib.auth.models import User

from .models import (
    Certification, Company, EducationRecord, EmployeeProfile, EmploymentRecord,
    Internship, Placement, Profile, SalaryQuery, SalaryRecord, Skill, StudentProfile
)


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "form-check-input" if isinstance(field.widget, forms.CheckboxInput) else "form-control"
            field.widget.attrs.setdefault("class", css)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    role = forms.ChoiceField(choices=Profile._meta.get_field("role").choices, widget=forms.Select(attrs={"class": "form-control"}))
    mobile = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    demo_identity_number = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
        widgets = {name: forms.TextInput(attrs={"class": "form-control"}) for name in ["username", "first_name", "last_name", "email"]}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                role=self.cleaned_data["role"],
                mobile=self.cleaned_data["mobile"],
                demo_identity_number=self.cleaned_data["demo_identity_number"],
            )
        return user


class StudentProfileForm(BootstrapModelForm):
    class Meta:
        model = StudentProfile
        exclude = ["user", "is_verified"]


class EmployeeProfileForm(BootstrapModelForm):
    class Meta:
        model = EmployeeProfile
        exclude = ["user", "is_verified"]


class CompanyForm(BootstrapModelForm):
    class Meta:
        model = Company
        exclude = ["owner", "is_verified"]


class EducationRecordForm(BootstrapModelForm):
    class Meta:
        model = EducationRecord
        fields = "__all__"


class SkillForm(BootstrapModelForm):
    class Meta:
        model = Skill
        fields = "__all__"


class CertificationForm(BootstrapModelForm):
    class Meta:
        model = Certification
        fields = "__all__"
        widgets = {"issued_on": forms.DateInput(attrs={"type": "date", "class": "form-control"})}


class InternshipForm(BootstrapModelForm):
    class Meta:
        model = Internship
        fields = "__all__"
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


class PlacementForm(BootstrapModelForm):
    class Meta:
        model = Placement
        fields = "__all__"
        widgets = {"offer_date": forms.DateInput(attrs={"type": "date", "class": "form-control"})}


class EmploymentRecordForm(BootstrapModelForm):
    class Meta:
        model = EmploymentRecord
        fields = "__all__"
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


class SalaryRecordForm(BootstrapModelForm):
    class Meta:
        model = SalaryRecord
        fields = "__all__"


class SalaryQueryForm(BootstrapModelForm):
    class Meta:
        model = SalaryQuery
        fields = ["salary_record", "subject", "description"]
