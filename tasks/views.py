import datetime
import logging
import time
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone, dateformat
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from docxtpl import DocxTemplate
from rest_framework import permissions, generics
from rest_framework.viewsets import ModelViewSet

# from commons.forms import UserCommentForm
from commons.models import Comment
from commons.utils import (TASK_SOURCE, TASK_STATUS, REU_CHOICE)
from tasks.permissions import IsOwnerOrReadOnly
from .eds_v10 import *
from .forms import FilterForm, TaskCommentForm, TaskForm
# from .models import Task, Category, Status
from .models import Task, Category
from .serializers import TaskSerializer, TaskInWorkSerializer, CommentSerializer, TaskInListViewInWorkSerializer


# from .sms import *
# from .telethon_test import telegramm


# @csrf_exempt
def return_tool(request):  # 54634
    return_dict = dict()
    data = request.POST
    home = data.get("home")
    apt = data.get("apt")
    y = Task.objects.all().filter(address=home, apartment=apt).first()
    if y:
        return_dict["porch"] = y.porch
        return_dict["floor"] = y.floor
        return_dict["phone"] = str(y.phone)
    return JsonResponse(return_dict)


def return_last_id(request):
    return_dict = dict()
    data = request.POST
    id = Task.objects.all().order_by('id').last().id
    if id:
        return_dict["id"] = id
    return JsonResponse(return_dict)


def return_deadline(request):
    return_dict = dict()
    data = request.POST
    id_category = data.get('id_category')
    if id_category:
        all_category = Category.objects.all()
        deadline_category = all_category.filter(id=id_category)
        now = datetime.now()
        for x in deadline_category:
            return_dict['deadline'] = str(dateformat.format((now + x.deadline), 'd.m.y H:i'))
            return_dict['id_category'] = id_category
            return_dict['name'] = x.name
            return_dict['id'] = x.id
        # print(return_dict)
    return JsonResponse(return_dict)


# @csrf_exempt
def return_count_tel(request):
    return_dict = dict()
    data = request.POST
    tel = data.get("tel")
    if (len(tel) < 10):
        return_dict["str_info"] = 'неверный формат номера (меньше 10 символов)'
        return JsonResponse(return_dict)
    all_count_tel = Task.objects.all()
    inwork_count_tel = all_count_tel.exclude(status_task__icontains='выполнена')
    count_tel = all_count_tel.filter(phone__icontains=tel)
    inwork_count_tel = inwork_count_tel.filter(phone__icontains=tel)

    str_info = ""
    for x in count_tel[:10]:
        str_info += str(x.phone)
        str_info += '<a href="/tasks/' + str(x.id) + "/view"'">' + " №" + str(x.id) + '</a>'
        str_info += " от " + str(timezone.make_naive(x.created_on).strftime('%d.%m.%y %H:%M'))
        if x.status_task:
            str_info += " " + '<b style="color:red">' + x.status_task + '</b>' + "</br>"
        if x.address:
            str_info += str(x.address) + " "
        if x.apartment:
            str_info += "кв. " + str(x.apartment) + " "
        if x.reu:
            str_info += "(" + x.reu + ")" + "</br>"
        if x.description:
            str_info += x.description + "</br>"
        if x.comment_status:
            str_info += x.comment_status + "</br></br>"
        else:
            str_info += "</br>"

    def get_reu(reu):
        str_reu = ""
        if reu:
            if reu == 'Аварийная служба':
                str_reu = '(АС)'
        return str_reu

    short_str_info = ''
    for i, x in enumerate(inwork_count_tel):
        str_reu = str(get_reu(x.reu))
        if i == len(inwork_count_tel) - 1:
            short_str_info += str(x.id) + str_reu
        else:
            short_str_info += str(x.id) + str_reu + ', '
    if short_str_info != '':
        short_str_info = 'не выполнено ' + short_str_info
    try:
        return_dict = run(tel)
    except:
        print('не вернулся словарь')
        pass
    if return_dict:
        str_info = return_dict['author'] + '<br><br>' + str_info
    return_dict["str_info"] = str_info
    return_dict["short_str_info"] = short_str_info
    return JsonResponse(return_dict)


