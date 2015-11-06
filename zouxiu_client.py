# -*- coding: utf-8 *-
from baseclient import *

class Zouxiu_client(Baseclient):

    def getitem(self, data):
        self.set_path('/api/supplier/item/getitem')
        self.set_data(data)
        return self.req_put().content

    def product(self, data):
        self.set_path('/api/supplier/product')
        self.set_data(data)
        return self.req_post().content

    def remove_all_products(self, data):
        self.set_path('/api/supplier/delete/deleteallbysupplierid')
        self.set_data(data)
        return self.req_put().content

