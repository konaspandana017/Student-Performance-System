from django import forms
from analytics_app.models import Mark, Subject, Attendance
from django.contrib.auth.models import User


class AddMarksForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__role='Student'),
        label="Select Student",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'padding: 10px; border-radius: 10px; border: 2px solid #E8DCC8;'
        })
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        label="Select Subject",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'padding: 10px; border-radius: 10px; border: 2px solid #E8DCC8;'
        })
    )

    marks_obtained = forms.FloatField(
        label="Marks Obtained",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter marks (0-100)',
            'style': 'padding: 10px; border-radius: 10px; border: 2px solid #E8DCC8;',
            'min': '0',
            'max': '100',
            'step': '0.5'
        })
    )

    class Meta:
        model = Mark
        fields = ['student', 'subject', 'marks_obtained']


class SubjectForm(forms.ModelForm):
    name = forms.CharField(
        label="Subject Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter subject name (e.g., Data Structures)',
            'style': 'padding: 10px; border-radius: 10px; border: 2px solid #E8DCC8;'
        })
    )

    code = forms.CharField(
        label="Subject Code",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter code (e.g., CS101)',
            'style': 'padding: 10px; border-radius: 10px; border: 2px solid #E8DCC8;'
        })
    )

    class Meta:
        model = Subject
        fields = ['name', 'code']


class MarkAttendanceForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__role='Student'),
        label="Select Student",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'padding: 10px; border-radius: 10px; border: 2px solid #E8DCC8;'
        })
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        label="Select Subject",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'padding: 10px; border-radius: 10px; border: 2px solid #E8DCC8;'
        })
    )

    is_present = forms.BooleanField(
        label="Mark as Present",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'style': 'width: 20px; height: 20px; cursor: pointer;'
        })
    )

    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'is_present']