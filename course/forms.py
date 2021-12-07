from django.forms import ModelForm
from django import forms

from course.models import Class, Semester
from course.widgets import CustomDatePickerInput, CustomTimePickerInput

# Create the form class.

class ClassForm(ModelForm):
    
    class Meta:
        model = Class
        exclude = ['enrolled_by','start_date','end_date','start_time','end_time', 'semester', 'cancelled']
