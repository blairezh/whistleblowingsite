from django import forms
from login.models import Report

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Report
        fields=['userID','className', 'professorName', 'studentName', 'rating','workType','fileLink','status','feedback']