# -*- coding: utf-8 -*-
from zouxiu_client import *
import time
import json

def remove_all_products():
    zouxiu_client = Zouxiu_client()
    zouxiu_client.params["ip"] = "113.106.63.13"
    request_data = {}
    response = zouxiu_client.remove_all_products(data=request_data)
    print(response)

remove_all_products()

