# -*- coding: utf-8 -*-
from zouxiu_client import *
import time
import json

request_data = [
                {"productDetailUrl": "http://www.xiu.com",
                 "xopSupplierItems": [
                 {"productId": "00000004",
                 "productName": "test0000004",
                 "brandNameZhs": "Prada",
                 "productDesc": "Prada",
                 "itemId": "test0000004",
                 "stock":1,
                 "supplyPrice":23.6,
                 "catName": "fengyi"}
                 ],
                 "brandNameZhs":"普拉达",
                 "productName":"test0000004",
                 "productId":"00000004"
                }
               ]
def get_all_products():
    zouxiu_client = Zouxiu_client()
    response = zouxiu_client.getitem(data={ "pageSize":100 })
    response_dict = json.loads(response, encoding="utf-8")
    if response_dict['errorCode'] == '0':
        data = response_dict['data']
        total = data['total']
        loop = total/100
        residue  = total%100
        total_products_list = []
        for i in range(1, loop+1+(1 if residue!=0 else 0)):
            response = zouxiu_client.getitem(data={ "pageSize":100, "pageNo":i })
            response_dict = json.loads(response, encoding="utf-8")
            data = response_dict['data']
            item_list = data['list']
            total_products_list += item_list
        print(total_products_list)
        print(total)
        print(len(total_products_list))

get_all_products()


