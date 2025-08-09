from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import SkillProgress, UserProfile, Feedback, Question, Option, CareerPath, Skill, RecruiterProfile, JobPost


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name','age']

        widgets = {
        # 'gender': forms.Select(attrs={'class': 'form-select'}),

        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'age': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'education_level': forms.Select(attrs={'class': 'form-control'}),
            # 'current_status': forms.Select(attrs={'class': 'form-control'}),
            # 'location': forms.TextInput(attrs={'class': 'form-control'}),
    }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'gender', 'education_level', 'current_status', 'location']

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name','gender', 'education_level', 'current_status', 'location']

    def __init__(self, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True




class RecruiterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['name','company_name']



PROGRESS_CHOICES = [
    (10, "I'm new to this skill"),
    (40, 'I’ve done some tutorials'),
    (70, 'I’ve built small projects'),
    (100, 'I’ve mastered this skill'),
]

class SkillProgressForm(forms.ModelForm):
    progress = forms.ChoiceField(
        choices=PROGRESS_CHOICES,
        widget=forms.RadioSelect,
        label='How far have you learned this skill?'
    )

    class Meta:
        model = SkillProgress
        fields = ['progress']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your feedback here...'})
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter question text'}),
        }

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['question', 'text', 'career']
        widgets = {
            'question': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option text'}),
            'career': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(OptionForm, self).__init__(*args, **kwargs)
        self.fields['career'].queryset = CareerPath.objects.all()  # ✅ Important line
        self.fields['career'].empty_label = "Select a Career"


class CareerForm(forms.ModelForm):
    class Meta:
        model = CareerPath
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['career', 'name']
        widgets = {
            'career': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter skill name'}),
        }


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['career', 'title', 'description', 'location', 'qualifications']


class EditRecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['name','company_name', 'contact_email', 'phone']

    def __init__(self, *args, **kwargs):
        super(EditRecruiterProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['company_name'].widget.attrs['readonly'] = True

