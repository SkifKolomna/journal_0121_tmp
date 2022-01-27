from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .utils import TASK_STATUS


class Comment(models.Model):
    executor = models.CharField(_("Предано"), blank=True, null=True, max_length=255)
    status_task = models.CharField(_("Статус заяки"), max_length=255, blank=True, null=True, choices=TASK_STATUS)
    status_time = models.DateTimeField(_("Время исполнения"), blank=True, null=True, auto_now=False, auto_now_add=False)
    # comment = models.CharField(_("Комментарий к статусу"), blank=True, null=True, max_length=255)
    comment = models.TextField(_("Комментарий к статусу"), blank=True, null=True)

    commented_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    task = models.ForeignKey('tasks.Task',
                             blank=True,
                             null=True,
                             related_name='tasks_comments',
                             on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User,
                                     verbose_name='Создана',
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True,
                                     max_length=100,
                                     related_name='comment_commented_by')
    updated_by = models.ForeignKey(User,
                                   verbose_name='Изменена',
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True,
                                   max_length=100,
                                   related_name='comment_updated_by')

    class Meta:
        ordering = ['-commented_on']
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        # return reverse('task-detail', args=[str(self.id)])
        return reverse('comment-detail', args=[self.id])
