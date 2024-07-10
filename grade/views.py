from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Grade
from .forms import GradeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def grade_list(request):
    grades = Grade.objects.filter(assignment__teacher=request.user)
    return render(request, 'grade/grade_list.html', {'grades': grades})

@login_required
def grade_create(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.grader = request.user  # Assign the logged-in user (teacher) as the grader
            grade.save()
            return redirect('grade_list')
    else:
        form = GradeForm()
    return render(request, 'grade/grade_create.html', {'form': form})

@login_required
def grade_edit(request, pk):
    grade = get_object_or_404(Grade, pk=pk, user=request.user)
    if request.method == 'POST':
        form = GradeForm(request.POST, request.FILES, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('grade_list')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'grade/grade_edit.html', {'form': form, 'grade': grade})