from django.db import models
from tinymce import models as tinymce_models

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
