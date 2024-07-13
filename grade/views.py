from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import AssignmentForm, GradeForm, StudentForm
from .models import Assignment, Grade, Language, Student
from .services import process_submission_with_ai  # Importa la función síncrona


@method_decorator(login_required, name='dispatch')
class AssignmentListView(ListView):
    model = Assignment
    template_name = 'grade/assignment_list.html'
    context_object_name = 'assignments'
    ordering = ['-id']  # Order by id in descending order

    def get_queryset(self):
        return Assignment.objects.filter(user=self.request.user).order_by('-id')



@method_decorator(login_required, name='dispatch')
class AssignmentCreateView(CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'grade/assignment_form.html'
    success_url = reverse_lazy('assignment-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



@method_decorator(login_required, name='dispatch')
class AssignmentDetailView(DetailView):
    model = Assignment
    template_name = 'grade/assignment_detail.html'
    context_object_name = 'assignment'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404  # or return a redirect to a not authorized page
        return obj



@method_decorator(login_required, name='dispatch')
class AssignmentUpdateView(UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'grade/assignment_detail.html'
    context_object_name = 'assignment'

    def get_success_url(self):
        return reverse_lazy('assignment-list')


@method_decorator(login_required, name='dispatch')
class StudentListView(ListView):
    model = Student
    template_name = 'grade/student_list.html'
    context_object_name = 'students'
    ordering = ['-id']  # Order by id in descending order

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user).order_by('-id')



@method_decorator(login_required, name='dispatch')
class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'grade/student_form.html'
    success_url = reverse_lazy('student-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class StudentDetailView(DetailView):
    model = Student
    template_name = 'grade/student_detail.html'
    context_object_name = 'student'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("You don't have permission to view this student.")
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'save_changes' in request.POST:
            self.object.name = request.POST.get('name')
            self.object.surname = request.POST.get('surname')
            self.object.email = request.POST.get('email')
            self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('student-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grades'] = self.object.grade_set.filter(user=self.request.user)
        return context


@method_decorator(login_required, name='dispatch')
class GradeListView(ListView):
    model = Grade
    template_name = 'grade/grade_list.html'
    context_object_name = 'grades'
    ordering = ['-id']  # Order by id in descending order

    def get_queryset(self):
        return Grade.objects.filter(user=self.request.user).order_by('-id')

@method_decorator(login_required, name='dispatch')
class GradeCreateView(CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'grade/grade_form.html'
    success_url = reverse_lazy('grade-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        if form.instance.local_path:
            process_submission_with_ai(form.instance.id)
        
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['languages'] = Language.objects.all()
        context['assignments'] = Assignment.objects.filter(user=self.request.user)
        context['students'] = Student.objects.filter(user=self.request.user)
        context['current_datetime'] = timezone.now()
        return context




@method_decorator(login_required, name='dispatch')
class GradeDetailView(DetailView):
    model = Grade
    template_name = 'grade/grade_detail.html'
    context_object_name = 'grade'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("You don't have permission to view this grade.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignments'] = Assignment.objects.filter(user=self.request.user)
        context['students'] = Student.objects.filter(user=self.request.user)
        return context 

    def post(self, request, *args, **kwargs):
        grade = self.get_object()
        if 'ask_ai_grade_again' in request.POST:
            process_submission_with_ai(grade.id)
            # Puedes añadir un mensaje de éxito o cualquier otra lógica aquí
        return self.get(request, *args, **kwargs)
