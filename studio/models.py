from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

class YoutubeVideo(models.Model):
    title = models.CharField(max_length=200)
    video_id = models.CharField(max_length=20, unique=True)
    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES,
        default='es'  # O el idioma que prefieras como predeterminado
    )
    country = CountryField(null=True, blank=True)

    def __str__(self):
        return self.title