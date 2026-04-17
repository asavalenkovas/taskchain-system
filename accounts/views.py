from django.contrib.auth.views import LoginView
from django.urls import reverse


class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser:
            return reverse("dashboard")

        if not hasattr(user, "employeeprofile"):
            return reverse("home")

        profile = user.employeeprofile

        if profile.role == "manager":
            return reverse("dashboard")

        if profile.role == "operator" and profile.machine:
            return reverse("machine_tasks", kwargs={"machine_id": profile.machine.id})

        return reverse("home")