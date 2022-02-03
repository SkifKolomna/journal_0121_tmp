from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from tasks.models import Act, Address, Resource, Category


# Create your models here.
class Chart(models.Model):
    created_on = models.DateTimeField(_("Время создания"), auto_now_add=True)
    # address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True,
    #                             related_name="address_charts")
    # resource = models.ForeignKey(Resource, on_delete=models.SET_NULL, null=True, blank=True,
    #                              related_name="resource_charts")
    # act = models.ForeignKey(Act, on_delete=models.SET_NULL, null=True, blank=True, related_name="act_charts")

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    resource = models.ForeignKey(Resource, on_delete=models.SET_NULL, null=True, blank=True, )
    act = models.ForeignKey(Act, on_delete=models.SET_NULL, null=True, blank=True)

    start_time = models.DateTimeField(_("Начало"), blank=True, null=True, auto_now=False, auto_now_add=False)
    stop_time = models.DateTimeField(_("Завершение"), blank=True, null=True, auto_now=False, auto_now_add=False)
    description = models.TextField(_("Комментарий"), blank=True, null=True)

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('chart-detail', args=[str(self.id)])

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'график'
        verbose_name_plural = 'графики'

    def __str__(self):
        return str(self.id)
