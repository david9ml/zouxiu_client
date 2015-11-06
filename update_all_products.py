# -*- coding: utf-8 -*-
from zouxiu_client import *
from const import *
from xml.dom import minidom
import time
import json
import functools

def get_or_empty_str(node, tag_name):
    try:
        return node.getElementsByTagName(tag_name)[0].firstChild.data
    except:
        return ""

def get_image_str(brand, model, material, color):
    try:
        brand_no_str = BRAND_ID_DICT[brand]
    except:
        brand_no_str = ''
    url_str = 'http://img.yvogue.hk/pimg/pl/' + brand_no_str + '/m' + model.lower() + '/m' + material.lower() + '/c' + color.lower() + '.jpg'
    return url_str

def push_all_products_once():
    zouxiu_client = Zouxiu_client()
    stock_doc = minidom.parse("./morning.inventory.hk.xml")
    erp_products = stock_doc.getElementsByTagName("product")
    map(functools.partial(update_one_product, client=zouxiu_client), erp_products)
    print("All products are done")

def get_item_from_zouxiu(sku):
    return {}

def update_one_product(node, client):
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
    image_str = get_image_str(brand, model, material, color)
    print(image_str)
    #print(client.product(data=request_data))
    #time.sleep(1)

def update_all_products():
    stock_doc = minidom.parse("./morning.inventory.hk.xml")
    erp_products = stock_doc.getElementsByTagName("product")
    map(functools.partial(update_one_product, client={}), erp_products)
    print("All products are updated!")
    return True

update_all_products()

