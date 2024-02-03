# ProxyMan

Automated rotation proxy forwarding tool

[中文版](./README_CN.md)

---

1.Download repository

```git
git clone https://github.com/DarkLord-W/ProxyMan.git
```

2.Install required  libraries

```bash
pip install -r requirements.txt
```

3.Run program

```python
❯ python main.py -h
usage: main.py [-h] [-email EMAIL] [-token TOKEN] [-l L] [-page PAGE] [-t T] [-region REGION] [-p P]

Proxy tool

options:
  -h, --help      show this help message and exit
  -email EMAIL    login email
  -token TOKEN    login token
  -l L            local listen port
  -page PAGE      fofa request page
  -t T            thread: for the speed of check valid proxy url
  -region REGION  0:all 1:hk 2:abroad default=0
  -p P            fofa request proxy default=null
```

```python
❯ python main.py -email YOUR_FOFA_EMAIL -token YOUR_FOFA_TOKEN -l PORT -page 10 -region 1 -t 100
Deleted existing database file: proxy_list.db
第1页
第1页获取100条数据
----------------------------------------
第2页
第2页获取100条数据
----------------------------------------
第3页
第3页获取100条数据
----------------------------------------
第4页
第4页获取100条数据
----------------------------------------
第5页
第5页获取100条数据
----------------------------------------
第6页
第6页获取100条数据
----------------------------------------
第7页
第7页获取100条数据
----------------------------------------
第8页
第8页获取100条数据
----------------------------------------
第9页
第9页获取100条数据
----------------------------------------
第10页
第10页获取73条数据
----------------------------------------
共获取973条数据

Deleted existing database file: checked.db
Checking Proxies: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████| 973/973 [00:34<00:00, 28.22 proxy_url/s]
Avail proxyurl:
socks5://4X.1X4.1XX.1XX:7777
socks5://XX.152.XX.X62:7777
socks5://XX.128.XX.177:1080
----------------------------------------------------
[*] 正在监听 ('localhost', 5678) ,等待其他程序发送数据
Current proxy: socks5://45.XXX.67.XX2:7777
```

At this point, the agent program has successfully obtained the agent data and started the corresponding data monitoring and forwarding service.

---

Set the proxy in the program that needs proxy, the format is as follows:

```
socks5://agent IP: listening port
```

For example, in this project, `test_requets.py` is used for testing:

```python
# Set proxy host ip
proxy_host = '127.0.0.1'
# The listening port of the agent to connect to
proxy_port = 5678

# Set proxy type to SOCKS5
proxies = {
    'http': f'socks5://{proxy_host}:{proxy_port}',
    'https': f'socks5://{proxy_host}:{proxy_port}'
}
```

Run `test_requets.py`:

```python
python test_requets.py 
Command:(start/stop) start
URL: http://myip.ipip.net/
成功获取页面内容:
当前 IP：43.xx.xxx9.185  来自于：中国 香港   tencent.com

Command:(start/stop) start
URL: http://myip.ipip.net/
成功获取页面内容:
当前 IP：x5.xxx.67.1xx  来自于：中国 香港   

Command:(start/stop) start
URL: http://myip.ipip.net/
成功获取页面内容:
当前 IP：xx.128.xx.177  来自于：中国 香港   tencent.com

Command:(start/stop) stop

进程已结束,退出代码0
```

---

**By the way, it is highly recommended to run it under linux.**

**just download it from kali.**

**and it is ready to eat after opening the lid.**

---

**And, I have to mention, FUCK YOU --- Windows!!!**
