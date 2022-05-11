import requests
import json
import time

def quake_search(all_config,excel,data,xlsx_save_name,domain):
    all_sheet=excel.sheetnames
    if "quake" in all_sheet:         #查看是否存在quake这个sheet
        w_excel=excel["quake"]
    else:
        w_excel=excel.create_sheet("quake",0)            #如果没有则新建
        w_excel.append(data)            #添加title

    quake_api=all_config.get('quake').get('quake_key')
    select=all_config['quake']['quake_select']
    

    quake_search=select.replace('%s',domain)         #将查询语句中的%s替换为用户指定的值domain
    
    headers = {
        "X-QuakeToken": quake_api
    }

    #search_query="domain: {0} || cert: {0} || owner: {0} || hostname: {0}".format(domain)

    data = {
        "query": quake_search,
        "start": 0,
        "size": 500
    }
    print("[-] 正在执行quake模块")
    response = requests.post(url="https://quake.360.cn/api/v3/search/quake_service", headers=headers, json=data)
    datas = json.loads(response.text)
    all_data=datas['data']          #数据格式如此，所有数据都在data下

    if all_data==None:          #因为quake的特殊性，所以经常出现各种报错，如果没数据的话则输出异常，手工排查
        print(response.text)

    for one_data in all_data:
        #print(one_data)
        ip=one_data['ip']
        port=one_data['port']
        hostname=one_data['hostname']
        try:
            cert=one_data.get('service').get('cert')
        except:
            cert="null"
        transport=one_data['transport']
        asn=one_data['asn']
        org=one_data['org']
        country_cn=one_data['location']['country_cn']
        province_cn=one_data['location']['province_cn']
        city_cn=one_data['location']['city_cn']
        try:
            http_host=one_data.get('service').get('http').get('host')
        except:
            http_host="null"
        http_response=one_data['service']['response']
        if one_data['components']:
            try:
                product_catalog=one_data['components'][0]['product_catalog'][0]
            except:
                product_catalog="error"
            try:
                product_type=one_data['components'][0]['product_type'][0]
            except:
                #print(one_data['components'][0]['product_type'])
                product_type="error"
            product_level=one_data['components'][0]['product_level']
            product_vendor=one_data['components'][0]['product_vendor']
        else:
            product_catalog="null"
            product_type="null"
            product_level="null"
            product_vendor="null"
        country_en=one_data['location']['country_en']
        province_en=one_data['location']['province_en']
        city_en=one_data['location']['city_en']
        district_en=one_data['location']['district_en']
        district_cn=one_data['location']['district_cn']
        isp=one_data['location']['isp']
        try:
            body=one_data.get('service').get('http').get('body')
        except:
            body="null"


        # 网站使用的协议
        #name=one_data['service']['name']
        try:
            title=one_data['service']['http']['title']
        except:
            title="null"
        #print("ip: {} port: {} title: {}".format(ip,port,title))
        try:
            w_excel.append([domain,ip,port,title,http_host,http_response,cert,transport,asn,org,country_cn,province_cn,city_cn,district_cn,product_catalog,product_type,product_level,product_vendor,hostname,country_en,province_en,city_en,district_en,isp,body])
        except:
            continue
    #,product_catalog,product_type,product_level,product_vendor
    excel.save(xlsx_save_name)
    print("[+] quake模块已完成")
    time.sleep(4)