# -*- coding: utf-8 -*-
"""
Created on 2024/1/22.
@author: darklord
"""
import os
import random
import sqlite3
import threading
import time

import requests
from tqdm import tqdm


class ProxyChecker:
    def __init__(self):
        self.checked_db_cursor = None
        self.checked_db_connection = None
        self.checked_list = []
        self.lock = threading.Lock()
        self.checked_db = 'checked.db'
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "DNT": "1",
            "Referer": "https://www.baidu.com/"
        }

        # 检查数据库文件是否存在
        if os.path.exists(self.checked_db):
            # 如果存在，则删除数据库文件
            os.remove(self.checked_db)
            print(f"Deleted existing database file: {self.checked_db}")

    def random_agent(self):
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

    def random_check_site(self):
        site_list = [
            "http://myip.ipip.net/",
            "https://api.ip.sb/ip",
            "https://ip.3322.net/",
            "https://ip.qaros.com/",
            "https://icanhazip.com/",
            "https://api.ipify.org/",
            "http://httpbin.org/ip"
        ]
        return random.choice(site_list)

    def generate_headers(self):
        agent = self.random_agent()
        self.headers['User-Agent'] = str(agent)

        return self.headers

    def create_checked_db_database(self):
        # 创建代理URL表
        self.checked_db_connection = sqlite3.connect(self.checked_db)
        self.checked_db_cursor = self.checked_db_connection.cursor()

        self.checked_db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS proxy_urls (
                id INTEGER PRIMARY KEY,
                url TEXT UNIQUE
            )
        ''')

        self.checked_db_connection.commit()

    def connectivity_check(self, proxy_url):
        try:
            check_url = self.random_check_site()
            # print(F"Current check url: {check_url}")

            proxies = {"http": proxy_url, "https": proxy_url}
            start_time = time.time()
            # print(proxies)
            headers = self.generate_headers()
            response = requests.get(check_url, headers=headers, proxies=proxies, timeout=10)
            # print(response.text)
            elapsed_time = time.time() - start_time

            if response.status_code == 200:
                return response.text, int(elapsed_time), True
            else:
                return "", 0, False

        except requests.RequestException:
            return "", 0, False

    def write_to_checked_db(self, proxy_url):
        try:
            conn = sqlite3.connect(self.checked_db)
            cursor = conn.cursor()

            # 检查数据库中是否已存在相同的 URL
            cursor.execute('SELECT * FROM proxy_urls WHERE url = ?', (proxy_url,))
            existing_data = cursor.fetchone()

            if not existing_data:
                cursor.execute('INSERT INTO proxy_urls (url) VALUES (?)', (proxy_url,))
                conn.commit()
            else:
                print(f"URL {proxy_url} already exists in the checked database.")

            conn.close()
        except Exception as e:
            print(f"Error writing to checked database: {e}")

    def run(self, result, progress_bar):
        try:
            with self.lock:
                item = result.pop(0)
            while item:
                # proxy_url = item['url']
                proxy_url = item
                # print(f"Proxy_url: {proxy_url}")
                resp_body, timeout, avail = self.connectivity_check(proxy_url)
                # print(resp_body, timeout, avail)
                progress_bar.update(1)

                url = proxy_url.lstrip('socks5://')
                host, port = url.split(":")

                if host in resp_body:
                    # print(proxy_url)
                    with self.lock:
                        if proxy_url not in self.checked_list:
                            self.checked_list.append(proxy_url)
                        self.write_to_checked_db(proxy_url)
                else:
                    pass

                with self.lock:
                    if result:
                        item = result.pop(0)
                    else:
                        item = None
        except Exception as msg:
            print(f"Error in function run: {msg}")

    def start_check(self, result, threads_count):
        threads = []
        self.create_checked_db_database()
        # check_url = self.random_check_site()
        # print(F"Current check url: {check_url}")
        try:
            progress_bar = tqdm(total=len(result), desc="Checking Proxies", unit=" proxy_url")
            for i in range(threads_count):
                t = threading.Thread(target=self.run, args=(result, progress_bar))
                threads.append(t)
                t.start()

            for i in range(threads_count):
                threads[i].join()
        except Exception as msg:
            print(msg)
            return False

        progress_bar.close()

        print("Avail proxyurl:")
        for item in self.checked_list:
            print(item)
        print("----------------------------------------------------")
