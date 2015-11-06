# -*- coding: utf-8 -*-
from zouxiu_client import *
from xml.dom import minidom
import time
import json
import functools

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

def get_or_empty_str(node, tag_name):
    try:
        return node.getElementsByTagName(tag_name)[0].firstChild.data
    except:
        return ""

def create_one_product(node, client):
    model = get_or_empty_str(node, "model")
    material = get_or_empty_str(node, "material")
    color = get_or_empty_str(node, "color")
    pt_sku = get_or_empty_str(node, "pt_sku")
    pt_name = get_or_empty_str(node, "pt_name")
    price_eu = get_or_empty_str(node, "price_eu")
    price = get_or_empty_str(node, "price")
    name = get_or_empty_str(node, "name")
    size = get_or_empty_str(node, "size")
    brand = get_or_empty_str(node, "brand")
    cate = get_or_empty_str(node, "cate")
    quantity = get_or_empty_str(node, "quatity")
    code = get_or_empty_str(node, "code")
    request_data = [
                    {"productDetailUrl": "http://www.yvogue.com",
                    "xopSupplierItems": [
                    {"productId": pt_sku,
                    "productName": name,
                    "brandNameZhs": brand,
                    "productDesc": model+'_'+material+'_'+color,
                    "itemId": code,
                    "stock":quantity,
                    "supplyPrice":price,
                    "catName": cate}
                    ],
                    "brandNameZhs": brand,
                    "productName": pt_name,
                    "productId": pt_sku
                    }
                ]
    print(client.product(data=request_data))
    time.sleep(2)

#print(zouxiu_client.product(data=request_data))
#print(zouxiu_client.getitem(data={}))

def push_all_products_once():
    zouxiu_client = Zouxiu_client()
    stock_doc = minidom.parse("./morning.inventory.hk.xml")
    erp_products = stock_doc.getElementsByTagName("product")
    map(functools.partial(create_one_product, client=zouxiu_client), erp_products)
    print("All products are done")

push_all_products_once()

