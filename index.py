# -*- encoding: utf-8 -*-
'''
@File    :   index.py
@Time    :   2020年09月04日 23:09:17 星期五
@Author  :   ermao
@Version :   1.0
@Link    :   https://erma0.gitee.io
@Desc    :   阿里云 函数计算 托管API—flask应用
'''

# 导入需求模块
# import json
import requests
from flask import Flask, request, jsonify

# 导入lib目录中的功能模块，随用随导入，没有用到的不会占用内存

# 需要设置返回header时
# from flask import make_response
# 需要用内置库将URL参数字符串解析成字典时
# from urllib.parse import parse_qs

app = Flask(__name__)

# jsonify返回中文直接显示，不加这一句的话会编码Unicode
app.config['JSON_AS_ASCII'] = False

# 返回jsonp解决跨域
# def jsonp(resp):
#     callback = request.args.get('callback')
#     return '{}({})'.format(callback, json.dumps(resp))


# 设置允许跨域
@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers[
        'Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ


# 设置404返回模板
@app.errorhandler(404)
def not_found(error):
    resp = {'作者': '二毛', 'QQ': '1737882100', '主页': 'https://erma0.gitee.io'}
    return jsonify(resp), 404


# 无参数
@app.route('/', methods=['GET', 'POST'])
def index():
    resp = {'作者': '二毛', 'QQ': '1737882100', '主页': 'https://erma0.gitee.io'}
    return jsonify(resp)


# @NAME :   IP定位
# @URL  :   /ip?ip=123.123.123.123
# @URL  :   /ip?longitude=123.26011&latitude=34.176219
@app.route('/ip', methods=['GET'])
def get_ip_info():
    from lib import ip as iplib
    user_ip = request.remote_addr
    ip = request.args.get('ip', user_ip)
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    if longitude:
        resp = iplib.location_info(longitude, latitude)
    elif ip:
        resp = iplib.locate(ip)
    else:
        resp = {'error': '参数错误！'}
    resp['ip'] = ip
    return jsonify(resp)


# @NAME :   QQ信息（昵称、头像）查询
# @URL  :   /qq?num=1737882100
@app.route('/qq', methods=['GET'])
def qq_info():
    from lib import qq
    num = request.args.get('num')
    if num:
        resp = qq.get_info(num)
    else:
        resp = {'msg': 'QQ号格式错误！'}
    return jsonify(resp)


# @NAME :   快手刷新cookie的did
# @URL  :   /kuaishou/did
@app.route('/kuaishou/did', methods=['GET'])
def did():
    from lib import kuaishou
    resp = kuaishou.refresh_did()
    return jsonify(resp)


# @NAME :   抖音查询用户信息
# @URL  :   /douyin/user?uid=72673737181
# @URL  :   /douyin/user?url=https://v.douyin.com/JBknYQp/
@app.route('/douyin/user', methods=['GET'])
def douyin_userinfo():
    from lib import douyin
    uid = request.args.get('uid')
    url = request.args.get('url')
    if uid:
        resp = douyin.user_info(uid)
    elif url:
        resp = douyin.user_info_url(url)
    else:
        resp = {'error': '参数错误！'}
    return jsonify(resp)


# @NAME :   抖音解析去水印视频
# @URL  :   /douyin/parse?id=6808453751930719502
# @URL  :   /douyin/parse?url=https://v.douyin.com/JBBebxv/
@app.route('/douyin/parse', methods=['GET'])
def douyin_parsing():
    from lib import douyin
    id = request.args.get('id')
    url = request.args.get('url')
    if id:
        resp = douyin.parse_by_id(id)
    elif url:
        resp = douyin.parse_by_url(url)
    else:
        resp = {'error': '参数错误！'}
    return jsonify(resp)
    # return jsonp(resp)


# @NAME :   快手查询用户信息
# @URL  :   /kuaishou/user?id=sanda927
# @URL  :   /kuaishou/user?url=https://v.kuaishou.com/6vPcKW
@app.route('/kuaishou/user', methods=['GET'])
def kuaishou_userinfo():
    from lib import kuaishou
    id = request.args.get('id')
    url = request.args.get('url')
    if id:
        resp = kuaishou.user_info(id)
    elif url:
        resp = kuaishou.user_info_url(url)
    else:
        resp = {'error': '参数错误！'}
    return jsonify(resp)


# @NAME :   快手解析去水印视频
# @URL  :   /kuaishou/parse?id=3xrkjbikwdh5chm
# @URL  :   /kuaishou/parse?url=https://v.kuaishou.com/4WAqVg
@app.route('/kuaishou/parse', methods=['GET'])
def kuaishou_parsing():
    from lib import kuaishou
    id = request.args.get('id')
    url = request.args.get('url')
    if id:
        resp = kuaishou.parse_by_id(id)
    elif url:
        # resp = kuaishou.parse_by_url2(url)
        resp = kuaishou.parse_by_url(url)
    else:
        resp = {'error': '参数错误！'}
    return jsonify(resp)
    # return jsonp(resp)


# 2020.09.06 失效
# @NAME :   百度网盘查提取码
# @URL  :   /pan?url=https://pan.baidu.com/s/1Qg4VrIu3KwmKWa_DwacWcA
# @URL  :   /pan?id=Qg4VrIu3KwmKWa_DwacWcA
@app.route('/pan', methods=['GET'])
def pan_parsing():
    from lib import pan
    id = request.args.get('id')
    url = request.args.get('url')
    if id:
        resp = pan.get_passwd_by_id(id)
    elif url:
        resp = pan.get_passwd_by_url(url)
    else:
        resp = {'error': '参数错误！'}
    return jsonify(resp)


@app.route('/parse', methods=['GET'])
def parse():
    p = request.args.get('p')
    if p:
        # 验证参数类型，未完成
        resp = {'error': '参数错误！'}
        requests.head(p, allow_redirects=False)
    else:
        resp = {'error': '参数错误！'}
    return jsonify(resp)


# 云端入口
def handler(environ, start_response):
    return app(environ, start_response)


# 本地调试
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2222)
