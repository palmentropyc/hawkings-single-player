from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from .models import Assignment, Student, Grade, Language
from .forms import AssignmentForm, StudentForm, GradeForm
from django.utils import timezone




class AssignmentListView(ListView):
    model = Assignment
    template_name = 'grade/assignment_list.html'
    context_object_name = 'assignments'

class AssignmentCreateView(CreateView):
    model = Assignment    
    form_class = AssignmentForm
    template_name = 'grade/assignment_form.html'
    success_url = reverse_lazy('assignment-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = Language.objects.all()
        return context


class AssignmentDetailView(DetailView):
    model = Assignment
    template_name = 'grade/assignment_detail.html'
    context_object_name = 'assignment'

class StudentListView(ListView):
    model = Student
    template_name = 'grade/student_list.html'
    context_object_name = 'students'



class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'grade/student_form.html'
    success_url = reverse_lazy('student-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class StudentDetailView(DetailView):
    model = Student
    template_name = 'grade/student_detail.html'
    context_object_name = 'student'

class GradeListView(ListView):
    model = Grade
    template_name = 'grade/grade_list.html'
    context_object_name = 'grades'

class GradeCreateView(CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'grade/grade_form.html'
    success_url = reverse_lazy('grade-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = Language.objects.all()
        context['assignments'] = Assignment.objects.all()
        context['students'] = Student.objects.all()
        context['current_datetime'] = timezone.now()
        return context




class GradeDetailView(DetailView):
    model = Grade
    template_name = 'grade/grade_detail.html'
    context_object_name = 'grade'

