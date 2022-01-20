import time

import requests

ip_sms = '192.168.0.101'
url = f'http://{ip_sms}/sendsms'
# is_debug = True
is_debug = False

# print('sms')

def send_sms(tel: str, ticket: str) -> requests.Response:
    """
            Отправка sms по шаблону
            :param tel: номер телефона, строка в формате 899999999999
            :param ticket: номер заявки, строка
            :return: request post
    """
    data = {'username': 'admin',
            'password': 'cthuttdbx',
            'port': 'gsm-1.2',
            'timeout': '20',
            'phonenumber': tel,
            # 'phonenumber': '8985891794',
            'message': f'Заявка №{ticket} выполнена.\rС уважением, ООО "ДГХ"',
            }
    r = None

    if not is_debug:
        try:
            r = requests.post(url, params=data)
            sms_dict = dict()
            for str in r.text.split('\n'):
                if ': ' in str:
                    str_dict = str.split(': ')
                    sms_dict[str_dict[0]] = str_dict[1]
            sms_dict['responce'] = r.status_code
            # print(sms_dict)
            return sms_dict
        # except requests.exceptions as e:
        except:
            pass
