from django.db import models

# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnails/')
    
    def get_thumbnail(self):
        try:
            return self.thumbnail.url
        except:
            return ''