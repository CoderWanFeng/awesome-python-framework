# Python电子书：http://t.cn/A6tMNzuI
# Python交流群：http://t.cn/A65MiFvH
import requests
from datetime import datetime

# 配置参数
# 协议
scheme = 'http'
# 主机地址
host = 'kxyy.ledu360.com'
# 请求头
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}

timeout = 3


def req(method, url, params):
    try:
        return requests.request(method, scheme + "://" + host + "/" + url, headers=headers, params=params,
                                timeout=timeout)
    except:
        print("时间：", str(datetime.now()), "---> 请求" + url + " 超时!", "数据源为：" + params['source'])
        return None
