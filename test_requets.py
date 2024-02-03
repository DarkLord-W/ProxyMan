# -*- coding:utf-8 -*-

# 该脚本用于简单测试代理程序有效性
import random

import requests

# 设置代理主机ip
proxy_host = '127.0.0.1'
# 要连接到的代理程序的监听端口
proxy_port = 5678

# 设置代理类型为 SOCKS5
proxies = {
    'http': f'socks5://{proxy_host}:{proxy_port}',
    'https': f'socks5://{proxy_host}:{proxy_port}'
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "DNT": "1",
    "Referer": "https://www.baidu.com/"
}


# 设置随机ua
def random_agent():
    user_agent_list = [
        {'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)'},
        {
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'},
        {'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; en) Opera 11.00'},
        {
            'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.0.2) Gecko/2008092313 Ubuntu/8.04 (hardy) Firefox/3.0.2'},
        {
            'Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.1.15) Gecko/20101027 Fedora/3.5.15-1.fc12 Firefox/3.5.15'},
        {
            'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.551.0 Safari/534.10'},
        {'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.2) Gecko/2008092809 Gentoo Firefox/3.0.2'},
        {
            'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.544.0'},
        {'Opera/9.10 (Windows NT 5.2; U; en)'},
        {
            'Mozilla/5.0 (iPhone; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko)'},
        {'Opera/9.80 (X11; U; Linux i686; en-US; rv:1.9.2.3) Presto/2.2.15 Version/10.10'},
        {
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5'},
        {'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9b3) Gecko/2008020514 Firefox/3.0b3'},
        {
            'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; fr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16'},
        {
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20'},
        {
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)'},
        {'Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux x86_64; en) Opera 9.60'},
        {
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.366.0 Safari/533.4'},
        {'Mozilla/5.0 (Windows NT 6.0; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.51'}
    ]
    return random.choice(user_agent_list)


agent = random_agent()
headers['User-Agent'] = str(agent)


# 测试URL
# url = "http://myip.ipip.net/"
# "->response:当前 IP：8.136.xxx.26  来自于：中国 浙江 杭州  阿里云"

# url = 'https://api.ipify.org/'

# url = "http://httpbin.org/ip"


def test(url):
    try:
        # # 创建 SOCKS5 连接
        # proxy_connection = socks.create_connection((proxy_host, proxy_port), proxy_type=socks.SOCKS5)

        # 使用代理发送请求
        response = requests.get(url, headers=headers, proxies=proxies, timeout=15)

        # 检查请求是否成功
        if response.status_code == 200:
            print("成功获取页面内容:")
            print(response.text)
        else:
            print(f"请求失败，状态码: {response.status_code}")

    except requests.RequestException as e:
        print(f"请求发生异常: {e}")


# finally:
#     # 记得关闭 SOCKS5 连接
#     proxy_connection.close()


while True:
    flag = input("Command:(start/stop) ")
    if flag == "start":
        url = input("URL: ")
        test(url)
    elif flag == "stop":
        break
