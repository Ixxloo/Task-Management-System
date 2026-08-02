from django import forms
from .models import Task
from django.utils import timezone

#Here only the shape , validating inputs
#create
class TaskForm (forms.ModelForm):
    class Meta ():
        model=Task #this checks for very variable if it valid or not
        fields='__all__'

    def clean_dueDate(self):
        dueDate = self.cleaned_data['dueDate']      #review this later 
        if dueDate < timezone.now().date():
            raise forms.ValidationError("Due date can't be in the past")
        return dueDate