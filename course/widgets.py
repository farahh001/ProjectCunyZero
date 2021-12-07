from django.forms import DateInput

class CustomDatePickerInput(DateInput):
    template_name = 'widgets/datepicker.html'

class CustomTimePickerInput(DateInput):
    template_name = 'widgets/timepicker.html'
