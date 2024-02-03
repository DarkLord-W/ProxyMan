# -*- coding: utf-8 -*-
"""
Created on 2024/1/24.
@author: darklord
"""

import argparse

from lib.check import ProxyChecker
from lib.crawler import FofaCrawler
from lib.forward import TrafficForwardClient

if __name__ == "__main__":
    paser = argparse.ArgumentParser(description="Proxy tool")
    paser.add_argument("-email", type=str, help="login email")
    paser.add_argument("-token", type=str, help="login token")
    paser.add_argument("-l", type=int, help="local listen port")
    paser.add_argument("-page", type=int, help="fofa request page")
    paser.add_argument("-t", type=int, help="thread: for the speed of check valid proxy url")
    paser.add_argument("-region", type=str, help="0:all  1:hk  2:abroad  default=0", default=0)
    paser.add_argument("-p", type=str, help="fofa request proxy  default=null", default="")

    args = paser.parse_args()

    if not (args.email and args.token):
        print("please input your email and token,such as '-email  email_account  -token token_value'")
    elif not args.l:
        print("please input listen port")
    elif not args.page:
        print("please input fofa request page")
    else:
        fofa_crawler = FofaCrawler()
        proxy_list = fofa_crawler.start_crawler(args.email, args.token, args.region, args.page, args.p)
        proxy_checker = ProxyChecker()
        proxy_checker.start_check(proxy_list, args.t)
        forward_client = TrafficForwardClient(args.l)
        forward_client.listen_and_forward()
