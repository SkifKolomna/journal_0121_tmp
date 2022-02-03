from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import dateformat, timezone

from tasks.models import Task
from .models import Comment

from .forms import TaskCommentForm


def update_comment(task):
    '''  получаем строку из всех комментов если они есть и записываем её в task.comment_status для отчётов '''
    task_comment_all = task.tasks_comments.exclude(comment='')
    comment = ''
    for task_comment in task_comment_all:
        print(task_comment)
        if task_comment.comment:
            comment += 'от ' + str(dateformat.format(timezone.make_naive(task_comment.commented_on),
                                                     'd.m.y H:i') + ' ' + task_comment.comment + '\r\n')
    task.comment_status = comment
    print(comment)

    '''  выбираем последний статус с датой и пишем выбранное в task.status_task task.status_time для отчётов '''
    last_status_task = task.tasks_comments.exclude(status_task__isnull=True).order_by('commented_on').last()
    if last_status_task:
        task.status_task = last_status_task.status_task
        task.status_time = last_status_task.commented_on
        print(last_status_task.status_task, last_status_task.commented_on)
    task.save()


def clone_first_comment(task, comment_form):
    comment_form = comment_form.save(commit=False)
    if task.status_task:
        comment_form.status_task = task.status_task
    if task.comment_status:
        comment_form.comment = task.comment_status
    comment_form.commented_by = task.created_by
    comment_form.task = task
    comment_form.save()
    if task.status_time:
        comment_form.status_time = task.status_time
        comment_form.commented_on = task.status_time
    else:
        comment_form.commented_on = task.created_on
    comment_form.save()
    update_comment(task)


# @csrf_exempt
def add_comment(request):
    if request.method == "POST":
        task = get_object_or_404(Task, id=request.POST.get('taskid'))
        form = TaskCommentForm(request.POST)
        if form.is_valid():
            if not task.tasks_comments.all():
                '''если нет коментариев при добавлении то клонируем старый'''
                comment_form = TaskCommentForm(request.POST)
                clone_first_comment(task, comment_form)
            comment = form.save(commit=False)
            if not comment.status_task and not comment.comment:
                form.errors['error'] = {'erorr': "Выберете статус или заполните комментарий."}
                return JsonResponse(form.errors)
            comment.commented_by = get_object_or_404(User, id=request.user.id)
            comment.task = task
            comment.save()

            update_comment(task)

            return JsonResponse({
                "task": comment.task.id,
                "status_task": comment.status_task,
                "comment_id": comment.id,
                "comment": comment.comment,
                "commented_on": comment.commented_on,
                "commented_by": get_name(comment.commented_by)[0],
            })
        return JsonResponse({"error": form.errors})


# @csrf_exempt
def edit_comment(request, pk):
    if request.method == "POST":
        comment_obj = get_object_or_404(Comment, id=pk)
        task = get_object_or_404(Task, id=comment_obj.task_id)
        print(comment_obj.task_id)
        print(comment_obj.task)
        if request.user == comment_obj.commented_by:
            form = TaskCommentForm(request.POST, instance=comment_obj)
            if form.is_valid():
                status_task = form.cleaned_data.get("status_task")
                comment = form.cleaned_data.get("comment")
                if not status_task and not comment:
                    data = {'error': "Выберете статус или заполните комментарий."}
                    return JsonResponse(data)
                comment_obj.comment = comment
                comment_obj.status_task = status_task
                comment_obj.save(update_fields=["comment", "status_task"])
                update_comment(task)
                return JsonResponse({
                    "comment_id": comment_obj.id,
                    "comment": comment_obj.comment,
                    "status_task": comment_obj.status_task,
                })
            return JsonResponse({"error": form['comment'].errors})
        data = {'error': "У вас нет разрешения на редактирование этого комментария."}
        return JsonResponse(data)


# @csrf_exempt
def remove_comment(request):
    if request.method == "POST":
        comment_obj = get_object_or_404(Comment, id=request.POST.get('comment_id'))
        task = get_object_or_404(Task, id=comment_obj.task_id)
        if request.user == comment_obj.commented_by:
            comment_obj.delete()
            data = {"cid": request.POST.get("comment_id")}
            print('--------------')
            update_comment(task)
            print('--------------')
            return JsonResponse(data)
        data = {'error': "У вас нет разрешения на удаление этого комментария."}
        return JsonResponse(data)