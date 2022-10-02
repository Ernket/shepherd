import base64
import requests
import datetime
import json,time

def get_datetime():
    a=datetime.date.today()
    b=str(a).split('-')
    c=int(b[0])-1
    year=str(a)+" 00:00:00"
    last_year="{}-{}-{} 00:00:00".format(c,b[1],b[2])
    return year,last_year

def hunter_search(all_config,excel,data,xlsx_save_name,domain):
    print("[+] 正在执行hunter模块")
    all_sheet=excel.sheetnames
    if "hunter" in all_sheet:         #查看是否存在hunter这个sheet
        w_excel=excel["hunter"]
    else:
        w_excel=excel.create_sheet("hunter",0)            #如果没有则新建
        w_excel.append(data)            #添加title

    select=all_config.get('hunter').get('hunter_select')
    username=all_config.get('hunter').get('hunter_username')
    key=all_config.get('hunter').get('hunter_key')
    year,last_year=get_datetime()

    hunter_select=select.replace('%s',domain)         #将查询语句中的%s替换为用户指定的值domain
    search = base64.urlsafe_b64encode(hunter_select.encode("utf-8"))
    search=search.decode("utf-8")
    #print(search.decode("utf-8"))

    pagenum=1           #页数

    try_num=0
    break_num=1         #尝试多少次后退出的次数

    while True:
        url="https://hunter.qianxin.com/openApi/search?username={}&api-key={}&search={}&page={}&page_size=10&is_web=3&start_time=\"{}\"&end_time=\"{}\"".format(username,key,search,pagenum,last_year,year)
        #print(url)
        req=requests.get(url)
        time.sleep(3)
        json_result=json.loads(req.text)
        try:
            all_data=json_result.get('data').get('arr')
            if all_data=="null":           #如果当前页面返回的数据为0，说明已遍历完成，无需继续
                if try_num<break_num:
                    print("[-] hunter查询页面数据为空，正在尝试下一页")
                    try_num+=1
                    pass
                else:
                    print("[+] hunter模块已完成")
                    break
            for i in all_data:
                is_risk=i.get('is_risk')
                url=i.get('url')
                ip=i.get('ip')
                port=i.get('port')
                web_title=i.get('web_title')
                data_domain=i.get('domain')
                is_risk_protocol=i.get('is_risk_protocol')
                protocol=i.get('protocol')
                base_protocol=i.get('base_protocol')
                status_code=i.get('status_code')
                component=i.get('component')
                os=i.get('os')
                company=i.get('company')
                number=i.get('number')
                country=i.get('country')
                province=i.get('province')
                city=i.get('city')
                updated_at=i.get('updated_at')
                is_web=i.get('is_web')
                as_org=i.get('as_org')
                isp=i.get('isp')
                banner=i.get('banner')
                w_excel.append([domain,url,ip,data_domain,port,web_title,status_code,is_web,is_risk,is_risk_protocol,protocol,base_protocol,str(component),os,company,number,country,province,city,updated_at,as_org,isp,banner])
            excel.save(xlsx_save_name)
            pagenum+=1
        except:
            #print(req.text)
            print("[+] hunter模块已完成")
            break
    excel.save(xlsx_save_name)