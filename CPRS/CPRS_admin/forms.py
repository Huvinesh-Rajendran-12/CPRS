from django import forms
from django.forms import ModelForm, modelformset_factory, ClearableFileInput
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import (
    Student,
    StudentGroup,
    User,
    Client,
    Supervisor,
    Project,
    Student_Profile,
    Client_Request,
)
from django.contrib.auth.models import Group
from django.contrib.admin.widgets import FilteredSelectMultiple
from dal import autocomplete


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    email = forms.EmailField(
        max_length=254,
        label="Email",
        help_text="Required. Inform a valid email address.",
    )
    student_no = forms.IntegerField(required=True, label="Student ID")

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.email = self.cleaned_data.get("email")
        user.save()
        student = Student.objects.create(
            user=user, name=user.first_name + " " + user.last_name
        )
        student.student_no = self.cleaned_data.get("student_no")
        student.save()
        return user


class ClientSignUpForm(UserCreationForm):

    CLIENT_TYPE_CHOICES = (
        (1, "University"),
        (2, "MLE"),
        (3, "Industry"),
    )

    client_type = forms.CharField(
        label="Select Client Type",
        widget=forms.Select(choices=CLIENT_TYPE_CHOICES),
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        user.save()
        client = Client.objects.create(user=user)
        client.client_type = self.cleaned_data.get("client_type")
        client.save()
        return user


class SupervisorSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, label="First Name", help_text="Optional."
    )
    last_name = forms.CharField(
        max_length=30, required=True, label="Last Name", help_text="Optional."
    )
    email = forms.EmailField(
        max_length=254,
        label="Email",
        help_text="Required. Inform a valid email address.",
    )

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_supervisor = True
        if commit:
            user.save()
        return user


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].required = False

    class Meta:
        model = Project
        exclude = ["id", "client", "is_assigned"]
        widgets = {"file": ClearableFileInput(attrs={"multiple": True})}


class StudentForm(ModelForm):
    class Meta:
        model = Student
        exclude = []


class GroupAdminForm(ModelForm):
    class Meta:
        model = Group
        exclude = []

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_student=True),
        required=False,
        widget=FilteredSelectMultiple("users", False),
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data["users"])

    def save(self, *args, **kwargs):
        instance = super(GroupAdminForm, self).save()
        self.save_m2m()
        return instance


class StudentProfileForm(ModelForm):
    class Meta:
        model = Student_Profile
        exclude = ["student","group"]


class EditStudetProfileForm(ModelForm):
    class Meta:
        model = Student_Profile
        exclude = ["student"]


class LoginForm(forms.Form):
    """user login form"""

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class ClientRequestForm(ModelForm):
    class Meta:
        model = Client_Request
        exclude = ["client", "group"]


class StudentGroupModelForm(ModelForm):
    class Meta:
        model = StudentGroup
        fields = ("name",)
        labels = {"name": "Group Name"}
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Group Name here"}
            )
        }


StudentFormset = modelformset_factory(
    Student,
    fields=("name",),
    extra=1,
    widgets={
        "name": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Student Number here"}
        )
    },
)
