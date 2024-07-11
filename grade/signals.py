from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Language

@receiver(post_migrate, sender='grade')
def create_default_languages(sender, **kwargs):
    if not Language.objects.exists():
        Language.objects.create(name='Inglés', code='EN', iso='en', enabled=True)
        Language.objects.create(name='Español', code='ES', iso='es', enabled=True)
