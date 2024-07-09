from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Assignment
from .forms import AssignmentForm




@login_required
def assignment_list(request):
    assignments = Assignment.objects.filter(user=request.user)
    return render(request, 'assignment/list.html', {'assignments': assignments})

@login_required
def assignment_create(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user
            assignment.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm()
    return render(request, 'assignment/create.html', {'form': form})

@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'assignment/detail.html', {'form': form, 'assignment': assignment})