import os,yaml,time
import openpyxl
import argparse
from api.fofa import fofa_search
from api.quake import quake_search

parser = argparse.ArgumentParser(description="ElapseScan.")
parser.add_argument('-d', '--domain', type=str, dest='domain', help='Input your domain.')
args = parser.parse_args()

py_path=os.path.dirname(os.path.realpath(__file__))         #获取py文件的当前路径
xlsx_save_name=str(py_path)+'/result/result-'+str(time.time_ns())+".xlsx"           #路径拼接、保存至result目录下

domain=args.domain
if domain==None:
    print("[-] 未指定域名")
    exit()

def get_config():           #读取配置文件
    global py_path
    config_path=os.path.join(py_path,"config.yaml")         #路径拼接，获取py文件同目录下的config.yaml
    file = open(config_path,"r",encoding="utf-8")
    data = yaml.full_load(file)
    file.close()
    return data

all_config=get_config()         #获取所有密钥

excel=openpyxl.Workbook()           #每次运行都创建一个新的xlsx文件，而非覆盖｜追加
excel.remove(excel[excel.sheetnames[0]])
fofa_data=["api","ip","端口","title","host","域名","国家","省份","城市","国家全名","header","server","协议","banner","cert","运营商","as_number","as_organization","latitude","longitude","icp","fid","cname","type","jarm"]
quake_data=["api","ip","端口","title","域名","网页状态码","cert","传输协议类型","asn","org","国家","省份","城市","区域","框架详情","框架类型","框架等级","供应商","hostname","国家","省份","城市","区域","运营商","Body"]
# data=[]
# for i in range(23):
#     data.append(str(i))
# w_excel=excel.create_sheet("api原始数据",0)
# w_excel.append(data)            #添加title

fofa_enable=all_config.get('fofa').get('enable')
if fofa_enable:
    fofa_search(all_config,excel,fofa_data,xlsx_save_name,domain)

quake_enable=all_config.get('quake').get('enable')
if quake_enable:
    quake_search(all_config,excel,quake_data,xlsx_save_name,domain)