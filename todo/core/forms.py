from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    title = forms.CharField(
        max_length=50,
        strip=True,
        error_messages={
            "required": "Task title cannot be empty.",
            "max_length": "Task title must be 50 characters or fewer.",
        },
    )

    class Meta:
        model = Task
        fields = ["title"]
