import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from course.models import Class, Semester


# Create your models here.
ROLES = (
    ('ins', "Instructor"),
    ('std', "Student"),
)
    # GPA = models.FloatField(default=0.00)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(choices=ROLES, max_length=50)
    image = models.ImageField(upload_to='profile_pics/')
    suspended = models.BooleanField(default=False)
    GPA = models.FloatField(default=0.00)

    def __str__(self):
        return f"{self.user.username}-{self.role}-GPA:({self.get_gpa})"

    @property
    def get_image(self):
        try:
            return self.image.url
        except:
            return ''


    @property
    def get_current_classes(self):
        try:
            enrolled_classes = self.enrolled_classes.all()
            active_enrolled_classes = [_class for _class in enrolled_classes if _class.is_active]
            return active_enrolled_classes
        except:
            return []

    @property
    def is_special_registration(self):
        try:
            current_timestamp = datetime.datetime.now().timestamp()
            semesters = Semester.objects.filter(deactivated=False)
            active_semester = [semester for semester in semesters if semester.is_active]
            if active_semester:
                active_semester = active_semester[0]

            enrolled_classes = self.enrolled_classes.all()
            deactive_enrolled_classes = [_class for _class in enrolled_classes if not _class.is_active]

            special_period_timestamp = (active_semester.registration_period + datetime.timedelta(days=6)).timestamp()
            if deactive_enrolled_classes:
                if current_timestamp < special_period_timestamp:
                    return True
        except:
            return []



    @property
    def get_enroll_requests(self):
        requests = []
        classes = Class.objects.filter(instructor__id = self.id)
        print(classes)
        for _class in classes:
            for request in _class.enroll_requests.all():
                requests.append(request)
        return requests


    @property
    def get_gpa(self):
        try:
            total_gpa = 0
            final_gpa = 0
            # print(self.grades.all())
            for grade in self.grades.all():
                total_gpa += float(grade.GPA)
            total_grades_given = len(self.grades.all())
            if total_grades_given:
                final_gpa = total_gpa/total_grades_given
            # print(final_gpa)
            return round(final_gpa,2)
        except:
            return 0


    @property
    def get_warnings(self):
        try:
            warnings = self.warnings_revieved.filter(deactivated=False)
        except:
            warnings = []
        return warnings


    @property
    def get_assigned_classes(self):
        try:
            assigned_classes = self.assigned_classes.all()
            active_assigned_classes = [_class for _class in assigned_classes if _class.is_active]
            return active_assigned_classes
        except:
            return []

    @property
    def get_reviews(self):
        try:
            return self.reviews_given.all()
        except:
            return []

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()



class Application(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(choices=ROLES, max_length=50)
    document = models.FileField(upload_to='applications/', blank=False)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

class UserUniqueId(models.Model):
    uuid = models.CharField(max_length=500, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="unique_id", null=True, blank=True)
    expired = models.BooleanField(default=False)
