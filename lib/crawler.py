# -*- coding: utf-8 -*-
"""
Created on 2024/1/19.
@author: darklord
"""

import base64
import json
import os
import sqlite3

import requests


# Fofa响应数据格式定义
class Fofa_Api_Response:
    def __init__(self):
        self.error = False
        self.mode = ""
        self.page = 0
        self.query = ""
        self.results = []
        self.size = 0


class FofaCrawler:
    def __init__(self):
        # SQLite数据库连接
        self.db_file = 'proxy_list.db'
        self.db_connection = None
        self.db_cursor = None

        # 检查数据库文件是否存在
        if os.path.exists(self.db_file):
            # 如果存在，则删除数据库文件
            os.remove(self.db_file)
            print(f"Deleted existing database file: {self.db_file}")

        # 代理列表
        self.proxy_list = []
        self.crawl_done = []

    def create_database(self):
        # 创建代理URL表
        self.db_connection = sqlite3.connect(self.db_file)
        self.db_cursor = self.db_connection.cursor()

        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS proxy_urls (
                id INTEGER PRIMARY KEY,
                url TEXT UNIQUE
            )
        ''')

        self.db_connection.commit()

    def storage_proxy_url(self, url):
        # 将代理URL存储到SQLite数据库
        try:
            # 在插入之前检查 url 是否已经存在
            self.db_cursor.execute('SELECT * FROM proxy_urls WHERE url = ?', (url,))
            existing_record = self.db_cursor.fetchone()

            if existing_record:
                pass
            else:
                # 如果不存在，则执行插入操作
                self.db_cursor.execute(
                    'INSERT INTO proxy_urls (url) VALUES (?)',
                    (url,))
                self.db_connection.commit()
                # print(f"The URL '{url}' has been inserted into the database.")
                # 将URL添加到代理列表，避免重复
                if url not in self.proxy_list:
                    self.proxy_list.append(url)

        except sqlite3.Error as msg:
            print(f"SQLite error: {msg}")

    def run(self, fofa_api_key, fofa_email, rule, page_num, proxy):
        url = "https://fofa.info/api/v1/search/all"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        params = {
            "email": fofa_email,
            "key": fofa_api_key,
            "qbase64": base64.b64encode(rule.encode()).decode(),
            "size": "100",
            "page": str(page_num),
            "fields": "host,title,ip,domain,port,country,city,server,protocol",
        }

        if proxy:
            proxies = {"http": proxy, "https": proxy}
        else:
            proxies = {}

        try:
            response = requests.get(url, params=params, headers=headers, proxies=proxies, timeout=10, verify=True)
        except requests.RequestException as msg:
            return msg

        res = Fofa_Api_Response()
        try:
            res.__dict__ = json.loads(response.text)
        except json.JSONDecodeError as msg:
            return msg

        print(f"第{res.page}页")
        print(f"第{res.page}页获取{len(res.results)}条数据")
        print("----------------------------------------")

        for value in res.results:
            host = value[0]
            self.storage_proxy_url("socks5://%s" % host)

    def start_crawler(self, fofa_email, fofa_api_key, region, page_count, proxy):
        self.create_database()

        rule_set = {
            "0": 'protocol=="socks5" && "Version:5 Method:No Authentication(0x00)" && after="2023-1-18"',
            "1": 'protocol=="socks5" && "Version:5 Method:No Authentication(0x00)" && after="2023-1-18" && country="CN" && region="HK"',
            "2": 'protocol=="socks5" && "Version:5 Method:No Authentication(0x00)" && after="2023-1-18" && country!="CN"'
        }
        rule = rule_set[region]

        for i in range(1, page_count + 1):
            self.run(fofa_api_key, fofa_email, rule, i, proxy)

        print(f"共获取{len(self.proxy_list)}条数据\n")
        # print("--------------------------")
        self.db_connection.close()

        return self.proxy_list
        # print("All Done!!!")