def print_alarm_task(request, pk):
    ''' печать "НАПРАВЛЕНИЕ НА ЛИКВИДАЦИЮ АВАРИИ (НЕИСПРАВНОСТИ)" '''
    # locale.setlocale(locale.LC_ALL, 'ru_RU')
    dt = Task.objects.get(id=pk)
    doc = DocxTemplate("static/tmp_alarm_task.docx")
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=generated_doc.docx'
    address = ''
    description = ''
    dispetcher = ''
    short_dispetcher = ''
    person = ''
    executor = ''
    if dt.description:
        description += '. ' + dt.description
        description = description.replace('\n', '')
        description = description.replace('[', '')
        description = description.replace(']', '')
    if dt.address:
        address = str(dt.address)
    if dt.apartment:
        address += ', кв.' + dt.apartment
    if dt.porch:
        address += ', подъезд ' + str(dt.porch)
    if dt.floor:
        address += ', этаж ' + str(dt.floor)
    if dt.phone:
        person += str(dt.phone)
    if dt.surname_name:
        person += ' ' + str(dt.surname_name)
    if dt.first_name:
        person += ' ' + str(dt.first_name)
    if dt.patronymic_name:
        person += ' ' + str(dt.patronymic_name)
    if dt.author_eds:
        person += ' ' + str(dt.author_eds)
    if dt.executor:
        executor += ' ' + str(dt.executor)
    if dt.created_by:
        dispetcher = get_name(dt.created_by)[1]
        short_dispetcher = get_name(dt.created_by)[0]
    data = str(dateformat.format(timezone.make_naive(dt.created_on), '"d" E Y г. H час. i мин.'))
    # print(dateformat.format(datetime.now(), settings.DATE_FORMAT)) # USE_L10N = False
    context = {
        'data': data,
        'address': address,
        'description': description,
        'person': person,
        'task_id': pk,
        'dispetcher': dispetcher,
        'short_dispetcher': short_dispetcher,
        'executor': executor,
    }
    doc.render(context)
    doc.save(response)
    return response


def timer(func):
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        print('[*] Время выполнения: {} секунд.'.format(end - start))
        return return_value

    return wrapper


