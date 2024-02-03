# -*- coding: utf-8 -*-
"""
Created on 2024/1/24.
@author: darklord
"""

import socket
import threading

from lib.db import ProxyManager


class TrafficForwardClient:
    def __init__(self, local_port):
        self.local_port = local_port
        self.proxy_manager = ProxyManager()

    def listen_and_forward(self):
        forward_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        forward_addr = ('localhost', int(self.local_port))
        forward_server.bind(forward_addr)
        forward_server.listen(5)

        print(f"[*] 正在监听 {forward_addr} ,等待其他程序发送数据")

        while True:
            proxy_url = self.proxy_manager.get_random_proxy_url()
            print(f"Current proxy: {proxy_url}")
            proxy_url = proxy_url.lstrip("socks5://")
            proxy_host, proxy_port = proxy_url.split(':')

            # 连接上游服务器
            server_addr = (proxy_host, int(proxy_port))

            try:
                upstream_conn = socket.create_connection(server_addr, timeout=15)

                downstream_conn, downstream_addr = forward_server.accept()
                threading.Thread(target=self.handle_conn, args=(downstream_conn, upstream_conn)).start()
            except Exception as msg:
                # print(msg)
                pass

    def handle_conn(self, downstream_conn, upstream_conn):
        try:
            threading.Thread(target=self.transport, args=(downstream_conn, upstream_conn)).start()

        except Exception as e:
            print(f"Error in handle_conn: {e}")

    def transport(self, data1, data2):
        try:
            # 控制线程的启动和停止,保持线程之间的协同工作
            stop_signal = threading.Event()

            def copy_data(src, dst):
                nonlocal stop_signal
                try:
                    while True:
                        data = src.recv(10240)
                        # print(f"接收到来自{src}的数据->{data}")
                        if not data:
                            break
                        dst.sendall(data)
                        # print(f"将来自{src}的数据->{data}发送给->{dst}")
                finally:
                    stop_signal.set()

            threading.Thread(target=copy_data, args=(data1, data2)).start()
            threading.Thread(target=copy_data, args=(data2, data1)).start()

            stop_signal.wait()

        except Exception as e:
            print(f"Error in transport: {e}")
