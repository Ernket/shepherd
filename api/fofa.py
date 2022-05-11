import requests
import json
import base64

def fofa_search(all_config,excel,data,xlsx_save_name,domain):
    all_sheet=excel.sheetnames
    if "fofa" in all_sheet:         #查看是否存在fofa这个sheet
        w_excel=excel["fofa"]
    else:
        w_excel=excel.create_sheet("fofa",0)            #如果没有则新建
        w_excel.append(data)            #添加title
    email=all_config["fofa"]["fofa_email"]
    key=all_config["fofa"]["fofa_key"]
    select=all_config["fofa"]["fofa_select"]

    fofa_search=select.replace('%s',domain)         #将查询语句中的%s替换为用户指定的值domain

    header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded"
    }


    #fofa_search='domain="{0}" || cert="{0}" || host="{0}" || cname="{0}"'.format(domain)            #定义fofa查询语句
    str_base64=base64.b64encode(fofa_search.encode('utf-8')).decode("utf-8")            #base64编码查询语句
    page_num=1
    print("[-] 正在执行fofa模块")
    try_num=0
    break_num=3         #失败后尝试的次数，如 =1，则表示只尝试一页
    while True:
        fofa_search_url = "https://fofa.info/api/v1/search/all?fields=ip,port,title,host,domain,country,province,city,country_name,header,server,protocol,banner,cert,isp,as_number,as_organization,latitude,longitude,icp,fid,cname,type,jarm&page={}&email={}&key={}&qbase64={}&size=10".format(page_num,email,key,str_base64)
        #print(fofa_search_url)
        res = requests.get(fofa_search_url, headers=header)
        if 'errmsg' not in res.text:
            result = json.loads(res.text)
        
        if len(result['results'])==0:           #如果当前页面返回的数据为0，说明已遍历完成，无需继续
            if try_num<break_num:
                print("[-] fofa查询页面数据为空，正在尝试下一页")
                try_num+=1
                pass
            elif try_num==break_num:          
                print("[+] fofa模块已完成")
                break
        
        #print("当前第"+str(page_num)+"页 "+"条目："+str(len(result['results'])))         #显示当前页数有多少条数据
        
        for link in result['results']:
            link.insert(0,domain)
            try:
                w_excel.append(link)
            except:
                link[13]="error"
                w_excel.append(link)
        #for link in result['results']:
            #print(link)
            #break
        page_num+=1
        #time.sleep(1)
    excel.save(xlsx_save_name)