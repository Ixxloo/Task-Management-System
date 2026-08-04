from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm

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

    reads = Task.objects.all()
    if status_filter:                                # only filter if the user actually picked something
        reads = reads.filter(status=status_filter)

    paginator = Paginator(reads, 5)                  # split results into pages of 5 tasks each
    page_number = request.GET.get('page')            # reads ?page=2 from the URL
    page_obj = paginator.get_page(page_number)        # gives back only that page's tasks (safe against bad input)

    return render(request, 'tas/index.html', {
        'tasks': page_obj,
        'status_filter': status_filter,
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


def MarkComplete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = 'C'
    task.save()

    # If this request came from our JavaScript fetch() call, respond with JSON
    # instead of redirecting, so the page doesn't reload.
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax:
        return JsonResponse({
            'success': True,
            'pk': task.pk,
            'status_code': task.status,
            'status_label': 'Completed',
        })

    # Fallback for non-JS / JS-disabled browsers: behave like before.
    return redirect('task_list')