import asyncio
import datetime
import multiprocessing
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from pprint import pprint
from time import timezone

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.forms import model_to_dict
from django.utils import dateformat
from tasks.models import Task

from .sms import *
from .telethon_test import telegramm


def get_name(user):
    io = user.first_name.split(' ')
    short_name = str(user.last_name + ' ' + io[0][:1] + '.' + io[1][:1] + '.')
    full_name = str(user.last_name + ' ' + io[0] + ' ' + io[1])
    return short_name, full_name


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
            s += str(dateformat.format(datetime.timezone.make_naive(task.status_time), ' d.m.y H:i'))
        return s

    def fio():
        s = ''
        if task.surname_name:
            s += ' ' + str(task.surname_name)
        if task.first_name:
            s += ' ' + str(task.first_name)
        if task.patronymic_name:
            s += ' ' + str(task.patronymic_name)
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


@receiver(pre_save, sender=Task)
def pre_update_model(instance, sender, **kwargs):
    print('pre', kwargs)
    pprint('')
    if not kwargs['update_fields'] and instance.id:
        instance.old_model = instance
        instance.old = Task.objects.get(id=instance.id)


@receiver(post_save, sender=Task)
def task_signal(instance, sender, **kwargs):
    print('------------------------------------------------------------')
    print('post', kwargs)
    print('post', kwargs['created'])
    str_msg, reu = message_str(instance, **kwargs)

    if not kwargs['update_fields'] and hasattr(instance, 'old'):
        instance_current = model_to_dict(instance)
        instance_old = model_to_dict(instance.old)
        pprint(instance_current)
        instance_old_model = instance.old_model

        diffkeys = [key for key in instance_current if instance_current[key] != instance_old[key]]
        for key in diffkeys:
            print(key, ':', instance_old[key], '->', instance_current[key])
            if key == 'updated_by':
                print('-->', get_name(instance_old_model.updated_by)[0])

    def not_alarm_signal(task):
        post_save.disconnect(task_signal, sender=Task)
        task.save()
        post_save.connect(task_signal, sender=Task)

    def telegramm_function():
        telegramm(str_msg, reu)

    def set_queue(timeout):
        task = instance
        if task.sms_is_queue is not True:
            print('ставим sms в очередь')
            task.sms_is_queue = True
            not_alarm_signal(task)
            timer_on(timeout)
        else:
            print('sms уже в очереди')
            return True

    def sms_function():
        str_tel = sms_tel(instance, **kwargs)
        set_worry = ''
        if str_tel:
            set_worry, timeout = worry()
            if set_worry is False:
                is_queue = set_queue(timeout)
                if is_queue is True:
                    set_worry = False
                else:
                    set_worry = True
        # print(set_worry)
        if str_tel and set_worry is True:
            sms_dict = send_sms(str_tel, instance)
            if sms_dict['responce'] == 200:
                if sms_dict['result'] == '':
                    print('нет результата')
                    sms_function()
                else:
                    result = sms_dict['result']
                    print(f'Статус отправки смс {result}', ' ', datetime.now())
                    task = Task.objects.get(id=str(instance))
                    if task.sms_is_sended is not True:
                        task.sms_is_sended = True
                        task.sms_result = sms_dict['result']

                        not_alarm_signal(task)
                    print('send sms Ok')
            else:
                print('send sms Error')
                # sms_function()

    pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ''' sms telegramm on/off'''
    asyncio.gather(
        loop.run_in_executor(pool, sms_function),
        loop.run_in_executor(pool, telegramm_function)
    )
