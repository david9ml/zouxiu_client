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

def merge_two(node1, node2):
    key_of_node2 = node2.keys()[0]
    if node1.has_key(key_of_node2):
        node1[key_of_node2].append(node2[key_of_node2][0])
    else:
        node1[key_of_node2] = node2[key_of_node2]
    return node1

def convert_one_product_zouxiu(item_dict):
    #{'母产品id': [母产品下的所有产品列表], ......}
    pt_sku = item_dict['productId']
    return {pt_sku: [item_dict]}

def update_one_stock(item_dict, erp_products_dict, client):
    print(item_dict['productId'])
    print("zouxiu stock:")
    print(item_dict['stock'])
    print("erp stock:")
    erp_item = None
    global updated_count_total
    if erp_products_dict.has_key(item_dict['productId']):
        for item in erp_products_dict[item_dict['productId']]:
            if get_or_empty_str(item, "code") == item_dict['itemId']:
                erp_item = item
                print(get_or_empty_str(item, "quatity"))
                if int(get_or_empty_str(item, "quatity")) == int(item_dict['stock']) :
                    print("zouxiu stock == erp_stock, not updating stock...")
                else:
                    #if get_or_empty_str(item, "code")=="9600000818912":
                    print("<-zouxiu stock != erp_stock, need updating stock...")
                    response = client.update_item_stock(data=[{"itemId":item_dict['itemId'], "stock":get_or_empty_str(item, "quatity")}])
                    print(response)
                    updated_count_total += 1
                    print("update complete!->")
                    #time.sleep(100)
                erp_products_dict[item_dict['productId']].remove(item)
                if erp_products_dict[item_dict['productId']] == []:
                    erp_products_dict.pop(item_dict['productId'], None)
    if erp_item == None:
        print("<-zouxiu item not in erp_stock, set stock 0 in zouxiu...")
        if int(item_dict['stock']) == 0:
            print("zouxiu stock already 0, update complete!->")
        else:
            response = client.update_item_stock(data=[{"itemId":item_dict['itemId'], "stock":0}])
            updated_count_total += 1
            print("zouxiu stock already 0, set 0, update complete!->")

def upload_one_erp_product(item_list, zouxiu_items_dict, client):
    parent_sku = item_list[0]
    for node in item_list[1]:
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
        image_str = get_image_str(brand, model, material, color)
        if zouxiu_items_dict.has_key(parent_sku):
            print("<-Parent exist, we create item")
            request_data = [
                            {"itemId": code,
                            "itemColor": color,
                            "productId": pt_sku,
                            "itemSize":size,
                            "supplyPrice":int(float(price)*0.72129),
                            "marketPrice":int(float(price)*0.72129),
                            "sellPrice":int(float(price)*0.72129),
                            "mainPicture":image_str,
                            "catName": cate,
                            "stock": quantity}
                            ]
            print(client.item(data=request_data))
            print("Creating item complete->")
            time.sleep(1)
        else:
            print("<-Parent not exist, we create product")
            request_data = [
                            {"productDetailUrl": "http://www.yvogue.com",
                            "xopSupplierItems": [
                            {"productId": pt_sku,
                            "productName": name,
                            "brandNameZhs": brand,
                            "productDesc": model+'_'+material+'_'+color,
                            "itemId": code,
                            "stock":quantity,
                            "supplyPrice":int(float(price)*0.72129),
                            "marketPrice":int(float(price)*0.72129),
                            "sellPrice":int(float(price)*0.72129),
                            "mainPicture":image_str,
                            "catName": cate}
                            ],
                            "brandNameZhs": brand,
                            "productName": pt_name,
                            "productId": pt_sku
                            }
                        ]
            print(client.product(data=request_data))
            print("Creating product complete->")
            zouxiu_items_dict[parent_sku] = {}
            time.sleep(1)

def update_all_products():
    stock_doc = minidom.parse("./morning.inventory.hk.xml")
    zouxiu_client = Zouxiu_client()

    erp_products = stock_doc.getElementsByTagName("product")
    erp_products_dict = reduce(merge_two, map(convert_one_product, erp_products))
    all_zouxiu_items = get_all_products(zouxiu_client=zouxiu_client)
    all_zouxiu_items_dict = reduce(merge_two, map(convert_one_product_zouxiu, all_zouxiu_items))

    #map(functools.partial(update_one_product, client={}), erp_products_dict.iteritems())
    print("--------------------------------------------------------------------------------------------------")
    print("Firstly, we update stocks!")
    print("--------------------------------------------------------------------------------------------------")
    time.sleep(3)
    map(functools.partial(update_one_stock, erp_products_dict = erp_products_dict, client=zouxiu_client), all_zouxiu_items)
    print("First step finished!")
    print("updated:")
    print(updated_count_total)
    time.sleep(5)

    #print("NEW PRODUCTS:")
    #print(erp_products_dict)
    print("--------------------------------------------------------------------------------------------------")
    print("Secondly, we create new products!")
    print("--------------------------------------------------------------------------------------------------")
    time.sleep(3)
    #print(erp_products_dict)
    map(functools.partial(upload_one_erp_product, zouxiu_items_dict=all_zouxiu_items_dict, client=zouxiu_client), erp_products_dict.iteritems())

    print("--------------------------------------------------------------------------------------------------")
    print("All products are updated!")
    print("--------------------------------------------------------------------------------------------------")
    print(erp_products_dict)
    return True

while True:
    while True:
        try:
            updated_count_total = 0
            update_all_products()
            break
        except:
            traceback.print_exc()
            print("Network failure, retry in 60secs...")
            time.sleep(60)
    import gc
    gc.collect()
    print("sleep 5*60 sec...")
    time.sleep(5*60)

