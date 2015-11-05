# -*- coding: utf-8 -*-
from zouxiu_client import *
import time
import json

zouxiu_client = Zouxiu_client()
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
#print(zouxiu_client.product(data=request_data))
print(zouxiu_client.getitem(data={}))


'''
# 3.2 商品批量分页查询(loop)
while True:
    shangpin_client.set_path('/commodity/findinfobypage')
    request_data = {"PageIndex":"1","PageSize":"100","endTime":"","startTime":""}
    shangpin_client.set_request_data(request_data)
    shangpin_client.req_post()
    response = shangpin_client.req_post()
    content = response.content
    print(content)
    shangpin_client.reset()
    time.sleep(1)
# 3.2 商品批量分页查询
shangpin_client.set_path('/commodity/findinfobypage')
request_data = {"PageIndex":"1","PageSize":"100","endTime":"","startTime":""}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
# 3.3 品类信息查询(未完成)
shangpin_client.set_path('/commodity/findcategorybypage')
request_data = {"PageIndex":"1","PageSize":"200"}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
# 3.4 品类下销售属性查询
shangpin_client.set_path('/commodity/findproductattr')
request_data = {"CategoryNo": "A01B01C01D02"}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
#3.7 基础色系查询（未完成）
shangpin_client.set_path('/commodity/findcolor')
request_data = {}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
#3.8 品牌信息查询（未完成）
shangpin_client.set_path('/commodity/findbrandbypage')
request_data = {"PageIndex":"1","PageSize":"200"}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
#3.9 地区信息查询（未完成）
shangpin_client.set_path('/commodity/findareabypage')
request_data = {"PageIndex":"1","PageSize":"200"}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
shangpin_client.set_path('/base/currency')
request_data = {}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
# 1.1. 供货价查询
shangpin_client.set_path('/supply/findinfo')
request_data = {"Starttime":"","Endtime":"", "SkuNos":"30003221001", "PriceStatus":""}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
# 1.2. 供货价更新 未完成
shangpin_client.set_path('/supply/updateprice')
request_data = {"SkuNo":"30003221001","SupplyPrice":"100.00","MarkePrice":"900.00"}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
# 2.1 库存查询
shangpin_client.set_path('/stock/findinfo')
request_data = ["30003221001", "30002856001"]
#request_data = ["30092240001"]
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
# 2.2 库存更新
shangpin_client.set_path('/stock/update')
request_data = {"SkuNo":"30003221001", "InventoryQuantity":100 }
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
# 5.1 采购单分页查询
shangpin_client.set_path('/purchase/findporderbypage')
request_data = {"PageIndex":"1","PageSize":"20","UpdateTimeBegin":"2015-07-16 14:00:00","UpdateTimeEnd":"2015-07-24 23:59:59"}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
# 6.1 发货单分页查询
shangpin_client.set_path('/purchase/finddorderbypage')
request_data = {"PageIndex":"1","PageSize":"20","UpdateTimeBegin":"2014-01-16 14:00:00","UpdateTimeEnd":"2015-01-17 14:00:00"}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
# 7.1 返货单分页查询
shangpin_client.set_path('/purchase/findrorderbypage')
request_data = {"PageIndex":"1","PageSize":"20","UpdateTimeBegin":"2014-01-16 14:00:00","UpdateTimeEnd":"2015-01-17 14:00:00"}
shangpin_client.set_request_data(request_data)
response = shangpin_client.req_post()
content = response.content
print(content)
'''

#response_dict = json.loads(content)
#print(response_dict.keys())
#print(response_dict['response'].keys())



