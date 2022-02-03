from datetime import timedelta

import arrow
# django.utils.timezone.now()
from django.db.models.signals import post_save
from django.dispatch import receiver

from commons.utils import (TASK_SOURCE, TASK_STATUS, REU_CHOICE, return_complete_address)
# from django.contrib.auth.models import User  # Required to assign User as a borrower
from django.contrib.auth import get_user_model  # Required to assign User as a borrower
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class Subdivision(models.Model):
    string_subdivision = models.CharField(_("Подразделение"), blank=True, unique=True, max_length=64)
    is_active = models.BooleanField(blank=True, default=True)

    class Meta:
        ordering = ("string_subdivision",)
        verbose_name = "подразделение"
        verbose_name_plural = "подразделения"

    def __str__(self):
        return self.string_subdivision


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic = models.CharField(_("Отчество"), blank=True, null=True, max_length=255)
    full_name = models.CharField(_("Полное имя"), max_length=30, blank=True)
    short_name = models.CharField(_("Короткое имя"), max_length=30, blank=True)
    subdivision = models.ForeignKey(Subdivision, on_delete=models.SET_NULL,
                                    null=True, blank=True)
    is_operator = models.BooleanField(_('operator'), default=True)

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Address(models.Model):
    string_address = models.CharField(_("Адрес"), blank=True, unique=True, max_length=64)
    string_subdivision = models.ForeignKey(Subdivision, on_delete=models.SET_NULL,
                                           null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)

    class Meta:
        ordering = ("string_address",)
        verbose_name = "адрес"
        verbose_name_plural = "адреса"

    def __str__(self):
        return self.string_address
        # return self.id


class Resource(models.Model):
    name = models.CharField(_("Ресурс"), blank=True, unique=True, max_length=64)

    class Meta:
        ordering = ("name",)
        verbose_name = "ресурс"
        verbose_name_plural = "ресурсы"

    def __str__(self):
        return self.name


class Act(models.Model):
    name = models.CharField(_("Действие"), blank=True, unique=True, max_length=64)

    class Meta:
        ordering = ("name",)
        verbose_name = "действие"
        verbose_name_plural = "действия"

    def __str__(self):
        return self.name


class Category(models.Model):
    edsmo_id = models.PositiveSmallIntegerField(_("Код в ЕДС"), unique=True)
    visible = models.BooleanField(blank=True, default=True)
    deadline = models.DurationField(_("Часов на исполнение"), default=timedelta(), blank=True, null=True)
    name = models.CharField(_("Категория заявки"), blank=True, unique=True, max_length=250)

    class Meta:
        ordering = ("name",)
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


# class Status(models.Model):
#     executor = models.CharField(_("Предано"), blank=True, null=True, max_length=255)
#     status_task = models.CharField(_("Статус заяки"), max_length=255, blank=True, null=True, choices=TASK_STATUS)
#     status_time = models.DateTimeField(_("Время исполнения"), blank=True, null=True, auto_now=False, auto_now_add=False)
#     comment_status = models.TextField(_("Комментарий к статусу"), blank=True, null=True)
#     created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
#     created_by = models.ForeignKey(User,
#                                    verbose_name='Создана',
#                                    on_delete=models.SET_NULL,
#                                    null=True,
#                                    blank=True,
#                                    max_length=100,
#                                    related_name='status_created_by')
#     updated_by = models.ForeignKey(User,
#                                    verbose_name='Изменена',
#                                    on_delete=models.SET_NULL,
#                                    null=True,
#                                    blank=True,
#                                    max_length=100,
#                                    related_name='status_updated_by')
#
#
#     class Meta:
#         ordering = ['-created_on']
#
#     def __str__(self):
#         return str(self.id)
#
#     def get_absolute_url(self):
#         # return reverse('task-detail', args=[str(self.id)])
#         return reverse('task-detail', args=[self.id])


