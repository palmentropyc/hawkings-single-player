from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
import re
from bson import ObjectId

class YoutubeVideo(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    video_id = models.CharField(max_length=20, unique=True)
    language = models.CharField(max_length=10, default='en')
    country = CountryField(blank=True, null=True)
    transcript = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

    def clean(self):
        if self.url:
            video_id = self.extract_video_id(self.url)
            if video_id:
                self.video_id = video_id
            else:
                raise ValidationError('Invalid YouTube URL')

    @staticmethod
    def extract_video_id(url):
        pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(?:embed\/)?(?:v\/)?(?:shorts\/)?(?:live\/)?(?:@[\w.-]+\/)?(?:[\w-]{11})'
        match = re.search(pattern, url)
        if match:
            return match.group()[-11:]
        return None
    
class Course(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField()
    uuid = models.CharField(max_length=24, default=str(ObjectId()))
    country = CountryField(blank=False, null=False)
    def __str__(self):
        return f"{self.name} ({self.country.name})"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    description = models.TextField()
    content = models.TextField()  

    def __str__(self):
        return self.name