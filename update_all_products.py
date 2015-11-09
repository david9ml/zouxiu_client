# -*- coding: utf-8 -*-
from zouxiu_client import *
from const import *
from xml.dom import minidom
import time
import json
import functools
import traceback

#python 2.7.9

def get_all_products(zouxiu_client):
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
    return total_products_list


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

def update_one_product(item_list, client):
    parent_sku = item_list[0]
    node = item_list[1]
    print(parent_sku)
    print(node)
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
    #print(image_str)
    #print(client.product(data=request_data))
    #time.sleep(1)

def convert_one_product(node):
    #{'母产品id': [母产品下的所有产品列表], ......}
    pt_sku = get_or_empty_str(node, "pt_sku")
    return {pt_sku: [node]}

def merge_two_nodes(node1, node2):
    key_of_node2 = node2.keys()[0]
    if node1.has_key(key_of_node2):
        node1[key_of_node2].append(node2[key_of_node2][0])
    else:
        node1[key_of_node2] = node2[key_of_node2]
    return node1

def update_one_stock(item_dict, erp_products_dict, client):
    print(item_dict['productId'])
    print("zouxiu stock:")
    print(item_dict['stock'])
    print("erp stock:")
    erp_item = None
    if erp_products_dict.has_key(item_dict['productId']):
        for item in erp_products_dict[item_dict['productId']]:
            if get_or_empty_str(item, "code") == item_dict['itemId']:
                erp_item = item
                print(get_or_empty_str(item, "quatity"))
                if int(get_or_empty_str(item, "quatity")) == int(item_dict['stock']):
                    print("zouxiu stock == erp_stock, not updating stock...")
                else:
                    print("zouxiu stock != erp_stock, need updating stock...")
                erp_products_dict[item_dict['productId']].remove(item)
    if erp_item == None:
        print("zouxiu item not in erp_stock, set stock 0 in zouxiu...")

def update_all_products():
    stock_doc = minidom.parse("./morning.inventory.hk.xml")
    erp_products = stock_doc.getElementsByTagName("product")
    erp_products_dict = reduce(merge_two_nodes, map(convert_one_product, erp_products))

    zouxiu_client = Zouxiu_client()
    print(len(erp_products))
    print(len(erp_products_dict))
    #map(functools.partial(update_one_product, client={}), erp_products_dict.iteritems())
    print("###################################################################################")
    print("Firstly, we update stocks!")
    print("###################################################################################")
    map(functools.partial(update_one_stock, erp_products_dict = erp_products_dict, client=zouxiu_client), get_all_products(zouxiu_client=zouxiu_client))

    print("###################################################################################")
    print("All products are updated!")
    print("###################################################################################")
    return True

update_all_products()
