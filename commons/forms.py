from django import forms

from .models import Comment


# class UserCommentForm(forms.ModelForm):
#     # comment_status = forms.CharField(max_length=64, required=True)
#     comment = forms.CharField(max_length=64, required=True)
#
#     class Meta:
#         model = Comment
#         # fields = ('comment', 'user', 'commented_by')
#         # fields = ('comment_status', 'task', 'created_by')
#         # fields = ('comment', 'comment_status', 'task', 'commented_by')
#         # fields = ('commented_by')
#         fields = ('comment',)
