from django import forms
from .models import User, Test, Question

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    user_type = forms.ChoiceField(
        choices=[('regular', 'Regular User'), ('headhunter', 'Headhunter')],
        widget=forms.RadioSelect
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
        }

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name', 'description', 'duration']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control"}),
            'duration': forms.NumberInput(attrs={"class": "form-control"}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['content', 'question_type', 'options', 'correct_answer']
        widgets = {
            'content': forms.TextInput(attrs={"class": "form-control"}),
            'question_type': forms.Select(attrs={"class": "form-control"}),
            'options': forms.TextInput(attrs={"class": "form-control"}),
            'correct_answer': forms.TextInput(attrs={"class": "form-control"}),
        }
