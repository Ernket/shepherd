'''
api：https://censys.io/api
文档：https://censys-python.readthedocs.io/en/stable/
例子：https://github.com/censys/censys-python/tree/main/examples
'''


import requests
import json
import time
import re
from threading import Thread
from queue import Queue
import threading
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import configparser
from tqdm import *
from colorama import Fore
import chardet


# cf.read("../../../../iniFile/config.ini") # 测试
# secs = cf.sections()


TIMEOUT = 10
title_patten = re.compile('<title>(.*)?</title>', re.IGNORECASE)        # 忽略大小写


def censysApi(domain,censysuid,censyssecret):
    censysIPS = []
    UID=censysuid
    SECRET=censyssecret
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    #https://search.censys.io/api/v2/hosts/search?q=szpt.edu.cn&per_page=50&virtual_hosts=INCLUDE
    search_url="https://search.censys.io/api/v2/hosts/search?q={}&per_page=100&virtual_hosts=INCLUDE".format(domain)
    try:
        req = requests.get(search_url, auth=(UID, SECRET), headers=headers, timeout=TIMEOUT)
        result=json.loads(req.text)
        tmp_ips=[]
        result=result.get('result')
        hits=result.get('hits')
        for i in hits: 
            tmp_ip=i.get('ip')
            tmp_ips.append(tmp_ip)

    except Exception as e:
        print(e)
        pass
    return tmp_ips


class Detect(threading.Thread):
    name = 'Host碰撞'

    def __init__(self, hostIPS_q, hostCollideResult):
        threading.Thread.__init__(self)
        self.hostIPS_q = hostIPS_q
        self.hostCollideResult = hostCollideResult


    def run(self):
        while not self.hostIPS_q.empty():
            host, ip = self.hostIPS_q.get()

            self.attack(host, ip)

            self.hostIPS_q.task_done()

    def get_title(self, res):
        cont = res.content
        # 获取网页的编码格式
        charset = chardet.detect(cont)['encoding']
        # 对各种编码情况进行判断
        html_doc = cont.decode(charset)
        title = re.search('<title>(.*)</title>', html_doc).group(1)
        return title

    def attack(self, host, ip):
        headers = {'Host': host,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        headers2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        urls = ["http://{}".format(ip), "https://{}".format(ip)]
        for url in urls:
            print("正在爆破host: {} url: {}".format(host,url))
            try:
                res = requests.get(url=url, headers=headers, verify=False, timeout=TIMEOUT)
                res2 = requests.get(url=url, headers=headers2, verify=False, timeout=TIMEOUT)
                title = self.get_title(res)
                title2 = self.get_title(res2)
                # 过滤直接访问IP也是正常响应，例如：host, ip = ["apitest.mobile.meituan.com", "47.108.170.229"]
                if res2.status_code != 200:
                    code = res.status_code
                    if code != 502 and code != 400:
                        print("[{}] {} {} {} {}".format(code, url, host, title, title2))
                        self.hostCollideResult.append([host, url, code, title, title2])
            except Exception as e:
                pass


# 判断是否是内网IP
def is_internal_ip(ip):
    ip_list = str(ip).split('.')
    if ip_list[0] == '10' or ip_list[0] == '127':
        return True
    elif ip_list[0] == '172' and 15 < int(ip_list[1]) < 32:
        return True
    elif ip_list[0] == '192' and ip_list[1] == '168':
        return True
    else:
        return False



# host碰撞
def run_hostCollide(domain, Subdomains_ips,all_config):
    hostCollideResult = []
    censysIPS = []
    allIps = []

    # 自域名解析的A记录是内网IP
    internal_ip_Subdomains = []
    for ip in Subdomains_ips.keys():
        #ip=Subdomains_ips[subdomain]
        #print(type(ip))
        if Subdomains_ips[ip]:
            subdomain=Subdomains_ips[ip]
            if is_internal_ip(str(ip)):
                internal_ip_Subdomains.append(subdomain)
            allIps.append(ip)

    censysuid=all_config.get('censys').get('censys_api')
    censyssecret=all_config.get('censys').get('censys_secret')

    censysIPS = censysApi(domain,censysuid,censyssecret)
    print('cesys api : {} 共 {} 个解析出来的IP'.format(domain, len(censysIPS)))

    for ip in censysIPS:
        if is_internal_ip(str(ip)):
            internal_ip_Subdomains.append(subdomain)

    print("共有{}个子域名的A记录是内网IP".format(len(internal_ip_Subdomains)))
    for _ in internal_ip_Subdomains:
        print(_)

    if len(internal_ip_Subdomains) != 0:

        allIps.extend(censysIPS)
        allIps = list(set(allIps))
        print('共 {} 个IP'.format(len(allIps)))

        # 避免太多的子域名去碰撞
        if len(internal_ip_Subdomains) > 5:
            internal_ip_Subdomains = internal_ip_Subdomains[:5]

        hostIPS_q = Queue(-1)
        for ip in allIps:
            for host in internal_ip_Subdomains:
                hostIPS_q.put([host, ip])

        threads = []
        thread_num = 100  # 漏洞检测的线程数目

        for num in range(1, thread_num + 1):
            t = Detect(hostIPS_q, hostCollideResult)  # 实例化漏洞类，传递参数：存活web的队列，  存储漏洞的列表
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    else:
        print("不碰撞Host")

    return hostCollideResult, censysIPS
