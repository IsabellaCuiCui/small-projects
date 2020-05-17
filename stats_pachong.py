#按照教程，爬取国家统计局价格指数数据
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import time
import json

#解析网页
def getTime():
    return int(round(time.time() * 1000))

url = 'http://data.stats.gov.cn/easyquery.htm?cn=A01'
headers={'User-Agent':'Mozilla/5.0(Windows;U;Windows NT6.1;en-US;rv:1.9.1.6) Geko/20091201 Firefox/3.5.6'}
key = {}
key['m'] = 'QueryData'
key['dbcode'] = 'hgyd'
key['rowcode'] = 'zb'
key['colcode'] = 'sj'
key['wds'] = '[]'
key['dfwds'] = '[{"wdcode":"sj","valuecode":"LAST13"}]'
key['k1'] = str(getTime())
r = requests.get(url, headers = headers, params = key)
js = json.loads(r.text)

#解析js内容
length=len(js['returndata']['datanodes'])
def getList(length):
    List=[]
    for i in range(length):
        List.append(eval(js['returndata']['datanodes'][i]['data']['strdata']))
    return List
lst = getList(length)

#将输出的结果结构化展示
array=np.array(lst).reshape(9,13)
df=pd.DataFrame(array)

#DataFrame行列重命名
df.columns = ['2020年4月','2020年3月','2020年2月','2020年1月','2019年12月','2019年11月','2019年10月','2019年9月','2019年8月','2019年7月','2019年6月','2019年5月','2019年4月']
df.index = ['居民消费价格指数（上年同月=100）',
            '食品烟酒类居民消费价格指数（上年同月=100）',
            '衣着类居民消费价格指数（上年同月=100）',
            '居住类居民消费价格指数（上年同月=100）',
            '生活用品及服务类居民消费价格指数（上年同月=100）',
            '交通和通信类居民消费价格指数（上年同月=100）',
            '教育文化和娱乐类居民消费价格指数（上年同月=100）',
            '医疗保健类居民消费价格指数（上年同月=100）',
            '其他用品和服务类居民消费价格指数（上年同月=100）']
print(df)
