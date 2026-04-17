from django import forms
from .models import Project, Machine, Task


class TaskChainCreateForm(forms.Form):
    project = forms.ModelChoiceField(
        queryset=Project.objects.filter(is_active=True),
        label="Projektas",
        empty_label="Pasirinkite projekta"
    )

    name = forms.CharField(
        max_length=100,
        label="Pozicija"
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        label="Aprasymas"
    )

    part_code = forms.CharField(
        max_length=100,
        required=False,
        label="Kodas"
    )

    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Kiekis"
    )

    due_date = forms.DateTimeField(
        label="Terminas",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    priority = forms.ChoiceField(
        choices=Task.PRIORITY_CHOICES,
        initial="medium",
        label="Prioritetas"
    )

    machine_1 = forms.ModelChoiceField(
        queryset=Machine.objects.filter(is_active=True),
        label="1 etapas",
        required=True,
        empty_label="Pasirinkite darbo vieta"
    )

    machine_2 = forms.ModelChoiceField(
        queryset=Machine.objects.filter(is_active=True),
        label="2 etapas",
        required=False,
        empty_label="Pasirinkite darbo vieta"
    )

    machine_3 = forms.ModelChoiceField(
        queryset=Machine.objects.filter(is_active=True),
        label="3 etapas",
        required=False,
        empty_label="Pasirinkite darbo vieta"
    )

    machine_4 = forms.ModelChoiceField(
        queryset=Machine.objects.filter(is_active=True),
        label="4 etapas",
        required=False,
        empty_label="Pasirinkite darbo vieta"
    )

    def clean(self):
        cleaned_data = super().clean()

        machines = [
            cleaned_data.get("machine_1"),
            cleaned_data.get("machine_2"),
            cleaned_data.get("machine_3"),
            cleaned_data.get("machine_4"),
        ]

        selected = [machine for machine in machines if machine]

        if len(selected) != len(set(selected)):
            raise forms.ValidationError("Ta pati darbo vieta negali buti parinkta du kartus.")

        return cleaned_data