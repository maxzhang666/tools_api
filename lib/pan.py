# -*- encoding: utf-8 -*-
# -*- encoding: utf-8 -*-
'''
@File    :   pan.py
@Time    :   2020年09月27日 15:08:46 星期天
@Author  :   ermao
@Version :   1.0
@Link    :   https://erma0.gitee.io
@Desc    :   百度网盘提取码查询
'''

print('start pan.py')

import requests


def get_passwd_by_url(url):
    if 'baidu.com/s/1' in url:
        sp = '/s/1'
    elif 'init?surl=' in url:
        sp = 'surl='
    else:
        return {'error': 'Invalid URL'}
    try:
        id = url.split(sp)[1]
    except Exception:
        return {'error': 'Invalid URL'}
    if '&' in id:
        id = id.split('&')[0]
    if '#' in id:
        id = id.split('#')[0]
    res = get_passwd_by_id(id)
    return res


def get_passwd_by_id(id):
    url = 'https://ypsuperkey.meek.com.cn/api/v1/item/check-data'
    data = {'uuids': 'BDY-' + id, 'client_version': '2019.2'}
    try:
        r = requests.post(url, data=data).json()
        d = r.get('BDY-' + id)
        if d:
            password = d.get('access_code')
            if password:
                return {
                    'source': 'ypsuperkey.meek.com.cn',
                    'password': password
                }
    except Exception:
        return {'error': 'An exception occurred'}

    url = 'https://search.pandown.cn/api/query?referral=&surl=1' + id
    try:
        r = requests.get(url).json()
        password = r.get('password')
        if password:
            return {'source': 'pandown.cn', 'password': password}
    except Exception:
        return {'error': 'An exception occurred'}

    return {'error': 'Can not find the password'}


if __name__ == "__main__":
    q = get_passwd_by_url('百度盘https://pan.baidu.com/s/1Qg4VrIu3KwmKWa_DwacWcA')
    print(q)
