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
    Supervisor_Profile,
    Project,
    Student_Profile,
    Client_Request,
    MLEClient,
    UniversityClient,
    IndustryClient,
    Task,
    StudentFeedback,
)
from django.contrib.auth.models import Group
from django.contrib.admin.widgets import FilteredSelectMultiple
from dal import autocomplete


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, label="First Name", help_text="Required"
    )
    last_name = forms.CharField(
        max_length=30, required=True, label="Last Name", help_text="Required"
    )
    email = forms.EmailField(
        max_length=254,
        label="Email",
        help_text="Required. Inform a valid email address.",
    )
    student_no = forms.IntegerField(required=True, label="Student ID")
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if "@sd.taylors.edu.my" not in data:
            raise forms.ValidationError("Must be a Taylor's Email")
        return data

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
    first_name = forms.CharField(
        max_length=30, required=True, label="First Name", help_text="Required"
    )
    last_name = forms.CharField(
        max_length=30, required=True, label="Last Name", help_text="Required"
    )
    email = forms.EmailField(
        max_length=254,
        label="Email",
        help_text="Required. Inform a valid email address.",
    )
    CLIENT_TYPE_CHOICES = (
        ("University", "University"),
        ("MLE", "MLE"),
        ("Industry", "Industry"),
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
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.email = self.cleaned_data.get("email")
        user.save()
        client = Client.objects.create(
            user=user, name=user.first_name + " " + user.last_name
        )
        client.client_type = self.cleaned_data.get("client_type")
        client.save()
        return user


class SupervisorSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, label="First Name", help_text="Required"
    )
    last_name = forms.CharField(
        max_length=30, required=True, label="Last Name", help_text="Required"
    )
    email = forms.EmailField(
        max_length=254,
        label="Email",
        help_text="Required. Inform a valid email address.",
    )
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if "@sd.taylors.edu.my" not in data:
            raise forms.ValidationError("Must be a Taylor's Email")
        return data

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.email = self.cleaned_data.get("email")
        user.is_supervisor = True
        user.save()
        supervisor = Supervisor.objects.create(
            user=user, name=user.first_name + " " + user.last_name
        )
        supervisor.save()
        return user


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].required = False

    class Meta:
        model = Project
        exclude = ["id", "client", "is_assigned", "status"]
        widgets = {"file": ClearableFileInput(attrs={"multiple": True})}


class EditProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].required = False

    class Meta:
        model = Project
        exclude = ["id", "client", "is_assigned"]
        widgets = {"file": ClearableFileInput(attrs={"multiple": True})}



class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["assigned_to"] = forms.ModelChoiceField(
            queryset=Student.objects.filter(group=self.request.user.student.group)
        )

    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "assigned_to"]

    @transaction.atomic
    def save(self, commit=True):
        task = super().save(commit=False)
        task.created_by = self.request.user.student
        task.project = self.request.user.student.group.project
        task.assigned_to = self.cleaned_data.get("assigned_to")
        task.group = self.request.user.student.profile.group
        task.save()
        return task


class UpdateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "assigned_to", "status"]


class StudentProfileForm(ModelForm):
    class Meta:
        model = Student_Profile
        exclude = ["student", "group"]


class SupervisorProfileForm(ModelForm):
    class Meta:
        model = Supervisor_Profile
        exclude = ["supervisor"]


class IndustryClientProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
    class Meta:
        model = IndustryClient
        exclude = ["client"]
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.client = self.request.user.client
        profile.save()
        return profile
    


class EditIndustryClientProfileForm(ModelForm):
    class Meta:
        model = IndustryClient
        exclude = ["client"]


class MLEClientProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
    class Meta:
        model = MLEClient
        exclude = ["client"]
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.client = self.request.user.client
        profile.save()
        return profile

class EditMLEClientProfileForm(ModelForm):
    class Meta:
        model = MLEClient
        exclude = ["client"]


class UniversityClientProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
    class Meta:
        model = UniversityClient
        exclude = ["client"]
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.client = self.request.user.client
        profile.save()
        return profile

class EditUniversityClientProfileForm(ModelForm):
    class Meta:
        model = UniversityClient
        exclude = ["client"]


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
        exclude = ["client", "group", "approval_status"]


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
            attrs={"class": "form-control", "placeholder": "Enter Student Name here"}
        )
    },
)


class AssignSupervisorForm(ModelForm):
    class Meta:
        model = StudentGroup
        fields = ["supervisor"]


class StudentFeedbackForm(ModelForm):
    class Meta:
        model = StudentFeedback
        fields = ["feedback"]


class StudentFeedbackReplyForm(ModelForm):
    class Meta:
        model = StudentFeedback
        fields = ["feedback_reply"]
