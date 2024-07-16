from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def tailwind_demo(request):
    return render(request, 'base.html')