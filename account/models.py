from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
ROLES = (
    ('ins', "Instructor"),
    ('std', "Student"),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(choices=ROLES, max_length=50)
    image = models.ImageField(upload_to='profile_pics/')

    def get_image(self):
        try:
            return self.image.url
        except:
            return ''

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
