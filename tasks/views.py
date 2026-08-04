from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm

STATUS_LABELS = {'P': 'Pending', 'IN': 'In Progress', 'C': 'Completed'}

def Create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tas/task_form.html', {'form': form})
                                                    # here is for looping , if i want to reach the created data

def Read(request):
    status_filter = request.GET.get('status', '')   # reads ?status=P from the URL, defaults to '' (no filter)
    search_query = request.GET.get('q', '').strip()  # reads ?q=... from the URL, defaults to '' (no search)

    reads = Task.objects.all()

    if search_query:
        reads = reads.filter(title__icontains=search_query)

    if status_filter:
        reads = reads.filter(status=status_filter)

    paginator = Paginator(reads, 5)                  # split results into pages of 5 tasks each
    page_number = request.GET.get('page')            # reads ?page=2 from the URL
    page_obj = paginator.get_page(page_number)        # gives back only that page's tasks (safe against bad input)

    return render(request, 'tas/index.html', {
        'tasks': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
    })
                                                    # here is for looping , if i want to reach all data

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

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax:
        return JsonResponse({
            'success': True,
            'pk': task.pk,
            'status_code': task.status,
            'status_label': STATUS_LABELS.get(task.status, task.status),
        })

    return redirect('task_list')