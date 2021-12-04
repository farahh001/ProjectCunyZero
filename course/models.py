from django.db import models
from tinymce import models as tinymce_models
from django.core.exceptions import ValidationError
import datetime

# Create your models here.



class Semester(models.Model):
    # classes = models.ManyToManyField("course.Class", related_name="semester")
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=False, blank=False)

    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=False, blank=False)
    setup_period = models.DateTimeField(auto_now=False, auto_now_add=False, null=False, blank=False)
    
    registration_period = models.DateTimeField(auto_now=False, auto_now_add=False, null=False, blank=False)
    running_period = models.DateTimeField(auto_now=False, auto_now_add=False, null=False, blank=False)
    grading_period = models.DateTimeField(auto_now=False, auto_now_add=False, null=False, blank=False)
    deactivated = models.BooleanField(default=False)

    def __str__(self):
        return f"Semester #{self.id} {self.is_active}"

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('End date should be greater than start date.')
        if self.setup_period > self.registration_period:
            raise ValidationError('Registration period should be greater than setup period.')
        elif self.registration_period > self.running_period:
            raise ValidationError('Running period should be greater than registration period.')
        elif self.running_period > self.grading_period:
            raise ValidationError('Grading period should be greater than Running period.')
        return True

    def get_status(self):
        current_timestamp = datetime.datetime.now().timestamp()

        if not self.is_active:
            return "Ended"
        
        if current_timestamp > self.start_date.timestamp() and current_timestamp < self.setup_period.timestamp():
            return "Setup"
        elif current_timestamp > self.setup_period.timestamp() and current_timestamp < self.registration_period.timestamp():
            return "Registration"
        elif current_timestamp > self.registration_period.timestamp() and current_timestamp < self.running_period.timestamp():
            return "Running"
        elif current_timestamp > self.running_period.timestamp() and current_timestamp < self.grading_period.timestamp():
            return "Grading"
        elif current_timestamp > self.grading_period.timestamp() and current_timestamp < self.end_date.timestamp():
            return "Grading_Ended"
        return None

    @property
    def get_classes(self):
        classes = self.classes.filter(cancelled=False)
        return classes

    @property
    def is_active(self):
        if not self.deactivated:
            if not datetime.datetime.now().timestamp() > self.end_date.timestamp():
                return True
        return False

    



class Class(models.Model):

    title = models.CharField(max_length=250)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True, default="default.jpg")
    instructions = tinymce_models.HTMLField(null=True, blank=True)
    quota = models.PositiveIntegerField(default=0)
    instructor = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE, related_name="assigned_classes", null=True, blank=True)
    enrolled_by = models.ManyToManyField("accounts.Profile", related_name="enrolled_classes", null=True, blank=True)
    completed_by = models.ManyToManyField("accounts.Profile", related_name="completed_classes", null=True, blank=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False, null=False, blank=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=False, blank=False)
    start_time = models.TimeField(auto_now=False, auto_now_add=False, null=False, blank=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False, null=False, blank=False)
    cancelled = models.BooleanField(default=False)
    rating = models.FloatField(default=0)

    @property
    def get_thumbnail(self):
        try:
            return self.thumbnail.url
        except:
            return ''





class Course(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnails/')

    def get_thumbnail(self):
        try:
            return self.thumbnail.url
        except:
            return ''

    @property
    def get_enroll_requests(self):
        requests = []
        classes = Class.objects.filter(instructor__id = self.id)
        print(classes)
        for _class in classes:
            for request in _class.enroll_requests.all():
                requests.append(request)
        return requests
