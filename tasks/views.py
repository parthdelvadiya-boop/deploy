from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import TaskForm
from .models import Task

def register_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,"Account created successfully.")
            return redirect("task_list")
    else:
        form = UserCreationForm()
    return render(request,"register.html",{"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")
    if request.method == "POST":
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("task_list")
    else:
        form = AuthenticationForm()
    return render(request,"login.html",{"form": form})


@login_required
def task_list(request):
    search = request.GET.get("search", "").strip()
    tasks = Task.objects.filter(user=request.user)

    if search:
        tasks = tasks.filter(title__icontains=search)

    return render(request,"task_list.html",{"tasks": tasks,"search": search,})


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request,"Task created successfully.")
            return redirect("task_list")

    else:
        form = TaskForm()

    return render(
        request,"task_form.html",{"form": form,"page_title": "Create Task","button_text": "Create Task",}
    )


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task,pk=pk,user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST,instance=task)

        if form.is_valid():
            form.save()
            messages.success(request,"Task updated successfully.")

            return redirect("task_list")

    else:
        form = TaskForm(instance=task)

    return render(request,"task_form.html",{"form": form,
            "page_title": "Update Task",
            "button_text": "Update Task",
        }
    )


@login_required
def task_delete(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        task.delete()

        messages.success(
            request,
            "Task deleted successfully."
        )

        return redirect("task_list")

    return render(
        request,
        "confirm_delete.html",
        {"task": task}
    )


@login_required
def task_complete(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
        user=request.user
    )

    task.status = "completed"

    task.save()

    messages.success(
        request,
        "Task marked as completed."
    )

    return redirect("task_list")