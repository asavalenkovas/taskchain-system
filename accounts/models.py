from django.contrib.auth.models import User
from django.db import models
from tasks.models import Machine


class EmployeeProfile(models.Model):
    ROLE_CHOICES = [
        ("operator", "Darbuotojas"),
        ("manager", "Vadovas"),
        ("other", "Kita"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="operator")
    machine = models.ForeignKey(
        Machine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="operators",
    )

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
