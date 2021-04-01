# -*- encoding: utf-8 -*-
'''
@File    :   ip.py
@Time    :   2020年09月27日 15:08:06 星期天
@Author  :   ermao
@Version :   1.0
@Link    :   https://erma0.gitee.io
@Desc    :   IP定位
'''

print('start ip.py')

import requests

# 支付宝的key： 0113a13c88697dcea6a445584d535837
# gofan出行的key： 228a2d3b4f2c142386aa8b6ad900df52
key = '0113a13c88697dcea6a445584d535837'
# key = '228a2d3b4f2c142386aa8b6ad900df52'


def locate(ip):
    url = 'https://restapi.amap.com/v4/ip'
    params = {'key': key, 'ip': ip}
    try:
        resj = requests.get(url, params=params).json()
        lng = resj['data']['lng']
        lat = resj['data']['lat']
        res = location_info(lng, lat)
    except Exception:
        res = {'error': '出错了！'}
    return res


def location_info(longitude, latitude):
    url = 'https://amap.com/service/regeo'
    params = {'longitude': longitude, 'latitude': latitude}
    try:
        resj = requests.get(url, params=params).json()
        res = resj['data']
        res.pop('cross_list', None)
        res.pop('road_list', None)
        res.pop('sea_area', None)
    except Exception:
        res = {'error': '出错了！'}
    return res


def location_info_with_key(longitude, latitude):
    url = 'https://restapi.amap.com/v3/geocode/regeo'
    params = {
        "key": key,
        "s": "rsv3",
        "location": "{},{}".format(longitude, latitude)
    }
    try:
        resj = requests.get(url, params=params).json()
        res = {}
        res['addr'] = resj['regeocode']['formatted_address']
        res['citycode'] = resj['regeocode']['addressComponent']['citycode']
    except Exception:
        res = {'error': '出错了！'}
    return res


if __name__ == "__main__":
    # a = location_info('123.26011', '34.176219')
    a = location_info_with_key('123.26011', '34.176219')
    # a=locate('123.123.123.123')
    print(a)
