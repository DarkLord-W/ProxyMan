# -*- coding: utf-8 -*-
"""
Created on 2024/1/23.
@author: darklord
"""
import random
import sqlite3
import threading
import time


class ProxyManager:
    def __init__(self):
        self.database_path = "checked.db"
        # self.database_path = "proxy_list.db"
        self.proxy_queue = []
        self.used_proxies = set()
        self.lock = threading.Lock()
        self.refresh_interval = 30  # 刷新代理队列的时间间隔，单位为秒
        self.last_refresh_time = 0

        # 初始化时加载代理列表
        self.refresh_proxy_queue()

        # 启动定时任务，定期刷新代理队列
        threading.Thread(target=self.schedule_refresh_proxy_queue).start()

    def release_proxy(self, proxy_url):
        with self.lock:
            # 在一段时间后释放代理，以便下次可以再次使用
            self.used_proxies.remove(proxy_url)

    def schedule_refresh_proxy_queue(self):
        while True:
            # 定时刷新代理队列
            time.sleep(self.refresh_interval)
            self.refresh_proxy_queue()

    def refresh_proxy_queue(self):
        try:
            with self.lock:
                # 连接数据库
                conn = sqlite3.connect(self.database_path)
                cursor = conn.cursor()

                # 从数据库查询未被短期未被使用的代理地址
                cursor.execute("SELECT * FROM proxy_urls WHERE url NOT IN (?)",
                               (",".join(self.used_proxies),))
                proxies = cursor.fetchall()
                # print(f"refresh_proxy_queue ->proxies -> {proxies} ")

                # 关闭数据库连接
                conn.close()

                # 更新代理队列
                self.proxy_queue = [f"{proxy[0]}:{proxy[1]}" for proxy in proxies]
                # print(f"refresh_proxy_queue ->self.proxy_queue -> {self.proxy_queue}")

                # 记录本次的刷新时间
                self.last_refresh_time = time.time()
        except Exception as e:
            print(f"Error refreshing proxy queue: {e}")

    def get_random_proxy_url(self):
        with self.lock:
            # 获取当前时间，检查是否需要刷新代理队列
            current_time = time.time()
            # 如果刷新时间的间隔已经超过定义的时间，则刷新代理队列
            if current_time - self.last_refresh_time > self.refresh_interval:
                self.refresh_proxy_queue()

            # 从代理队列中随机选择一个未使用的代理
            if self.proxy_queue:
                # 随即获取一个代理
                proxy_url = random.choice(self.proxy_queue)
                # [2:]是为了去掉序号，如：1:socks5://ip:port -> socks5://ip:port
                proxy_url = proxy_url[2:]
                # 将此代理添加到已使用代理(used_proxies)序列中
                self.used_proxies.add(proxy_url)
                # 延时一段时间后再次释放该代理
                threading.Timer(random.randint(1, 10), self.release_proxy, args=(proxy_url,)).start()
                # print(f"get_random_proxy_url -> proxy_url ->{proxy_url}")
                # print(proxy_url)
                return proxy_url
            else:
                return None

# proxy_manager = ProxyManager()
# proxy_manager.get_random_proxy_url()
