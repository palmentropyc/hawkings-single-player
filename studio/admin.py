from django.contrib import admin
from .models import Course, Subject

class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1  # Número de líneas extra para agregar asignaturas desde el curso

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    inlines = [SubjectInline]

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')

admin.site.register(Course, CourseAdmin)
admin.site.register(Subject, SubjectAdmin)
