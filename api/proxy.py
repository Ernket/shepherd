import requests
import threading
import time

def output(ok_list,file_path):
    num=1
    temp_1='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ProxifierProfile version="101" platform="MacOSX" product_id="2" product_minver="200">
<Options>
    <Resolve>
        <AutoModeDetection enabled="false"/>
        <ViaProxy enabled="false">
            <TryLocalDnsFirst enabled="false"/>
        </ViaProxy>
        <ExclusionList ExcludeSimpleHostnames="true" ExcludeLocalhost="true" ExcludeSelfHostname="true" ExcludeLocalDomain="true">localhost;%SimpleHostnames%;%ComputerName%;*.local;
</ExclusionList>
    </Resolve>
    <Encryption mode="basic"/>
    <HttpProxiesSupport enabled="true"/>
    <HandleDirectConnections enabled="false"/>
    <ConnectionLoopDetection enabled="true"/>
    <ProcessServices enabled="true"/>
    <ProcessOtherUsers enabled="true"/>
</Options>
<ProxyList>
    '''
    temp_2=''
    temp_3='''
    </ProxyList>
<ChainList/>
<RuleList>
    <Rule enabled="true">
        <Name>burpsuite</Name>
        <Applications>"Burp Suite Professional.app"; "Burp Suite Professional"; com.install4j.7318-9294-3757-1226.70</Applications>
        <Action type="Direct"/>
    </Rule>
    <Rule enabled="true">
        <Name>Default</Name>
        <Action type="Direct"/>
    </Rule>
</RuleList>
</ProxifierProfile>
    '''
    #for g in range(len(ok_list)):
    for key in ok_list:
        wnum=num+100
        num+=1
        ip=key
        port=ok_list[key]
        temp_2+='''
        <Proxy id="{}" type="SOCKS5">
            <Address>{}</Address>
            <Port>{}</Port>
            <Options>0</Options>
        </Proxy>\n
        '''.format(str(wnum),ip,port)
    with open(file_path+'/result/'+str(time.time_ns())+'.ppx', 'a') as s:
        s.write(temp_1+temp_2+temp_3)
    print('验证完毕，结果位于根目录下的ok.ppx')


def check_proxy(all_proxy,file_path):
    ok_list={}
    socks=['socks5']
    for sock in socks:
        for key in all_proxy:
            ip_port=str(key)+":"+str(all_proxy[key])
            
            web_proxy="{}://{}".format(sock,ip_port)
            proxy = {
                'http': web_proxy,
                'https': web_proxy
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
            }
            try:
                #r = requests.get('http://httpbin.org/ip', headers=headers, proxies=proxy, timeout=5)
                r = requests.get('https://www.baidu.com', headers=headers, proxies=proxy, timeout=5)
                if r.status_code == 200:
                    print('【{}】{}----验证成功'.format(threading.current_thread().name,web_proxy))
                    ok_list[key]=all_proxy[key]
                    proxy_file=open(file_path+"/result/proxy_list.txt",'w',encoding='utf-8')
                    proxy_file.write(str(ip_port))
                    proxy_file.close()
            except Exception as e:
                print('【{}】{}----超时'.format(threading.current_thread().name,web_proxy))
    #return ok_list
    output(ok_list,file_path)