class Task(models.Model):
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    apartment = models.CharField(_("Квартира"), max_length=55, blank=True, null=True)
    porch = models.PositiveSmallIntegerField(_("Подъезд"), blank=True, null=True)
    floor = models.PositiveSmallIntegerField(_("Этаж"), blank=True, null=True)
    phone = PhoneNumberField(_("Телефон"), null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(_("Содержание заявки"), blank=True, null=True)
    reu = models.CharField(_("РЭУ"), max_length=255, blank=True, null=True, choices=REU_CHOICE)
    executor = models.CharField(_("Предано"), blank=True, null=True, max_length=255)
    transmission_time = models.TimeField(_("Время передачи"), blank=True, null=True, auto_now=False, auto_now_add=False)
    source_task = models.CharField(_("Источник заявки"), max_length=255, blank=True, null=True, choices=TASK_SOURCE)
    sms_is_active = models.BooleanField(_("Согласие на СМС"), blank=True, default=False)
    sms_is_sended = models.BooleanField(_("Смс отправлена"), blank=True, default=False)
    sms_is_queue = models.BooleanField(_("Смс уже в очереди"), blank=True, default=False)
    sms_result = models.CharField(_("Результат отправки"), max_length=55, blank=True, null=True)
    status_task = models.CharField(_("Статус заяки"), max_length=255, blank=True, null=True, choices=TASK_STATUS)
    status_time = models.DateTimeField(_("Время исполнения"), blank=True, null=True, auto_now=False, auto_now_add=False)

    # history_status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)

    comment_status = models.TextField(_("Комментарий к статусу"), blank=True, null=True)
    surname_name = models.CharField(_("Фамилия"), blank=True, null=True, max_length=255)
    first_name = models.CharField(_("Имя"), blank=True, null=True, max_length=255)
    patronymic_name = models.CharField(_("Отчество"), blank=True, null=True, max_length=255)
    author_eds = models.CharField(_("Автор в ЕДС"), blank=True, null=True, max_length=255)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   verbose_name='Создана',
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   max_length=100,
                                   related_name='created_by')
    updated_by = models.ForeignKey(User,
                                   verbose_name='Изменена',
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   max_length=100,
                                   related_name='updated_by')

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    def get_name(self):
        user = self.created_by
        # if user and user.first_name and user.last_name:
        if user:
            short_name = user.profile.short_name
            full_name = user.profile.full_name
            return short_name, full_name

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('tasks:task-detail', args=[str(self.id)])

    def __str__(self):
        # return self.title
        # return self.id
        return str(self.id)

    def get_complete_address(self):
        return return_complete_address(self)

    @property
    def phone_raw_input(self):
        if str(self.phone) == '+NoneNone':
            return ''
        return self.phone

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    @property
    def get_team_users(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        return User.objects.filter(id__in=team_user_ids)

    @property
    def get_team_and_assigned_users(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        assigned_user_ids = list(self.assigned_to.values_list('id', flat=True))
        user_ids = team_user_ids + assigned_user_ids
        return User.objects.filter(id__in=user_ids)

    @property
    def get_assigned_users_not_in_teams(self):
        team_user_ids = list(self.teams.values_list('users__id', flat=True))
        assigned_user_ids = list(self.assigned_to.values_list('id', flat=True))
        user_ids = set(assigned_user_ids) - set(team_user_ids)
        return User.objects.filter(id__in=list(user_ids))

    # def save(self, *args, **kwargs):
    #     super(Lead, self).save(*args, **kwargs)
    #     queryset = Lead.objects.all().exclude(status='converted').select_related('created_by'
    #         ).prefetch_related('tags', 'assigned_to',)
    #     open_leads = queryset.exclude(status='closed')
    #     close_leads = queryset.filter(status='closed')
    #     cache.set('admin_leads_open_queryset', open_leads, 60*60)
    #     cache.set('admin_leads_close_queryset', close_leads, 60*60)
