# -*- encoding: utf-8 -*-
'''
@File    :   qq.py
@Time    :   2020年09月27日 15:09:05 星期天
@Author  :   ermao
@Version :   1.0
@Link    :   https://erma0.gitee.io
@Desc    :   QQ相关接口
'''

print('start qq.py')

import requests


def get_info(qq):
    url = 'https://r.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?get_nick=1&uins=1321245360'
    # url = 'https://users.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?uins=1321245360'
    try:
        res = requests.get(url).text.split('"')
        # 这里取回的是历史头像,换另一个接口
        # qlogo = res[3]
        qlogo = get_logo(qq)
        nickName = res[5]
        resp = {'nickName': nickName, 'qlogo': qlogo}
        return resp
    except Exception:
        return {'error': 'An exception occurred'}


def get_logo(qq):
    url = 'https://q1.qlogo.cn/g?b=qq&nk={}&s=640'.format(qq)
    return url


if __name__ == "__main__":
    # a = get_logo('1737882100')
    a = get_info('1737882100')
    print(a)
