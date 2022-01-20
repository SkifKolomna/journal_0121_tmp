from django import forms
from django.utils.translation import ugettext as _
from django_select2.forms import (
    ModelSelect2Widget,
)
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

from commons.models import Comment
from commons.utils import TASK_STATUS
from . import models
# from .models import Task, Address, Category, Status
from .models import Task, Address, Category


class AddressCustomTitleWidget(ModelSelect2Widget):
    model = Address()
    queryset = models.Address.objects.all().filter(is_active=True)
    search_fields = ["string_address__icontains"]


class AddressCustomFilterWidget(ModelSelect2Widget):
    model = Address()
    queryset = models.Address.objects.all().filter(is_active=True)
    search_fields = ["string_address__icontains"]

    def get_context(self, name, value, attrs):
        context = super(AddressCustomFilterWidget, self).get_context(name, value, attrs)
        context["widget"]["attrs"]['data-placeholder'] = 'Дом'
        attrs_optgroups = context["widget"]["optgroups"][0][1][0]
        attrs_optgroups['value'] = list(context["widget"]["value"])[0]
        if attrs_optgroups['value']:
            label = models.Address.objects.all().filter(id=attrs_optgroups['value'])[0]
            attrs_optgroups['label'] = label
        return context

    # def __init__(self, *args, **kwargs):
    #     super(AddressCustomFilterWidget, self).__init__(*args, **kwargs)
    #     pprint(self)


class CategoryCustomTitleWidget(ModelSelect2Widget):
    model = Category()
    queryset = models.Category.objects.all().filter(visible=True)
    search_fields = ["name__icontains"]


class FilterForm(forms.Form):
    filter_time = forms.DateField(label=_("Время исполнения"), required=False,
                                  widget=DatePicker(options={'format': 'YYYY-MM-DD', },
                                                    attrs={'class': 'form-control datetimepicker-input',
                                                           'append': 'fa fa-calendar', }),
                                  )

    home = forms.ChoiceField(label=_("Дом"),
                             # widget=AddressCustomFilterWidget(attrs={'class': 'form-control'}), # полный список
                             widget=AddressCustomFilterWidget(attrs={'class': 'form-control'}),
                             required=False)

    # def __init__(self, *args, **kwargs):
    #     super(FilterForm, self).__init__(*args, **kwargs)


""" overcoder.net/q/844/измените-поле-формы-django-на-скрытое-поле """


class TaskCommentForm(forms.ModelForm):
    # comment = forms.CharField(max_length=255, required=True)
    # status_task = forms.ChoiceField(max_length=255, blank=True, null=True, choices=TASK_STATUS)

    class Meta:
        model = Comment
        fields = ('comment', 'task', 'id', 'status_task')



class TaskForm(forms.ModelForm):
    transmission_time = forms.TimeField(label=_("Время передачи"), required=False,
                                        widget=TimePicker(options={
                                            'format': 'LT',
                                            # 'format': 'HH:mm',
                                        },
                                            attrs={'class': 'form-control datetimepicker-input',
                                                   'append': 'fa fa-clock-o', }
                                        ),
                                        )

    status_time = forms.DateTimeField(label=_("Время исполнения"), required=False,
                                      widget=DateTimePicker(options={'format': 'L LT', },
                                                            attrs={'class': 'form-control datetimepicker-input',
                                                                   'append': 'fa fa-calendar', }),
                                      )

    class Meta:
        model = Task
        fields = '__all__'
        # labels = {'category': 'Категория'}
        labels = {'address': 'Адрес', 'category': 'Категория'}
        widgets = {
            "address": AddressCustomTitleWidget,
            "category": CategoryCustomTitleWidget,
            'author_eds': forms.HiddenInput(),

            'sms_is_sended': forms.HiddenInput(),
            'sms_is_queue': forms.HiddenInput(),
            'sms_result': forms.HiddenInput(),

            # 'sms': forms.CheckboxInput(),
            # 'sms': forms.NullBooleanSelect(),
            # 'address_task': forms.HiddenInput(),

            'created_by': forms.HiddenInput(),
            'updated_by': forms.HiddenInput(),

            # "name": NameForm(),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    # def __init__(self, *args, **kwargs):
    #     super(TaskForm, self).__init__(*args, **kwargs)
    #     self.fields['target'].widget.attrs = {
    #         'data-theme': 'bootstrap4',
    #     }


# class StatusForm(forms.ModelForm):
#     # transmission_time = forms.TimeField(label=_("Время передачи"), required=False,
#     #                                     widget=TimePicker(options={
#     #                                         'format': 'LT',
#     #                                         # 'format': 'HH:mm',
#     #                                     },
#     #                                         attrs={'class': 'form-control datetimepicker-input',
#     #                                                'append': 'fa fa-clock-o', }
#     #                                     ),
#     #                                     )
#
#     status_time = forms.DateTimeField(label=_("Время исполнения"), required=False,
#                                       widget=DateTimePicker(options={'format': 'L LT', },
#                                                             attrs={'class': 'form-control datetimepicker-input',
#                                                                    'append': 'fa fa-calendar', }),
#                                       )
#
#     class Meta:
#         model = Status
#         fields = '__all__'
#         # labels = {'address': 'Адрес'}
#         # widgets = {
#         #     "address": AddressCustomTitleWidget,
#         #     "category": CategoryCustomTitleWidget,


"""  https://django.fun/tutorials/kak-podklyuchit-vidzhet-vybora-daty-v-django/  """
