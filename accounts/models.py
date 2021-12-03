from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
