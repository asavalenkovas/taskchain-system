from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.db.models import Case, When, Value, IntegerField, Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from .models import Task, Machine
from .forms import TaskChainCreateForm


@login_required
def machine_tasks(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)

    if not request.user.is_superuser:
        if not hasattr(request.user, "employeeprofile"):
            return HttpResponseForbidden("Profilis nerastas.")

        profile = request.user.employeeprofile

        if profile.role == "manager":
            pass
        elif profile.role == "operator" and profile.machine_id == machine.id:
            pass
        else:
            return HttpResponseForbidden("Negalite matyti siu uzduociu.")

    tasks = (
        Task.objects
        .filter(machine=machine)
        .filter(Q(depends_on__isnull=True) | Q(depends_on__status="completed"))
        .annotate(
            status_order=Case(
                When(status="in_progress", then=Value(1)),
                When(status="pending", then=Value(2)),
                When(status="completed", then=Value(3)),
                default=Value(99),
                output_field=IntegerField(),
            )
        )
        .order_by("status_order", "order", "due_date", "id")
    )

    can_view_dashboard = False
    if request.user.is_authenticated:
        if request.user.is_superuser:
            can_view_dashboard = True
        elif hasattr(request.user, "employeeprofile") and request.user.employeeprofile.role == "manager":
            can_view_dashboard = True

    return render(request, "machine_tasks.html", {
        "machine": machine,
        "tasks": tasks,
        "can_view_dashboard": can_view_dashboard,
    })


@require_POST
@login_required
def update_task_status(request, task_id, new_status):
    task = get_object_or_404(Task, id=task_id)

    if not request.user.is_superuser:
        if not hasattr(request.user, "employeeprofile"):
            return HttpResponseForbidden("Profilis nerastas.")

        profile = request.user.employeeprofile

        if profile.role == "manager":
            pass
        elif profile.role == "operator" and profile.machine_id == task.machine_id:
            pass
        else:
            return HttpResponseForbidden("Neturite teises keisti sios uzduoties.")

    allowed_transitions = {
        "pending": ["in_progress"],
        "in_progress": ["completed"],
        "completed": [],
    }

    if new_status not in allowed_transitions.get(task.status, []):
        return HttpResponseForbidden("Neteisingas statuso keitimas.")

    if task.depends_on and task.depends_on.status != "completed":
        return HttpResponseForbidden("Pirma reikia uzbaigti ankstesne uzduoti.")

    task.status = new_status
    task.save()

    if new_status == "completed":
        reorder_tasks_after_completion(task)

    return redirect("machine_tasks", machine_id=task.machine.id)


@login_required
def dashboard(request):
    if not request.user.is_superuser:
        if not hasattr(request.user, "employeeprofile"):
            return HttpResponseForbidden("Profilis nerastas.")

        if request.user.employeeprofile.role != "manager":
            return HttpResponseForbidden("Neturite teises matyti si puslapi.")

    machines = Machine.objects.filter(is_active=True)

    machine_data = []

    for machine in machines:
        tasks = Task.objects.filter(machine=machine)

        pending_count = tasks.filter(status="pending").count()
        in_progress_count = tasks.filter(status="in_progress").count()
        completed_count = tasks.filter(status="completed").count()
        overdue_count = tasks.filter(
            due_date__lt=timezone.now()
        ).exclude(status="completed").count()

        machine_data.append({
            "machine": machine,
            "pending_count": pending_count,
            "in_progress_count": in_progress_count,
            "completed_count": completed_count,
            "overdue_count": overdue_count,
            "total_count": tasks.count(),
        })

    return render(request, "dashboard.html", {
        "machine_data": machine_data,
    })


@login_required
def create_task(request):
    if not request.user.is_superuser:
        if not hasattr(request.user, "employeeprofile"):
            return HttpResponseForbidden("Profilis nerastas.")

        if request.user.employeeprofile.role != "manager":
            return HttpResponseForbidden("Neturite teises kurti uzduociu.")

    if request.method == "POST":
        form = TaskChainCreateForm(request.POST)

        if form.is_valid():
            machines = [
                form.cleaned_data.get("machine_1"),
                form.cleaned_data.get("machine_2"),
                form.cleaned_data.get("machine_3"),
                form.cleaned_data.get("machine_4"),
            ]
            machines = [machine for machine in machines if machine]

            with transaction.atomic():
                previous_task = None

                for index, machine in enumerate(machines, start=1):
                    task = Task.objects.create(
                        project=form.cleaned_data["project"],
                        machine=machine,
                        name=form.cleaned_data["name"],
                        description=form.cleaned_data["description"],
                        part_code=form.cleaned_data["part_code"],
                        quantity=form.cleaned_data["quantity"],
                        due_date=form.cleaned_data["due_date"],
                        priority=form.cleaned_data["priority"],
                        order=index,
                        status="pending",
                        depends_on=previous_task,
                    )
                    previous_task = task

            return redirect("dashboard")
    else:
        form = TaskChainCreateForm()

    return render(request, "task_create.html", {"form": form})


def reorder_tasks_after_completion(completed_task):
    if not completed_task.machine:
        return

    tasks = Task.objects.filter(machine=completed_task.machine).order_by("order", "due_date", "id")

    new_order = 1

    for task in tasks:
        if task.id == completed_task.id:
            continue

        if task.status != "completed":
            if task.order != new_order:
                task.order = new_order
                task.save(update_fields=["order"])
            new_order += 1

    if completed_task.order != new_order:
        completed_task.order = new_order
        completed_task.save(update_fields=["order"])


def set_language(request):
    lang = request.GET.get("lang", "lt")

    if lang in ["lt", "en"]:
        request.session["lang"] = lang

    return redirect(request.META.get("HTTP_REFERER", "/"))