@login_required
@timer
def index(request):
    """
    Функция отображения домашней страницы сайта.
    Генерация "количеств" некоторых главных объектов
    """
    now = timezone.now()

    # @timer
    def count_dbl(query):
        dbl_description = query.filter(description__icontains='повтор')
        dbl_comment = query.filter(comment_status__icontains='повтор')
        cnt_dbl_description = dbl_description.count()
        cnt_dbl_comment = dbl_comment.count()
        cnt_dbl = cnt_dbl_description + cnt_dbl_comment
        # str(all_tasks_reu.count()) + count_dbl(all_tasks_reu)
        if cnt_dbl:
            # for n, v in enumerate((dbl_description.values('comment_status', 'description'))):
            #     print(n, v)
            cnt_dbl = str(query.count()) + '/' + str(cnt_dbl)
        else:
            cnt_dbl = str(query.count())
        return cnt_dbl

    all_tasks = Task.objects.all().only('status_task', 'created_on', 'reu', 'description', 'comment_status')
    # for task in all_tasks:
    #     in_work = task.
    #     print(task.status_task)
    # all_tasks = Task.objects.all()
    # all_tasks = Task.objects.filter(created_on__year=now.year, created_on__month=now.month)
    # all_tasks = Task.objects.filter(created_on__year=now.year)
    in_work = all_tasks.filter(status_task__icontains='в работе')
    dop_controll = all_tasks.filter(status_task__icontains='дополнительный контроль')
    completed = all_tasks.filter(status_task__iexact='выполнена')

    day_all_tasks = all_tasks.filter(created_on__date=now)
    day_in_work = in_work.filter(created_on__date=now)
    day_dop_controll = dop_controll.filter(created_on__date=now)
    day_completed = completed.filter(created_on__date=now)

    all_task = {}
    work = {}
    control = {}
    close = {}

    day_all_task = {}
    day_work = {}
    day_control = {}
    day_close = {}

    '''
    проход по РЭУ
    '''

    for key in dict(REU_CHOICE):
        print(key)
        all_tasks_reu = all_tasks.only('reu', 'created_on').filter(reu__icontains=key)
        in_work_reu = in_work.only('reu', 'created_on').filter(reu__icontains=key)
        dop_controll_reu = dop_controll.only('reu', 'created_on').filter(reu__icontains=key)
        completed_reu = completed.only('reu', 'created_on').filter(reu__icontains=key)

        if all_tasks_reu:
            all_task[key] = count_dbl(all_tasks_reu)
        if in_work_reu:
            work[key] = count_dbl(in_work_reu)
        if dop_controll_reu:
            control[key] = count_dbl(dop_controll_reu)
        if completed_reu:
            close[key] = count_dbl(completed_reu)

        all_tasks_reu_day = all_tasks_reu.filter(created_on__date=now)
        in_work_reu_day = in_work_reu.filter(created_on__date=now)
        dop_controll_reu_day = dop_controll_reu.filter(created_on__date=now)
        completed_reu_day = completed_reu.filter(created_on__date=now)

        if all_tasks_reu_day:
            day_all_task[key] = count_dbl(all_tasks_reu_day)
        if in_work_reu_day:
            day_work[key] = count_dbl(in_work_reu_day)
        if dop_controll_reu_day:
            day_control[key] = count_dbl(dop_controll_reu_day)
        if completed_reu_day:
            day_control[key] = count_dbl(completed_reu_day)

    # for key, value in enumerate(work(reu__icontains=key)):
    # reu: v for reu, v in [(reu, in_work(reu__icontains=reu).count(),)]
    # num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    # num_authors = Author.objects.count()  # Метод 'all()' применен по умолчанию.
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(request, 'index.html', context={'num_all_tasks': count_dbl(all_tasks),
                                                  'num_in_work': count_dbl(in_work),
                                                  'num_dop_controll': count_dbl(dop_controll),
                                                  'num_completed': count_dbl(completed),
                                                  'day_num_all_tasks': count_dbl(day_all_tasks),
                                                  'day_num_in_work': count_dbl(day_in_work),
                                                  'day_num_dop_controll': count_dbl(day_dop_controll),
                                                  'day_num_completed': count_dbl(day_completed),
                                                  # 'form': userform,
                                                  'all_task': all_task,
                                                  'work': work,
                                                  'control': control,
                                                  'close': close,
                                                  'day_all_task': day_all_task,
                                                  'day_work': day_work,
                                                  'day_control': day_control,
                                                  'day_close': day_close,
                                                  },
                  )


