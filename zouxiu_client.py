# -*- coding: utf-8 *-
from baseclient import *

class Zouxiu_client(Baseclient):

    def getitem(self, data):
        self.set_path('/api/supplier/item/getitem')
        self.set_data(data)
        return self.req_put().content

    def getonlineitem(self, data):
        self.set_path('/api/supplier/item/getonlineitem')
        self.set_data(data)
        return self.req_get().content

    def product(self, data):
        self.set_path('/api/supplier/product')
        self.set_data(data)
        return self.req_post().content

    def item(self, data):
        self.set_path('/api/supplier/item')
        self.set_data(data)
        return self.req_post().content

    def remove_all_products(self, data):
        self.set_path('/api/supplier/delete/deleteallbysupplierid')
        self.set_data(data)
        return self.req_put().content

    def update_item_stock(self, data):
        self.set_path('/api/supplier/item/stock')
        self.set_data(data)
        return self.req_put().content


