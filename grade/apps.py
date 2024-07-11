from django.apps import AppConfig

class GradeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'grade'

    def ready(self):
        import grade.signals