class TaskListView(PermissionRequiredMixin, generic.ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    permission_required = 'tasks.can_mark_returned'

    # paginate_by = 25

    def get_queryset(self):
        queryset = self.model.objects.all()
        request_post = self.request.POST
        if request_post:
            if request_post.get('home'):
                queryset = queryset.filter(address=request_post.get('home'))
            if request_post.get('reu'):
                queryset = queryset.filter(reu=request_post.get('reu'))
            if request_post.get('status_task'):
                queryset = queryset.filter(status_task=request_post.get('status_task'))
            if request_post.get('source_task'):
                queryset = queryset.filter(source_task=request_post.get('source_task'))
            if request_post.get('filter_time'):
                queryset = queryset.filter(created_on__date=request_post.get('filter_time'))
            if request_post.get('number_task').isdigit():
                queryset = queryset.filter(id=request_post.get('number_task'))
            if request_post.get('phone_task'):
                queryset = queryset.filter(phone__icontains=request_post.get('phone_task'))
            if request_post.get('checkbox_hide'):
                queryset = queryset.exclude(status_task__icontains='выполнена')
            if request_post.get('start_data'):
                queryset = queryset.filter(created_on__gte=request_post.get('start_data'))
            if request_post.get('end_data'):
                end_data = datetime.strptime(request_post.get('end_data'), '%Y-%m-%d') + timedelta(days=1)
                queryset = queryset.filter(created_on__lte=end_data)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super(TaskListView, self).get_context_data(**kwargs)
        context["reu"] = REU_CHOICE
        context["status_task"] = TASK_STATUS
        context["source_task"] = TASK_SOURCE
        context["phone_task"] = self.request.POST.get('phone_task')
        context["checkbox_hide"] = self.request.POST.get('checkbox_hide')
        paginator = Paginator(context['object_list'], 20)
        page = self.request.GET.get('page')
        context['form'] = FilterForm(self.request.POST)
        # context['form'].fields['filter_time'].widget.js_options['date'] = self.request.POST.get('filter_time')
        start_data = self.request.POST.get('start_data')
        end_data = self.request.POST.get('end_data')
        # print(self.request.POST.get('filter_time'))
        # print(start_data)
        # print(end_data)
        # print(context['form'].fields['start_data'].widget.js_options['date'])
        # print(context['form'].fields['end_data'].widget.js_options['date'])
        context['hidden_home'] = self.request.POST.get('home')
        if start_data and end_data:
            if start_data > end_data:
                context['errors'] = 'Дата начала периода должна быть меньше даты завершения периода.'
        number_task = self.request.POST.get('number_task')
        if number_task:
            if not number_task.isdigit():
                context['errors'] = 'Поле "Номер заявки" должно содержать целое число.'
        try:
            context['object_list'] = paginator.page(page)
        except PageNotAnInteger:
            context['object_list'] = paginator.page(1)
        except EmptyPage:
            context['object_list'] = paginator.page(paginator.num_pages)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, 'tasks/task_list.html', context)
        # return self.render_to_response(context)


# @method_decorator(csrf_exempt, name='dispatch')
class TaskDetailView(PermissionRequiredMixin, generic.DetailView):
    """Generic class-based detail view for a task."""
    permission_required = 'tasks.can_mark_returned'
    model = Task
    # paginate_by = 2
    context_object_name = "tasks"
    # print('context_object_name', context_object_name)
    template_name = "tasks/task_detail.html"

    # Task.objects.get(id=instance.id)
    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        task_obj = self.object
        tasks_data = []
        # for each in Task.objects.all():
        # for each in Task.objects.filter(id=task_obj.id):
        #     assigned_dict = {}
        #     assigned_dict['id'] = each.id
        #     # assigned_dict['name'] = each.username
        #     tasks_data.append(assigned_dict)
        #     # comments = task_obj.tasks_comments.all()
        #     comments = task_obj.tasks_comments.all()
        #     # print(each)
        Task.objects.get(id=task_obj.id)
        assigned_dict = {}
        assigned_dict['id'] = task_obj.id
        # assigned_dict['name'] = each.username
        tasks_data.append(assigned_dict)
        # comments = task_obj.tasks_comments.all()
        ''' related_name='tasks_comments' '''
        comments = task_obj.tasks_comments.all()
        # print(comments)
        for comment in comments:
            # print(get_name(comment.commented_by)[0])
            comment.created_by = get_name(comment.commented_by)
            # print(comment.created_by)
        # print(task_obj.tasks_comments.all())
        status_on = task_obj.tasks_comments.filter(status_task__isnull=False).count()
        # print(status_on)
        comment_on = task_obj.tasks_comments.exclude(comment='').count()
        # print(comment_on)
        context.update({
            "task_obj": task_obj,
            "status_on": status_on,
            "comment_on": comment_on,
            # "opportunity_list": Opportunity.objects.filter(assigned_to=task_obj.id),
            # "contacts": Contact.objects.filter(assigned_to=task_obj.id),
            # "cases": Case.objects.filter(assigned_to=task_obj.id),
            # "accounts": Account.objects.filter(assigned_to=task_obj.id),
            # "assigned_data": json.dumps(tasks_data),
            # "commented_by": get_name(comments.commented_by)[0]
            "comments": comments,
        })
        return context


