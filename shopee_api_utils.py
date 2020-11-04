from requests import Request, Session, exceptions
from async_class import AsyncClass
import aiohttp
import json
import time
import hmac
import hashlib
import requests

class ShopeeApiUtils():
    UNLIST_URL = 'https://partner.shopeemobile.com/api/v1/items/unlist'
    UPDATE_STOCK_URL = 'https://partner.shopeemobile.com/api/v1/items/update_stock'
    GET_CATEGORIES_URL = 'https://partner.shopeemobile.com/api/v1/item/categories/get'
    GET_ATTRIBUTES_URL = 'https://partner.shopeemobile.com/api/v1/item/attributes/get'
    GET_ITEM_DETAIL_URL = 'https://partner.shopeemobile.com/api/v1/item/get'
    GET_SHOP_CATEGORIES_URL = 'https://partner.shopeemobile.com/api/v1/shop_categorys/get'
    GET_ORDER_DETAILS_URL = 'https://partner.shopeemobile.com/api/v1/orders/detail'
    GET_ORDER_ESCROW_DETAILS_URL = 'https://partner.shopeemobile.com/api/v1/orders/my_income'
    GET_ORDER_INCOME_URL = 'https://partner.shopeemobile.com/api/v1/orders/income'

    def __init__(self, partner_id: int, shop_id: int, secret_key: str):
        self.partner_id = partner_id
        self.shop_id = shop_id
        self.secret_key = secret_key

    def get_order_escrow_detail(self, ordersn):
        url = self.GET_ORDER_ESCROW_DETAILS_URL
        body = self.get_default_body()
        body['ordersn'] = ordersn

        return self.execute_request(url, body)

    def get_order_income(self, ordersn):
        url = self.GET_ORDER_INCOME_URL
        body = self.get_default_body()
        body['ordersn'] = ordersn
        
        return self.execute_request(url, body)

    def get_single_order_details(self, ordersn):
        url = self.GET_ORDER_DETAILS_URL
        body = self.get_default_body()
        body['ordersn_list'] = [ordersn]
        
        return self.execute_request(url, body)

    def get_shop_categories(self, offset=0, entries_per_page=100):
        url = self.GET_SHOP_CATEGORIES_URL
        body = self.get_default_body()
        body['pagination_offset'] = offset
        body['pagination_entries_per_page'] = entries_per_page
        
        return self.execute_request(url, body)

    def get_item_detail(self, item_id):
        url = self.GET_ITEM_DETAIL_URL
        body = self.get_default_body()
        body['item_id'] = item_id
        
        return self.execute_request(url, body)

    def get_attributes(self, cat_id):
        url = self.GET_ATTRIBUTES_URL
        body = self.get_default_body()
        body['category_id'] = cat_id
        
        return self.execute_request(url, body)

    def get_categories(self):
        url = self.GET_CATEGORIES_URL
        body = self.get_default_body()
        
        return self.execute_request(url, body)

    def unlist_batch_items(self, items):
        url = self.UNLIST_URL
        body = self.get_default_body()
        body['items'] = items
        
        return self.execute_request(url, body)

    def update_stock(self, item_id, stock):
        url = self.UNLIST_URL
        body = self.get_default_body()
        body['item_id'] = item_id
        body['stock'] = stock
        
        return self.execute_request(url, body)

    # async def update_stock_async(self, item_id, stock, session):
    #     url = self.UPDATE_STOCK_URL
    #     body = self.get_default_body()
    #     body['item_id'] = item_id
    #     body['stock'] = stock
    #     headers = self.get_headers(url, body)

    #     async with session.post(url=url, data=body, headers=headers) as response:
    #         data = await response.text()
    #         print(data)
    #         return data, response.status

    def execute_request(self, url, body):
        headers = self.get_headers(url, body)
        response = requests.post(url=url, data=json.dumps(body), headers=headers)
        return response.json()

    def get_headers(self, url, body):
        return {
            'Content-Type' : 'application/json',
            'Authorization' : self._sign(url, json.dumps(body))
        }

    def get_default_body(self):
        return {
            'partner_id': self.partner_id,
            'shopid': self.shop_id,
            'timestamp': self._get_timestamp()
        }

    def _sign(self, url, body):
        bs = url + "|" + body
        dig = hmac.new(ShopeeApiUtils.SECRET_KEY.encode(), msg=bs.encode(),
                       digestmod=hashlib.sha256).hexdigest()
        return dig

    def _get_timestamp(self):
        timestamp = int(time.time())
        return timestamp
