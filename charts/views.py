from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from tasks.models import Task, Address

from .models import Chart


# from .sms import *


class ChartListView(PermissionRequiredMixin, generic.ListView):
    model = Chart
    # paginate_by = 5
    template_name = 'charts/chart_list.html'
    permission_required = 'chart.can_mark_returned'

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super(ChartListView, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], 15)
        page = self.request.GET.get('page')

        try:
            context['object_list'] = paginator.page(page)
        except PageNotAnInteger:
            context['object_list'] = paginator.page(1)
        except EmptyPage:
            context['object_list'] = paginator.page(paginator.num_pages)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return render(request, 'charts/chart_list.html', context)


class ChartDetailView(PermissionRequiredMixin, generic.DetailView):
    """Generic class-based detail view for a task."""
    permission_required = 'chart.can_mark_returned'
    model = Chart
    # paginate_by = 2


# Classes created for the forms challenge
class ChartCreate(PermissionRequiredMixin, CreateView):
    model = Chart
    # template_name = "tasks/task_form.html"
    # fields = '__all__'
    permission_required = 'chart.can_mark_returned'


class ChartUpdate(PermissionRequiredMixin, UpdateView):
    model = Chart
    # fields = '__all__'
    # success_url = reverse_lazy('task_update')
    permission_required = 'chart.can_mark_returned'


class ChartDelete(PermissionRequiredMixin, DeleteView):
    model = Chart
    success_url = reverse_lazy('chart-list')
    permission_required = 'chart.can_mark_returned'

@csrf_exempt
def return_count_adr(request):
    return_dict = dict()
    id_adr = set()
    id_adr_two = set()
    data = request.POST
    print(data)
    adr = data.get("adr")
    count_adr = Chart.objects.all()
    count_adr = count_adr.filter(address_id=adr)
    task_adr = Task.objects.all()
    task_close = task_adr.exclude(status_task__icontains='выполнена')
    # task_adr = task_close.filter(address=adr)
    task_adr = task_close.filter(address_id=adr)
    count_task_adr = task_adr.count()
    # print(count_task_adr)

    for x in count_adr:
        if x.start_time:
            adr_query = count_adr.filter(
                start_time__range=(
                    x.start_time - timezone.timedelta(days=3), timezone.now() + timezone.timedelta(days=2)))
            for y in adr_query:
                if y.stop_time:
                    adr_query_new = adr_query.filter(stop_time__range=(
                        timezone.now() - timezone.timedelta(days=2), y.stop_time + timezone.timedelta(days=3)))
                    for z in adr_query_new:
                        id_adr_two.add(z)
                        # print(z)
                else:
                    adr_query_new = adr_query.filter(start_time__range=(
                        timezone.now() - timezone.timedelta(days=2), y.start_time + timezone.timedelta(days=3)))
                    for z in adr_query_new:
                        id_adr_two.add(z)
    str_info = ""
    if count_task_adr:
        str_info += "по дому заявок " + str(count_task_adr) + "</br>"
    if task_adr:
        str_info += "от кв. "
    mn_apt = set()
    int_mn_apt = set()
    str_mn_apt = set()
    all_mn_apt = list()
    for apt in task_adr:
        mn_apt.add(apt.apartment)
        try:
            int_mn_apt.add(int(apt.apartment))
        except:
            str_mn_apt.add(str(apt.apartment))
        all_mn_apt.append(apt.apartment)
    mn_apt = sorted(int_mn_apt) + sorted(str_mn_apt)
    # mn_apt = sorted(map(str, list(filter(None.__ne__, mn_apt))))

    def cnt_apt(apt):
        cnt_str = ''
        cnt = all_mn_apt.count(str(apt))
        if cnt > 1:
            cnt_str = ' (' + str(cnt) + ' обр.)'
        return cnt_str

    for i, apt in enumerate(mn_apt):
        print(apt)
        if apt != 'None':
            cnt = cnt_apt(apt)
            if len(mn_apt) == (i + 1):
                str_info += str(apt) + cnt
            else:
                str_info += str(apt) + cnt + ", "


    for x in id_adr_two:
        if x.address:
            str_info += "</br>" + str(x.address) + "</br>"
        if x.act:
            str_info += " " + str(x.act) + ""
        if x.resource:
            str_info += " " + str(x.resource) + ""
        if x.start_time:
            str_info += " с " + str(timezone.make_naive(x.start_time).strftime('%d.%m.%y %H:%M')) + ""
        if x.stop_time:
            str_info += " по " + str(timezone.make_naive(x.stop_time).strftime('%d.%m.%y %H:%M')) + ""
        if x.description:
            str_info += " " + x.description + "</br></br>"
        else:
            str_info += "</br>"
    if count_task_adr > 5:
        return_dict["str_comment"] = str_info.replace('</br>', '\n')
    return_dict["str_info"] = str_info
    return JsonResponse(return_dict)

@csrf_exempt
def return_adr_reu(request):
    return_dict = dict()
    data = request.POST
    adr_reu = data.get("adr_reu")
    task_adr = Address.objects.all()
    task_active = task_adr.exclude(is_active=False)
    adr_reu = task_active.filter(string_address=adr_reu)
    str_reu = ""
    for x in adr_reu:
        if x.string_subdivision:
            str_reu += str(x.string_subdivision)
    return_dict["adr_reu"] = str_reu
    return JsonResponse(return_dict)
