from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['full_name', 'email', 'feedback']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your feedback here...',
                'rows': 4
            }),
        }
