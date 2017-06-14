#-*- coding: utf-8 -*-
'''
OLTP-API-1007.py
Author : CC
Version : 1.1.1
Date : 2017-05-31
Description : RAW API
'''

from flask import Response
from flask import Flask
from flask import request
import requests
import json
app = Flask(__name__)

txt1 = {'data': 'success', 'result': {'resultCode': 1001, 'resultMsg': '收票处理成功'}}
# txt2 = {'data': 'fail', 'result': {'resultCode': 1002, 'resultMsg': '收票处理失败'}}
txt3 = {'data': 'success', 'result': {'resultCode': 2001, 'resultMsg': '拒票处理成功'}}
# txt4 = {'data': 'fail', 'result': {'resultCode': 2002, 'resultMsg': '拒票处理失败'}}

# @app.route('/test')
# def hello_world():
#     return "hello !!"

@app.route('/servers/oltp/test1007', methods=['POST'])
def mock():
    statu = request.form.get('status')
    if statu == '1':
        response = Response(json.dumps(txt1), mimetype='application/json')
        response.headers.add('Server', 'python flask')
        return response

    elif statu == '0':
        response = Response(json.dumps(txt3), mimetype='application/json')
        response.headers.add('Server', 'python flask')
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run(debug=True)
