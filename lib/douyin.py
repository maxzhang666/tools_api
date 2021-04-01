# -*- encoding: utf-8 -*-
'''
@File    :   douyin.py
@Time    :   2020年09月13日 13:59:59 星期天
@Author  :   ermao
@Version :   1.0
@Link    :   https://erma0.gitee.io
@Desc    :   抖音相关接口
'''

print('start douyin.py')

import requests
import re

headers = {
    'User-Agent':
    'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Mobile Safari/537.36'
}


def get_real_addr(uri):
    url = 'https://aweme.snssdk.com/aweme/v1/play/?video_id={}&ratio=720p&line=0'.format(
        uri)
    try:
        r = requests.head(url, headers=headers, allow_redirects=False)
        addr = r.headers['Location']
        return addr
    except Exception:
        return 'error'


def user_info(uid):
    url = 'https://www.iesdouyin.com/web/api/v2/user/info/?uid=' + uid
    try:
        r = requests.get(url).json()
        info = r['user_info']
        # [print(i, v) for i, v in info.items() if not v]  # 删除null/false
        info.pop('avatar_thumb', '')  # 删除中、小尺寸头像，只留大的
        info.pop('avatar_medium', '')
        info.pop('followers_detail', '')  # 删除空白key
        return info
    except Exception:
        return {'error': '出错了！'}


def user_info_url(url):
    if 'share/user/' in url:
        id = re.findall(r'share/user/(\d+)\??', url)[0]
    else:
        try:
            r = requests.head(url, headers=headers, allow_redirects=False)
            id = re.findall(r'share/user/(\d+)\??', r.headers['Location'])[0]
        except Exception:
            return {'error': 'URL错误！'}
    return user_info(id)


def parse_by_url(url):
    if '/share/video/' in url:
        id = re.findall(r'share/video/(\d+)/?\??', url)[0]
    else:
        try:
            r = requests.head(url, headers=headers, allow_redirects=False)
            id = re.findall(r'share/video/(\d+)/?\??',
                            r.headers['Location'])[0]
        except Exception:
            return {'error': 'URL错误！'}
    return parse_by_id(id)


def parse_by_id(id):
    url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + id
    try:
        r = requests.get(url).json()
        video = r['item_list'][0]
        res = {}
        res['desc'] = video['desc']
        res['comment'] = video['statistics']['comment_count']
        res['digg'] = video['statistics']['digg_count']
        res['author'] = video['author']['nickname']
        res['music'] = video['music']['play_url']['uri']
        res['cover'] = video['video']['cover']['url_list'][0]
        videouri = video['video']['play_addr']['uri']
        res['video'] = get_real_addr(videouri)
        return res
    except Exception:
        return {'error': '出错了！'}


if __name__ == "__main__":
    # a = user_info_url('https://v.douyin.com/JBknYQp/')
    # a = user_info('72673737181')
    a = parse_by_url('https://v.douyin.com/JBBebxv/')
    # a = parse_by_id('6808453751930719502')
    print(a)
