from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def display_tasks(self):
        return self.tasks.count()

    display_tasks.short_description = "Uzduotys"


class Machine(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Laukia"),
        ("in_progress", "Vykdoma"),
        ("completed", "Uzbaigta"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Zemas"),
        ("medium", "Vidutinis"),
        ("high", "Aukstas"),
        ("critical", "Kritinis"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    machine = models.ForeignKey(
        Machine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    part_code = models.CharField(max_length=100, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    depends_on = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_tasks"
    )
    due_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium"
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["machine", "order", "due_date"]

    def __str__(self):
        machine_code = self.machine.code if self.machine else "NO-MACHINE"
        return f"{self.name} [{machine_code}]"

    def save(self, *args, **kwargs):
        from ledger.services import create_block

        is_new = self.pk is None
        old_status = None

        if not is_new:
            old_task = Task.objects.get(pk=self.pk)
            old_status = old_task.status

        super().save(*args, **kwargs)

        if is_new:
            create_block(
                event_type="TASK_CREATED",
                event_data={
                    "task_id": self.id,
                    "name": self.name,
                    "project_id": self.project_id,
                    "machine_id": self.machine_id,
                    "status": self.status,
                    "priority": self.priority,
                    "order": self.order,
                },
            )
            return

        if old_status != self.status:
            create_block(
                event_type="TASK_STATUS_CHANGED",
                event_data={
                    "task_id": self.id,
                    "name": self.name,
                    "project_id": self.project_id,
                    "old_status": old_status,
                    "new_status": self.status,
                },
            )