def get_name(user):
    if user:
        # print(user.profile.short_name)
        # print(user.profile.full_name)
        # io = user.first_name.split(' ')
        # short_name = str(user.last_name + ' ' + io[0][:1] + '.' + io[1][:1] + '.')
        # full_name = str(user.last_name + ' ' + io[0] + ' ' + io[1])
        short_name = user.profile.short_name
        full_name = user.profile.full_name
        return short_name, full_name


# Classes created for the forms challenge

# @method_decorator(csrf_exempt, name='dispatch')
class TaskCreate(PermissionRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    # fields = '__all__'
    permission_required = 'tasks.can_mark_returned'

    # form_class = TaskForm
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        ''' если в запросе есть статус или комментарий то записать'''
        status = self.request.POST['status_task']
        comment = self.request.POST['comment_status']
        if status or comment:
            comment_form = TaskCommentForm(self.request.POST)
            comment_form = comment_form.save(commit=False)
            if status:
                comment_form.status_task = status
            if comment:
                comment_form.comment = comment
            comment_form.task = get_object_or_404(Task, id=form.instance.id)
            comment_form.commented_by = get_object_or_404(User, id=self.request.user.id)
            comment_form.save()
        return super(TaskCreate, self).form_valid(form)


# @method_decorator(csrf_exempt, name='dispatch')
class TaskUpdate(PermissionRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    # print('transsmition_time', dir( model.transmission_time))
    # print('transsmition_time', model.transmission_time)
    # fields = '__all__'
    # success_url = reverse_lazy('task_update')
    permission_required = 'tasks.can_mark_returned'

    # form_class = TaskForm
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        # print(get_name(user)[1], get_name(user)[0])
        pprint(form.instance.status_task)
        pprint(form.instance)
        task = form.instance
        if not task.tasks_comments.all():
            '''если нет комментариев при обновлении и есть старый комментарий
            то создаем новый со старыми данными'''
            comment_form = TaskCommentForm(self.request.POST)
            clone_first_comment(task, comment_form)
        return super(TaskUpdate, self).form_valid(form)


class TaskDelete(PermissionRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks_task:tasks-list')
    permission_required = 'tasks.can_mark_returned'


'''' api '''


# class TaskView(ReadOnlyModelViewSet):
class TaskView(ModelViewSet):
    queryset = Task.objects.all().exclude(status_task='выполнена')
    queryset = queryset.filter(status_task='в работе', reu='Аварийная служба')
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    serializer_class = TaskSerializer


class TaskApiView(generics.ListAPIView):
    queryset = Task.objects.all().exclude(status_task='выполнена')
    queryset = queryset.filter(status_task='в работе', reu='Аварийная служба')
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [
    #     permissions.IsAuthenticated
    # ]
    serializer_class = TaskInListViewInWorkSerializer


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskInWorkSerializer


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class TaskApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


''' http://garmoncheg.blogspot.com/2013/11/ajax-form-in-django-with-jqueryform.html '''
'''  https://medium.com/@01701414/how-to-apply-ajax-with-django-2-1-8e9a4943f73 '''


# def clone_first_comment(task, comment_form):
#     comment_form = comment_form.save(commit=False)
#     if task.status_task:
#         comment_form.status_task = task.status_task
#     if task.comment_status:
#         comment_form.comment = task.comment_status
#     if task.status_time:
#         comment_form.status_time = task.status_time
#     else:
#         comment_form.status_time = task.created_on
#     comment_form.commented_by = task.created_by
#     comment_form.task = task
#     comment_form.save()

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


def clone_first(task):
    comment_form = TaskCommentForm()
    comment_form = comment_form.save(commit=False)
    print(task)
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


def clone_first_comment_all(request):
    tasks = Task.objects.all()
    for task in tasks:
        clone_first(task)


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

    # def form_valid(self, form):
    #     comment = form.save(commit=False)
    #     comment.commented_by = self.request.user
    #     print(comment.commented_by)
    #     print(dir(comment))
    #     comment.task = self.task
    #     # comment.task = comment.comment
    #     # comment.comment_status = self.comment_status
    #     comment.save()
    #     comment_id = comment.id
    #     # current_site = get_current_site(self.request)
    #     # send_email_user_mentions.delay(comment_id, 'accounts', domain=current_site.domain,
    #     #     protocol=self.request.scheme)
    #
    #     return JsonResponse({
    #         "comment_id": comment.id,
    #         # "comment": comment.comment,
    #         # "commented_on": comment.commented_on,
    #         # "commented_on_arrow": comment.commented_on_arrow,
    #         # "commented_by": comment.commented_by.email
    #     })
    #
    # def form_invalid(self, form):
    #     return JsonResponse({"error": form['comment'].errors})


# class UpdateCommentView(LoginRequiredMixin, View):
#     http_method_names = ["post"]
#
#     def post(self, request, *args, **kwargs):
#         self.comment_obj = get_object_or_404(
#             Comment, id=request.POST.get("commentid"))
#         if request.user == self.comment_obj.commented_by:
#             form = TaskCommentForm(request.POST, instance=self.comment_obj)
#             if form.is_valid():
#                 return self.form_valid(form)
#
#             return self.form_invalid(form)
#
#         data = {'error': "You don't have permission to edit this comment."}
#         return JsonResponse(data)
#
#     def form_valid(self, form):
#         self.comment_obj.comment = form.cleaned_data.get("comment")
#         self.comment_obj.save(update_fields=["comment"])
#         comment_id = self.comment_obj.id
#         current_site = get_current_site(self.request)
#         # send_email_user_mentions.delay(comment_id, 'accounts', domain=current_site.domain, protocol=self.request.scheme)
#         return JsonResponse({
#             "comment_id": self.comment_obj.id,
#             "comment": self.comment_obj.comment,
#         })
#
#     def form_invalid(self, form):
#         return JsonResponse({"error": form['comment'].errors})


# class DeleteCommentView(LoginRequiredMixin, View):
#
#     def post(self, request, *args, **kwargs):
#         self.object = get_object_or_404(
#             Comment, id=request.POST.get("comment_id"))
#         if request.user == self.object.commented_by:
#             self.object.delete()
#             data = {"cid": request.POST.get("comment_id")}
#             return JsonResponse(data)
#
#         data = {'error': "You don't have permission to delete this comment."}
#         return JsonResponse(data)


# logging.basicConfig(
#     level=logging.DEBUG,
#     filename="mylog.log",
#     format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
#     datefmt='%H:%M:%S',
# )


def message_str(task, **kwargs):
    def title():
        s = ''
        if task.id:
            s += '**Заявка** №' + str(task.id)
        return s

    def create_task():
        s = ''
        if task.created_on:
            s += ' от ' + str(dateformat.format(timezone.make_naive(task.created_on), 'd.m.y H:i'))
        return s

    def status_time():
        s = ''
        if task.status_time:
            s += str(dateformat.format(timezone.make_naive(task.status_time), ' d.m.y H:i'))
        return s

    def fio():
        s = ''
        if task.surname_name:
            s += ' ' + str(task.surname_name)
        if task.first_name:
            s += ' ' + str(task.first_name)
        if task.patronymic_name:
            s += ' ' + str(task.patronymic_name)
        if task.author_eds:
            s += ' ' + str(task.author_eds)
        return s

    def sourse():
        s = ''
        if task.source_task:
            s += '\n' + '**Инициатор:** ' + str(task.source_task) + fio()
        return s

    def adr():
        s = ''
        if task.address:
            s += '\n' + '**Адрес:** ' + str(task.address)
        if task.apartment:
            s += ', кв.' + str(task.apartment)
        if task.porch:
            s += ', п.' + str(task.porch)
        if task.floor:
            s += ', эт.' + str(task.floor)
        if task.phone:
            s += ', т. ' + str(task.phone)
        return s

    def executor():
        s = ''
        if task.reu:
            s += '\n' + '**Участок:** ' + str(task.reu)
        if task.executor:
            s += ', ' + str(task.executor)
        if task.transmission_time:
            s += ' в ' + str(dateformat.format(task.transmission_time, 'H:i'))
        return s

    def descr_comm():
        s = ''
        if task.description:
            s += '\n' + '**Содержание:** ' + str(task.description)
        if task.comment_status:
            s += '\n' + '**Комментарий:** ' + str(task.comment_status)
        return s

    str_msg = ''
    """ если новая заявка 'Заявка №15454 новая  от 12.05.21 14:20' """
    """ если старая заявка 'Заявка №15206 от 05.05.21 17:47 выполнена 13.05.21 10:11' """
    if kwargs['created'] == True:
        str_msg += title() + ' **новая** ' + create_task()
    else:
        if task.status_task:
            str_msg += title() + create_task() + ' **' + str(task.status_task) + '**' + status_time()

    str_msg += sourse()
    str_msg += adr()
    str_msg += executor()
    str_msg += descr_comm()

    reu = task.reu
    return str_msg, reu


def sms_tel(instance, **kwargs):
    task = instance
    if task.sms_is_sended is not True \
            and task.sms_is_active \
            and task.phone and task.reu == 'Аварийная служба' \
            and task.source_task == 'житель':
        print(task.reu)
        if task.status_task == 'выполнена':
            str_tel = str(task.phone)
            if str_tel[:5] == '+7496':
                print('городской')
                return
            if str_tel[:2] == '+7':
                print('сотовый')
                str_tel = str_tel.replace('+7', '8')
                print(str_tel)
                return str_tel


def timer_on(timeout):
    print('таймер запущен')
    for x in range(timeout // 60):
        time.sleep(60)
        if (x % 5) == 0:
            sec = str(timeout - x * 60)
            min = str(int(timeout // 60 - x))
            hour = str(int(timeout // 60 // 60 - x // 60))
            print('до отправки смс ' + sec + ' секунд ' + min + ' минут ' + hour + ' часов ')


def worry():
    now = datetime.now()
    # then = datetime(now.year, now.month, now.day + 1, 8)
    # then = datetime(now.year, now.month, now.day, now.hour, now.minute + 2)
    # print(now)
    then = datetime(now.year, now.month, now.day, 14, 50)
    delta = then - now  # от текущей секунды до пяти минут
    timeout = int(delta.seconds)
    # print('delta ', delta)
    # print('delta ', delta.seconds)
    # if int(delta.seconds) <= int('36000'):
    if timeout <= int('75600'):  # если меньше четырёх минут
        print(f'не беспокоить до {then}')
        return False, timeout
    else:
        print('отправить смс немедленно')
        return True, timeout


# @receiver(pre_save, sender=Task)
# def pre_update_model(instance, sender, **kwargs):
#     print('pre', kwargs)
#     # print('pre', kwargs['created'])
#     # check if the updated fields exist and if you're not creating a new object
#     # print('username', dir(User))
#     # print('username', User.get_username())
#     pprint('')
#     # for i in User:
#     #     print(i)
#     if not kwargs['update_fields'] and instance.id:
#         # Save it so it can be used in post_save
#         # print(type(instance))
#         # instance.old = model_to_dict(Task.objects.get(id=instance.id))
#         instance.old_model = instance
#         instance.old = Task.objects.get(id=instance.id)
#         # instance.old_model = instance
#         # pprint(instance.old)
#
#
# @receiver(post_save, sender=Task)
# def task_signal(instance, sender, **kwargs):
#     print('post', kwargs)
#     print('post', kwargs['created'])
#     str_msg, reu = message_str(instance, **kwargs)
#
#     # Add updated_fields, from old instance, so the method logic remains unchanged
#     if not kwargs['update_fields'] and hasattr(instance, 'old'):
#         # instance_current = model_to_dict(Task.objects.get(id=instance.id))
#         # print(type(instance))
#         instance_current = model_to_dict(instance)
#         instance_old = model_to_dict(instance.old)
#         # pprint(instance_old)
#         pprint(instance_current)
#         # pprint(instance_current)
#         # pprint(instance_old)
#         instance_old_model = instance.old_model
#         # pprint(instance_current == instance_old)
#
#         # kwargs['update_fields'] = []
#
#         diffkeys = [key for key in instance_current if instance_current[key] != instance_old[key]]
#         for key in diffkeys:
#             print(key, ':', instance_old[key], '->', instance_current[key])
#             if key == 'updated_by':
#                 print('-->', get_name(instance_old_model.updated_by)[0])
#                 # for x in instance_old_model:
#                 #     print(x)
#             # kwargs['update_fields'].append(key)
#
#             # if key in kwargs['update_fields']:
#             #     print(dir(instance))
#             # print(f'изменился {key}')
#
#     def not_alarm_signal(task):
#         post_save.disconnect(task_signal, sender=Task)
#         task.save()
#         post_save.connect(task_signal, sender=Task)
#
#     def telegramm_function():
#         telegramm(str_msg, reu)
#
#     def set_queue(timeout):
#         task = instance
#         if task.sms_is_queue is not True:
#             print('ставим sms в очередь')
#             task.sms_is_queue = True
#             not_alarm_signal(task)
#             timer_on(timeout)
#         else:
#             print('sms уже в очереди')
#             return True
#
#     def sms_function():
#         str_tel = sms_tel(instance, **kwargs)
#         set_worry = ''
#         if str_tel:
#             set_worry, timeout = worry()
#             if set_worry is False:
#                 is_queue = set_queue(timeout)
#                 if is_queue is True:
#                     set_worry = False
#                 else:
#                     set_worry = True
#         # print(set_worry)
#         if str_tel and set_worry is True:
#             sms_dict = send_sms(str_tel, instance)
#             if sms_dict['responce'] == 200:
#                 if sms_dict['result'] == '':
#                     print('нет результата')
#                     sms_function()
#                 else:
#                     result = sms_dict['result']
#                     print(f'Статус отправки смс {result}', ' ', datetime.now())
#                     task = Task.objects.get(id=str(instance))
#                     if task.sms_is_sended is not True:
#                         task.sms_is_sended = True
#                         task.sms_result = sms_dict['result']
#
#                         not_alarm_signal(task)
#                     print('send sms Ok')
#             else:
#                 print('send sms Error')
#                 # sms_function()
#
#     pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     ''' sms telegramm on/off'''
#     asyncio.gather(
#         loop.run_in_executor(pool, sms_function),
#         loop.run_in_executor(pool, telegramm_function)
#     )


# data = str(dateformat.format(timezone.make_naive(x.created_on), '"d" E Y г. H час. i мин.'))
# for key, value in kwargs.items():
#     print(key, value)
""" https://stackoverflow.com/questions/54578488/django-signals-kwargsupdate-fields-is-always-none-on-model-update-via-djan/54579134#54579134 """
""" https://stackoverflow.com/questions/21925671/convert-django-model-object-to-dict-with-all-of-the-fields-intact """

logging.basicConfig(
    level=logging.DEBUG,
    filename="mylog.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)
