# -*- coding: utf-8 -*-
import os

import django

#  you have to set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'journal.settings')
django.setup()

from tasks.models import Task


def get_string():
    with open('eds_db.csv', 'r+') as f:
        content = f.readlines()
        for i, line in enumerate(content):
            str = line.replace('\n', '')
            # print('i ', i, 'line ', str)
            fio_list = str.split(';')

            tel = fio_list[0]

            tasks = Task.objects.all()

            tasks_tel = tasks.filter(phone__icontains=tel)

            # print(tasks_tel)
            for x in tasks_tel:
                print('')
                if x.surname_name:
                    print(x.surname_name)
                    # x.surname_name = ''
                if x.first_name:
                    print(x.first_name)
                    # x.first_name = ''
                if x.patronymic_name:
                    print(x.patronymic_name)
                    # x.patronymic_name = ''

                # x.surname_name = fio_list[1]
                # x.first_name = fio_list[2]
                # x.patronymic_name = fio_list[3]
                # #
                # x.save()


def main():
    get_string()


if __name__ == '__main__':
    main()
