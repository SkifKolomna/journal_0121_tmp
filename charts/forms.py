from django import forms
from django.utils.translation import ugettext as _
from django_select2.forms import (
    ModelSelect2Widget,
)
from django.db import models
from django.utils.translation import ugettext_lazy as _

from tasks.models import Address, Category
from tempus_dominus.widgets import DateTimePicker

from . import models
from .models import Chart


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
        # pprint(context)
        if attrs_optgroups['value']:
            label = models.Address.objects.all().filter(id=attrs_optgroups['value'])[0]
            attrs_optgroups['label'] = label
        return context


class CategoryCustomTitleWidget(ModelSelect2Widget):
    model = Category()
    queryset = models.Category.objects.all().filter(visible=True)
    search_fields = ["name__icontains"]


class ChartForm(forms.ModelForm):
    start_time = forms.DateTimeField(label=_("Начало"), required=False,
                                     widget=DateTimePicker(options={'format': 'L LT', },
                                                           attrs={'class': 'form-control datetimepicker-input',
                                                                  'append': 'fa fa-calendar', }),
                                     )
    stop_time = forms.DateTimeField(label=_("Завершение"), required=False,
                                    widget=DateTimePicker(options={'format': 'L LT', },
                                                          attrs={'class': 'form-control datetimepicker-input',
                                                                 'append': 'fa fa-calendar', }),
                                    )

    class Meta:
        model = Chart
        fields = '__all__'
        labels = {'address': 'Адрес', 'resource': 'Коммунальный ресурс', 'act': 'Действие'}
        widgets = {
            "address": AddressCustomTitleWidget(),
        }


"""  https://django.fun/tutorials/kak-podklyuchit-vidzhet-vybora-daty-v-django/  """
