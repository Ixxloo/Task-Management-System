from django import forms
from .models import Task
from django.utils import timezone

# Here only the shape, validating inputs
# create
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task # this checks for every variable if it's valid or not
        exclude = ['createdBy']   # createdBy is set automatically from request.user, never shown to the user
        labels = {
            'title': 'Title',
            'assignedTo': 'Assigned To',
            'status': 'Status',
            'dueDate': 'Due Date',
            'description': 'Description',
        }
        widgets = {
            'dueDate': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_dueDate(self):
        dueDate = self.cleaned_data['dueDate']  # review this later
        if dueDate < timezone.now().date():
            raise forms.ValidationError("Due date can't be in the past")
        return dueDate
        from django import forms
from .models import Task
from django.utils import timezone

# Here only the shape, validating inputs
# create
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['createdBy']   # createdBy is set automatically from request.user, never shown to the user
        labels = {
            'title': 'Title',
            'assignedTo': 'Assigned To',
            'status': 'Status',
            'dueDate': 'Due Date',
            'description': 'Description',
        }
        widgets = {
            'dueDate': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_dueDate(self):
        dueDate = self.cleaned_data['dueDate']  # review this later
        if dueDate < timezone.now().date():
            raise forms.ValidationError("Due date can't be in the past")
        return dueDate