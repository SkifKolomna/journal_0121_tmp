from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from tasks.models import Task
from .models import Comment

from .forms import UserCommentForm


# def add_comment(request):
#     print(request)
#     if request.method == "POST":
#         task = get_object_or_404(Task, id=request.POST.get('taskid'))
#         print(task)
#         form = UserCommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.created_by = request.user
#             comment.task = task
#             comment.save()
#             print('тут')
#             return JsonResponse({
#                 "comment_id": comment.id, "comment": comment.comment,
#                 "commented_on": comment.commented_on,
#                 "created_by": comment.created_by
#             })
#         return JsonResponse({"error": form.errors})


# def edit_comment(request, pk):
#     if request.method == "POST":
#         comment_obj = get_object_or_404(Comment, id=pk)
#         if request.user == comment_obj.commented_by:
#             form = UserCommentForm(request.POST, instance=comment_obj)
#             if form.is_valid():
#                 comment_obj.comment = form.cleaned_data.get("comment")
#                 comment_obj.save(update_fields=["comment"])
#                 return JsonResponse({
#                     "comment_id": comment_obj.id,
#                     "comment": comment_obj.comment,
#                 })
#             return JsonResponse({"error": form['comment'].errors})
#         data = {'error': "You don't have permission to edit this comment."}
#         return JsonResponse(data)
#
#
# def remove_comment(request):
#     if request.method == "POST":
#         comment_obj = get_object_or_404(
#             Comment, id=request.POST.get('comment_id'))
#         if request.user == comment_obj.commented_by:
#             comment_obj.delete()
#             data = {"cid": request.POST.get("comment_id")}
#             return JsonResponse(data)
#         data = {'error': "You don't have permission to delete this comment."}
#         return JsonResponse(data)
