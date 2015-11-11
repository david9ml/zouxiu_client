# -*- coding: utf-8 -*-
from secret_file import *
from time import gmtime, strftime
from datetime import timedelta, datetime
import requests
import json

class Baseclient(object):
    def __init__(self):
        self.app_key = APP_KEY
        self.app_secret = APP_SECRET
        self.params = {}
        self.url = API_URL
        self.uid = UID
        self.timestamp = ''
        self.sign = ''
        self.path = ''
        self.data = ''
        self.headers = {'content-type': 'application/json'}
        self.params = {"uid": self.uid, "charset": "utf-8", "format": "json", "language": "zh_CN"}
        self.get_token()

    def get_token(self):
        self.set_path('/api/user/token')
        request_data = {"username":self.app_key, "password": self.app_secret, "timestamp": datetime.now().strftime("%Y%m%d%H%M%S")}
        response = requests.request('PUT', self.url+self.path, json=request_data, headers=self.headers, params=self.params)
        content = response.content
        response_dict = json.loads(content)
        self.params['token'] = response_dict['data']
        print(response_dict['data'])
        return response_dict['data']

    def print_secrets(self):
        print(self.app_key)
        print(self.app_secret)

    def reset(self):
        import gc
        gc.collect()

    def req_put(self):
        response = requests.request('PUT', self.url+self.path, json=self.data, params=self.params)
        return response

    def req_get(self):
        response = requests.request('GET', self.url+self.path, json=self.data, params=self.params)
        return response


    def req_post(self):
        print(self.data)
        print(self.params)
        response = requests.request('POST', self.url+self.path, json=self.data, params=self.params)
        return response

    def set_path(self, path_value):
        self.path = path_value
        return True

    def set_data(self, data):
        self.data = data
        return True
