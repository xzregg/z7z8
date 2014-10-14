# -*- coding: utf-8 -*-



import urllib
import urllib2
import sys,mechanize
from pyquery import PyQuery as pq
import time
import json
import pprint
import HTMLParser
html_parser = HTMLParser.HTMLParser()
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
from tornado.web import HTTPError, asynchronous
from tornado.httpclient import HTTPRequest
from tornado.options import define, options
import random
try:
    from tornado.curl_httpclient import CurlAsyncHTTPClient as AsyncHTTPClient
except ImportError:
    from tornado.simple_httpclient import SimpleAsyncHTTPClient as AsyncHTTPClient

DEBUG = False
if __name__ == '__main__':
    DEBUG = True
    
LOGIN_URL = 'https://meican.com/login'
LOGIN_DATA = {
    'username':'xiezhaorong@youai.com',
    'password':'123456',
}



class MeiCan(object):
    LOGIN_URL = 'https://meican.com/login'
    Address = u'芒果'
    Order_Menu_Names = [u'游爱 - 晚餐',u'游爱 - 午餐']
    #Order_Menu_Names = [u'游爱 - 晚餐']
    #Order_Restaurant = [u"鲜达", u"绿森林", "游爱早餐", u"山东老家", u"晚餐退餐", u"午餐退餐", u"佰荟餐饮"]
    #Order_Restaurant = [u'鲜达',u'山东老家']
    Order_Restaurant = [u'绿森林',u'鲜达',u'山东老家']
    
    def __init__(self,username='',password=''):
        br = mechanize.Browser()  
        #options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        #Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.username = username or LOGIN_DATA['username']
        self.password = password or  LOGIN_DATA['password']
        #debugging
        #br.set_debug_http(True)
        #br.set_debug_redirects(True)
        #br.set_debug_responses(True)
        
        #User-Agent (this is cheating, ok?)
        self.order_data = ''
        self.br = br
        self.pq = None
        self.menus = {} #
        self.week_menus = {}
        self.address = {}
        self.restaurants = {}
        self.order_token = ''
        self.url = {
                "save_tab_url":"",
               "delete_tab_url":"",
               "save_tab_last_used_time_url":"",
               "save_sort_order_url":"",
               "list_url_building":"",
               "list_url_location":"",
               "list_url_corp":"", #获取菜单的店铺
               "recommendation_url":"",
               "get_corp_info_url":"",
               "save_order_url":"/corps/savecorpcart",
               "address_url":"/application/getcartside",
               "order_url":"/corps/addcorpmemberorder"
               }
        self.token = 0
        self.corpIds = []
    
    def open_url(self,url,data=None,use_token=True,chunked=False):
        if use_token:
            self.token += 1
            url = '%s%stoken=%s' % (url,'&' if '?' in url else '?',self.token)
        if chunked:
            self.br.addheaders += [("X-Requested-With","XMLHttpRequest"),("Accept-Encoding","gzip,deflate,sdch")]
        r = self.br.open(url,data=data)
        html = r.read()
        return html.decode('utf-8')
      
    def random_choice_food(self,food_list):
        random_list = []
        for food_item in food_list:
            name,id,restaurants_name,date_id = food_item
            if restaurants_name in self.Order_Restaurant :
                if u'辣'  in name:
                    continue
                random_list.append(food_item)
        if len(random_list) == 0:
            random_list = food_list
        return random.choice(random_list)
        
    def random_order(self):
        for m_name in self.Order_Menu_Names:
            menu_obj = self.menus.get(m_name,'')
            if menu_obj:
                corpId = menu_obj.get('corpId','')
                menus = self.week_menus.get(m_name,{})
                if menus:
                    if DEBUG:
                        print m_name
                    for k,v in menus.iteritems():
                        random_food = self.random_choice_food(v)
                        random_food_id = random_food[1]
                        if DEBUG:
                            print random_food[2],k,random_food[0]
                        self.order(corpId, random_food_id)
                    self.corpIds.append(corpId)
        self.order_sure()
    
    def order_sure(self):
        order_url = self.url['order_url']
        save_url = self.url['save_order_url']
        address_id = self.address[self.Address]
        order_result = self.open_url(save_url, self.order_data,use_token=False,chunked=True)
        if DEBUG:
            print save_url,self.order_data
        #print order_result
        for corpId in self.corpIds :
            order_data = 'token=%s&corpAddressId=%s&corpId=%s' % (self.order_token,address_id,corpId)
            if DEBUG:
                print order_data
            result = self.open_url(order_url, order_data,use_token=False,chunked=True)
            json_data = self.update_token(result)
            if json_data.get('errorList',''):
                print '下单失败!'
            if DEBUG:
                print json_data
        self.order_data = ''

        
    def order(self,corpId,RevisionId):
        self.order_data += '&corpDishRevisionIdList[]=%s' % RevisionId
        self.order_data += '&corpDishCountList[]=1' 
        self.order_data += '&corpRefererList[]=restaurant'
        self.order_data += '&corpIdList[]=%s' % corpId

    def update_token(self,result_str):
        json_str = result_str[:result_str.find('<!--JH-->')]
        json_data = json.loads(json_str.strip())
        self.order_token = json_data.get('token',self.order_token)
        return json_data
    
    def login(self):
        r = self.br.open(self.LOGIN_URL)
        self.br.select_form(nr = 0)
        self.br['username'] = self.username
        self.br['password'] = self.password
        resp = self.br.submit()
        doc = resp.read()
        self.document_pq = pq(doc)
        self.order_token = self.document_pq('#corp_restaurant_form').attr('data-token')
        self.create_action_url()
        self.set_address()
        menus_item = self.document_pq('.menu_tab_middle a') #获取菜单
        self.create_menus(menus_item)
        self.print_attr()
        
    def print_attr(self):
        print json.dumps(self.week_menus,ensure_ascii=False)
        print json.dumps(self.menus,ensure_ascii=False)
        print json.dumps(self.address,ensure_ascii=False)
        print json.dumps(self.restaurants.keys(),ensure_ascii=False)
        print self.order_token

                      
    def set_address(self):
        '''获取下单位置
        '''
        resp = self.open_url(url=self.url['address_url'],use_token=False,chunked=True)
        document_pq = pq(resp)
        for address in document_pq('div[data-corp_address_id]'):
            pq_address = pq(address)
            self.address[pq_address.text()] = pq_address.attr('data-corp_address_id')
        
    def create_action_url(self):
        url_cont = self.document_pq('#menu_tab')
        for url_name in self.url.keys():
            self.url[url_name] = url_cont.attr('data-%s'%url_name ) or self.url.get(url_name)

    def get_food_for_restaurant(self,restaurant,menu_name):
        url = restaurant.get('url','')
        restaurants_name = restaurant.get('name','')
        if url:
            foods_html = self.open_url(url)
            pq_foods = pq(foods_html)
            food_map= {}
            for food in pq_foods('table[data-rev]'):
                pq_food =  pq(food)
                week_food_name = pq_food.attr('data-name')
                week_food_name_sp = week_food_name.split('/')
                if len(week_food_name_sp) == 2:
                    week,food_name = week_food_name_sp[:2]
                    food_map.setdefault(week,{})
                    food_id = pq_food.attr('data-rev')
                    food_data_id = pq_food.attr('data-id')
                    food_map[week].setdefault(food_name,food_id)
                    
                    self.week_menus.setdefault(menu_name,{})
                    self.week_menus[menu_name].setdefault(week,[])
                    food_item = (food_name,food_id,restaurants_name,food_data_id)
                    self.week_menus[menu_name][week].append(food_item)
            self.restaurants[restaurants_name] = food_map
            return food_map
        return {}
    
    def create_menus(self,menus_item):
        for m in  menus_item:
            m_pq = pq(m)
            if m_pq.attr('data-uuid'):
                menu = {}
                corpId = m_pq.attr('data-corp_id')
                menu_name = m_pq.text()
                menu['corpId'] = corpId
                restaurant_list = self.open_url('%s?corpId=%s' % (self.url['list_url_corp'],corpId))
                restaurant_list = json.loads(restaurant_list)
                restaurants = restaurant_list.get('searchResultList',[])
                for restaurant in restaurants:
                    restaurant['foods'] = self.get_food_for_restaurant(restaurant,menu_name) 
                menu['restaurants'] = restaurants
                self.menus[menu_name] = menu
    
    
class DianCanHandler(tornado.web.RequestHandler):
    def get(self):
        return self.post()
    
    def post(self):
        pass
    
    
def run_web():
    define("port", default=9001, help="run on the given port", type=int)
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/proxy_qq_pay$", DianCanHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    mc = MeiCan()
    mc.login()
    mc.random_order()

#    mc1 = MeiCan('xiexiaoling@youai.com','123456')
#    mc1.login()
#    mc1.random_order()
    
    mc1 = MeiCan('fanjunliang@youai.com','123456')
    mc1.login()
    mc1.random_order()
#    mc1 = MeiCan('zhaochufan@youai.com','123456')
#    mc1.login()
#    mc1.random_order()

