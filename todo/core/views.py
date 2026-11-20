from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.http import HttpResponse, HttpResponseBadRequest
from .forms import TaskForm
from .models import Task
# Create your views here.

@login_required
def index_view(request):
    tasks = Task.objects.filter(user = request.user)
    
    context = {
        'title': 'Home',
        'tasks': tasks,
    }
    return render(request, 'index.html', context)

@login_required
@require_POST
def is_completed_view(request, task_id):
    task = get_object_or_404(Task, user=request.user, id=task_id)
    
    status = not task.status
    
    task.status = status
    
    task.save(update_fields=['status'])
    context = {
        'task': task
    }
    return render(request, 'tasks/task.html', context)


# Delete Task view

@login_required
@require_http_methods(['DELETE'])
def delete_view(request, task_id):

    task = get_object_or_404(Task, user = request.user, id = task_id)
    
    task.delete()
    
    response = HttpResponse(status=200)
    
    return response

@login_required
@require_POST
def add_task_view(request):
    form = TaskForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors["title"][0])

    task = form.save(commit=False)
    task.user = request.user
    task.save()
    return render(request, 'tasks/task.html', {'task': task})
    

@login_required
@require_POST
def update_view(request, task_id):
    task = get_object_or_404(Task, user=request.user, id=task_id)
    form = TaskForm(request.POST, instance=task)
    if not form.is_valid():
        return render(request, 'tasks/task.html', {'task': task, 'form': form})

    task = form.save()
    return render(request, 'tasks/task.html', {'task': task})
