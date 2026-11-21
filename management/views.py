from django.shortcuts import get_object_or_404, redirect, render

from .forms import TaskForm
from .models import Task


def home(request):
    tasks = Task.objects.all()
    return render(request, "home.html", {"tasks": tasks})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "task_detail.html", {"task": task})


def task_create(request):
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        task = form.save()
        return redirect("task_detail", pk=task.pk)

    return render(request,"task_form.html",{"form": form, "page_title": "Create task", "submit_label": "Create task"},)


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("task_detail", pk=task.pk)

    return render(request,"task_form.html",{"form": form, "page_title": "Edit task", "submit_label": "Save changes"},)


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("home")

    return render(request, "task_confirm_delete.html", {"task": task})
