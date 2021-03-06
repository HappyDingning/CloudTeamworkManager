import re
from django.forms import ModelForm, ValidationError
from django.contrib.auth.models import User
from django import forms
from .models import task as models_task
from .models import comment as models_comment

class task(ModelForm):

    class Meta:
        model = models_task
        exclude = ("creator", "publish_data", "task_schedule", "task_progress", "all_members")

    def __init__(self, *args, **kwargs):
        super(task, self).__init__(*args, **kwargs)
        self.fields["deadline"].required = False
        self.fields["members"].required = False
        self.fields["task_description"].required = False
        self.fields["task_need"].required = False
        self.fields["appendixes"].required = False
        self.fields["leaders"].required = False

class comment(forms.Form):
    content = forms.CharField(max_length = 200)
