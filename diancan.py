#coding:utf-8



import urllib
import urllib2
import sys,mechanize
from pyquery import PyQuery as pq
import time


LOGIN_URL = 'https://meican.com/login'
LOGIN_DATA = {
    'username':'xiezhaorong@youai.com',
    'password':'123456',
    'remember':'true',
    'corpNamespace':'503271',
}

html = u'''
{"status":1}

<!--JH-->
<div>
            <div style="display:none" id="async_data_by_corp">
                                        <ul class="one_corp_data corp_925987 corp_952" data-id="952" data-namespace="925987">
        <li class="corp_address_list">
            <div class="corp_address_list_952 corp_address_list_925987">
                                    <div data-corp_address_id="1109" class="pick_up_location_of_1109 one_pick_up_location first">
                        财务
                    </div>
                                    <div data-corp_address_id="1115" class="pick_up_location_of_1115 one_pick_up_location">
                        新小蜜蜂
                    </div>
                                    <div data-corp_address_id="1125" class="pick_up_location_of_1125 one_pick_up_location">
                        小李飞刀
                    </div>
                                    <div data-corp_address_id="1126" class="pick_up_location_of_1126 one_pick_up_location">
                        蜘蛛
                    </div>
                                    <div data-corp_address_id="1127" class="pick_up_location_of_1127 one_pick_up_location">
                        灵动
                    </div>
                                    <div data-corp_address_id="1128" class="pick_up_location_of_1128 one_pick_up_location">
                        光束
                    </div>
                                    <div data-corp_address_id="1129" class="pick_up_location_of_1129 one_pick_up_location">
                        行政
                    </div>
                                    <div data-corp_address_id="1130" class="pick_up_location_of_1130 one_pick_up_location">
                        星辰
                    </div>
                                    <div data-corp_address_id="1131" class="pick_up_location_of_1131 one_pick_up_location">
                        旗乐
                    </div>
                                    <div data-corp_address_id="1132" class="pick_up_location_of_1132 one_pick_up_location">
                        同人
                    </div>
                                    <div data-corp_address_id="1133" class="pick_up_location_of_1133 one_pick_up_location">
                        游趣
                    </div>
                                    <div data-corp_address_id="1134" class="pick_up_location_of_1134 one_pick_up_location">
                        千云
                    </div>
                                    <div data-corp_address_id="1135" class="pick_up_location_of_1135 one_pick_up_location">
                        蜂鸟
                    </div>
                                    <div data-corp_address_id="1136" class="pick_up_location_of_1136 one_pick_up_location selected">
                        芒果
                    </div>
                                    <div data-corp_address_id="1137" class="pick_up_location_of_1137 one_pick_up_location">
                        19层
                    </div>
                                    <div data-corp_address_id="1138" class="pick_up_location_of_1138 one_pick_up_location">
                        剑舞
                    </div>
                                    <div data-corp_address_id="1139" class="pick_up_location_of_1139 one_pick_up_location last">
                        智慧
                    </div>
                            </div>
        </li>
    </ul>
                                        <ul class="one_corp_data corp_503271 corp_953" data-id="953" data-namespace="503271">
        <li class="corp_address_list">
            <div class="corp_address_list_953 corp_address_list_503271">
                                    <div data-corp_address_id="1110" class="pick_up_location_of_1110 one_pick_up_location first">
                        财务
                    </div>
                                    <div data-corp_address_id="1116" class="pick_up_location_of_1116 one_pick_up_location">
                        小蜜蜂
                    </div>
                                    <div data-corp_address_id="1140" class="pick_up_location_of_1140 one_pick_up_location">
                        小李飞刀
                    </div>
                                    <div data-corp_address_id="1141" class="pick_up_location_of_1141 one_pick_up_location">
                        蜘蛛
                    </div>
                                    <div data-corp_address_id="1142" class="pick_up_location_of_1142 one_pick_up_location">
                        灵动
                    </div>
                                    <div data-corp_address_id="1144" class="pick_up_location_of_1144 one_pick_up_location">
                        行政
                    </div>
                                    <div data-corp_address_id="1145" class="pick_up_location_of_1145 one_pick_up_location">
                        星辰
                    </div>
                                    <div data-corp_address_id="1146" class="pick_up_location_of_1146 one_pick_up_location">
                        旗乐
                    </div>
                                    <div data-corp_address_id="1147" class="pick_up_location_of_1147 one_pick_up_location">
                        同人
                    </div>
                                    <div data-corp_address_id="1148" class="pick_up_location_of_1148 one_pick_up_location">
                        游趣
                    </div>
                                    <div data-corp_address_id="1149" class="pick_up_location_of_1149 one_pick_up_location">
                        千云
                    </div>
                                    <div data-corp_address_id="1150" class="pick_up_location_of_1150 one_pick_up_location">
                        蜂鸟
                    </div>
                                    <div data-corp_address_id="1151" class="pick_up_location_of_1151 one_pick_up_location selected">
                        芒果
                    </div>
                                    <div data-corp_address_id="1152" class="pick_up_location_of_1152 one_pick_up_location">
                        19层
                    </div>
                                    <div data-corp_address_id="1153" class="pick_up_location_of_1153 one_pick_up_location">
                        剑舞
                    </div>
                                    <div data-corp_address_id="1154" class="pick_up_location_of_1154 one_pick_up_location last">
                        智慧
                    </div>
                            </div>
        </li>
    </ul>
                                        <ul class="one_corp_data corp_316323 corp_956" data-id="956" data-namespace="316323">
        <li class="corp_address_list">
            <div class="corp_address_list_956 corp_address_list_316323">
                                    <div data-corp_address_id="1113" class="pick_up_location_of_1113 one_pick_up_location first">
                        财务
                    </div>
                                    <div data-corp_address_id="1187" class="pick_up_location_of_1187 one_pick_up_location">
                        新小蜜蜂
                    </div>
                                    <div data-corp_address_id="1188" class="pick_up_location_of_1188 one_pick_up_location">
                        小李飞刀
                    </div>
                                    <div data-corp_address_id="1189" class="pick_up_location_of_1189 one_pick_up_location">
                        蜘蛛
                    </div>
                                    <div data-corp_address_id="1190" class="pick_up_location_of_1190 one_pick_up_location">
                        灵动
                    </div>
                                    <div data-corp_address_id="1191" class="pick_up_location_of_1191 one_pick_up_location">
                        光束
                    </div>
                                    <div data-corp_address_id="1192" class="pick_up_location_of_1192 one_pick_up_location">
                        行政
                    </div>
                                    <div data-corp_address_id="1193" class="pick_up_location_of_1193 one_pick_up_location">
                        星辰
                    </div>
                                    <div data-corp_address_id="1194" class="pick_up_location_of_1194 one_pick_up_location">
                        旗乐
                    </div>
                                    <div data-corp_address_id="1195" class="pick_up_location_of_1195 one_pick_up_location">
                        同人
                    </div>
                                    <div data-corp_address_id="1196" class="pick_up_location_of_1196 one_pick_up_location">
                        游趣
                    </div>
                                    <div data-corp_address_id="1197" class="pick_up_location_of_1197 one_pick_up_location">
                        千云
                    </div>
                                    <div data-corp_address_id="1198" class="pick_up_location_of_1198 one_pick_up_location">
                        蜂鸟
                    </div>
                                    <div data-corp_address_id="1199" class="pick_up_location_of_1199 one_pick_up_location selected">
                        芒果
                    </div>
                                    <div data-corp_address_id="1200" class="pick_up_location_of_1200 one_pick_up_location">
                        19层
                    </div>
                                    <div data-corp_address_id="1201" class="pick_up_location_of_1201 one_pick_up_location">
                        剑舞
                    </div>
                                    <div data-corp_address_id="1202" class="pick_up_location_of_1202 one_pick_up_location last">
                        智慧
                    </div>
                            </div>
        </li>
    </ul>
                                        <ul class="one_corp_data corp_710894 corp_1053" data-id="1053" data-namespace="710894">
        <li class="corp_address_list">
            <div class="corp_address_list_1053 corp_address_list_710894">
                                    <div data-corp_address_id="1322" class="pick_up_location_of_1322 one_pick_up_location first">
                        财务
                    </div>
                                    <div data-corp_address_id="1323" class="pick_up_location_of_1323 one_pick_up_location">
                        小蜜蜂
                    </div>
                                    <div data-corp_address_id="1324" class="pick_up_location_of_1324 one_pick_up_location">
                        小李飞刀
                    </div>
                                    <div data-corp_address_id="1325" class="pick_up_location_of_1325 one_pick_up_location">
                        蜘蛛
                    </div>
                                    <div data-corp_address_id="1326" class="pick_up_location_of_1326 one_pick_up_location">
                        灵动
                    </div>
                                    <div data-corp_address_id="1327" class="pick_up_location_of_1327 one_pick_up_location">
                        光束
                    </div>
                                    <div data-corp_address_id="1328" class="pick_up_location_of_1328 one_pick_up_location">
                        行政
                    </div>
                                    <div data-corp_address_id="1329" class="pick_up_location_of_1329 one_pick_up_location">
                        星辰
                    </div>
                                    <div data-corp_address_id="1330" class="pick_up_location_of_1330 one_pick_up_location">
                        旗乐
                    </div>
                                    <div data-corp_address_id="1331" class="pick_up_location_of_1331 one_pick_up_location">
                        同人
                    </div>
                                    <div data-corp_address_id="1332" class="pick_up_location_of_1332 one_pick_up_location">
                        游趣
                    </div>
                                    <div data-corp_address_id="1333" class="pick_up_location_of_1333 one_pick_up_location">
                        千云
                    </div>
                                    <div data-corp_address_id="1334" class="pick_up_location_of_1334 one_pick_up_location">
                        蜂鸟
                    </div>
                                    <div data-corp_address_id="1335" class="pick_up_location_of_1335 one_pick_up_location selected">
                        芒果
                    </div>
                                    <div data-corp_address_id="1336" class="pick_up_location_of_1336 one_pick_up_location">
                        19层
                    </div>
                                    <div data-corp_address_id="1337" class="pick_up_location_of_1337 one_pick_up_location">
                        剑舞
                    </div>
                                    <div data-corp_address_id="1338" class="pick_up_location_of_1338 one_pick_up_location last">
                        智慧
                    </div>
                            </div>
        </li>
    </ul>
                            </div>
            <div style="display:none" id="async_data_by_corp_order">
                            </div>
            <div style="display:none" id="async_data_by_user_order">
                            </div>
            <div style="display:none" id="async_data_by_restaurant">
                            </div>
            <div style="display:none" id="async_cart_json">
                {
    "cartDishItemList":[
            ],
    "cartDiscountItemList":[
            ],
    "corpCartDishItemList":[
                    {
                                                    "dishId":19654731,
                    "corpId":956,
                    "corpName":"\u6E38\u7231-\u665A\u9910",
                    "corpOrderRestaurantClosed": false,
                    "shortName":"\u6E38\u7231-\u665A\u9910",
                    "showPrice":true,
                    "dishRevisionId":30115706,
                    "restaurantId":35542,
                    "restaurantName":"\u5C71\u4E1C\u8001\u5BB6",
                    "noServiceBuildingList":"|",
                    "denyOrder":false,
                    "restaurantRevisionId": 384855,
                    "restaurantUuid":"5e164b",
                    "referer":"restaurant",
                    "deliveryTime":40,
                    "acceptPrepay":false,
                    "providesDeliveryService":true,
                    "temporaryClosed":false,                    
                    "restaurantRemoved":false,                    
                    "userDiscount":0,
                    "deliveryFee":null,
                    "minimumOrder":null,
                    "name":"\u56DB/\u714E\u997A",
                    "discountIdList": [
                                                0
                    ],
                    "price":12,
                    "priceString":null,
                    "count":1,
                    "stockCount":null
                            }
                        ]
}
            </div>
            <div style="display:none" id="async_promotion_data">
                            </div>
</div>'''
def get_food():
    food_map= {}
    document_pq=pq(html)
    for food in document_pq('table[data-rev]'):
        pq_food =  pq(food)
        week_food_name = pq_food.attr('data-name')
        week,food_name= week_food_name.split('/')
        food_map.setdefault(week,{})
        food_map[week].setdefault(food_name,pq_food.attr('data-rev'))
    
    print food_map
    
def get_address():
    document_pq=pq(html)
    address_map = {}
    for address in document_pq('div[data-corp_address_id]'):
        pq_address = pq(address)
        address_map[pq_address.text()] = pq_address.attr('data-corp_address_id')
    for k,v in address_map.iteritems():
        print k,v
if __name__ == '__main__':
    get_address()