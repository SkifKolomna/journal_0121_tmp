from django import forms

from .models import Comment

class TaskCommentForm(forms.ModelForm):
    # comment = forms.CharField(max_length=255, required=True)
    # status_task = forms.ChoiceField(max_length=255, blank=True, null=True, choices=TASK_STATUS)

    class Meta:
        model = Comment
        fields = ('comment', 'task', 'id', 'status_task')
