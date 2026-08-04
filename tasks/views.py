from django.shortcuts import render, redirect, get_object_or_404
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
    reads = Task.objects.all()
    return render(request, 'tas/index.html', {'tasks': reads})
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