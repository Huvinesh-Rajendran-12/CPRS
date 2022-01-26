from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Student, StudentGroup, User, Client, Supervisor, Project
from django.contrib.auth.models import Group
from django.contrib.admin.widgets import FilteredSelectMultiple


class StudentSignUpForm(UserCreationForm):
    pass

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)

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
        client.client_type.add(*self.cleaned_data.get("client_type"))

        return user


class SupervisorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_supervisor = True
        if commit:
            user.save()
        return user


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["projecttitle", "projectoverview"]


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ["course_taken", "specialization", "area_of_interest"]


class GroupAdminForm(forms.ModelForm):
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


class StudentGroupAdminForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        required=True,
        widget=FilteredSelectMultiple("students", False),
    )

    class Meta:
        model = StudentGroup
        exclude = []
