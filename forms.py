from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'email', 'course', 'grade']
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control quantra-input', 'placeholder': 'e.g. 2026-0001'}),
            'name': forms.TextInput(attrs={'class': 'form-control quantra-input', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control quantra-input', 'placeholder': 'student@school.edu'}),
            'course': forms.Select(attrs={'class': 'form-select quantra-input'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control quantra-input', 'step': '0.01', 'min': '0', 'max': '100', 'placeholder': '0.00 - 100.00'}),
        }
