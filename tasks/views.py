from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm

STATUS_LABELS = {'P': 'Pending', 'IN': 'In Progress', 'C': 'Completed'}

DEFAULT_CREATOR_USERNAME = 'maham'   # <-- change this to whichever username should always be "the creator"


def _is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def _get_default_creator():
    # Always returns the same fixed user, no matter who's browsing the site.
    return User.objects.filter(username=DEFAULT_CREATOR_USERNAME).first()


def Create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)      # build the Task object, don't save yet
            task.createdBy = _get_default_creator()   # always the same fixed user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tas/task_form.html', {'form': form})


def Read(request):
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '').strip()

    reads = Task.objects.all()

    if search_query:
        reads = reads.filter(title__icontains=search_query)

    if status_filter:
        reads = reads.filter(status=status_filter)

    paginator = Paginator(reads, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tasks': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
    }

    if _is_ajax(request):
        return render(request, 'tas/_task_table.html', context)

    return render(request, 'tas/index.html', context)


def Update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tas/task_form.html', {'form': form})


def Delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    return render(request, 'tas/task_confirm_delete.html', {'task': task})


def ToggleComplete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        completed = request.POST.get('completed') == 'true'
        task.status = 'C' if completed else 'P'
        task.save()

    if _is_ajax(request):
        return JsonResponse({
            'success': True,
            'pk': task.pk,
            'status_code': task.status,
            'status_label': STATUS_LABELS.get(task.status, task.status),
        })

    return redirect('task_list')