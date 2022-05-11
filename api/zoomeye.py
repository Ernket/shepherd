import requests
import json

def zoomeye_search(all_config,excel,data,xlsx_save_name,domain):
    print("[+] 正在执行zoomeye模块")
    all_sheet=excel.sheetnames
    if "zoomeye" in all_sheet:         #查看是否存在fofa这个sheet
        w_excel=excel["zoomeye"]
    else:
        w_excel=excel.create_sheet("zoomeye",0)            #如果没有则新建
        w_excel.append(data)            #添加title

    key=all_config.get('zoomeye').get('zoomeye_key')
    header={"API-KEY":str(key)}

    pagenum=1           #页数

    try_num=0
    break_num=3         #尝试多少次后退出的次数

    search_type=0
    while True:
        url1="https://api.zoomeye.org/domain/search?q={}&type={}&page={}".format(domain,search_type,pagenum)
        req=requests.get(url1,headers=header)
        #print(req.text)
        json_result=json.loads(req.text)
        all_list=json_result.get('list')
        if len(all_list)==0:           #如果当前页面返回的数据为0，说明已遍历完成，无需继续
            if try_num<break_num:
                print("[-] zoomeye查询页面数据为空，正在尝试下一页")
                try_num+=1
                pass
            elif try_num==break_num:
                if search_type==0:
                    search_type+=1
                else:          
                    print("[+] zoomeye模块已完成")
                    break
        for i in all_list:
            name=i.get('name')
            timestamp=i.get('timestamp')
            ip=i.get('ip')
            w_excel.append([domain,name,timestamp,str(ip)])
            #print(name,timestamp,ip)
        pagenum+=1
    excel.save(xlsx_save_name)