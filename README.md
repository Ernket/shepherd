# 前排提醒
项目有段时间没更新了，目前就fofa相关的模块应该是还能用的，其他的更新频率太高，个人开发者（其实就是懒）无暇顾及

# 吐槽
写工具好累，想弄一个真正看起来不错的得花好多时间，懒狗不想写了,欢迎有使用的大哥们提一下建议（例如运行到哪的时候有bug等）


# 介绍
- 工具作用：
- - 将多个空间测绘引擎（目前为zoomeye、hunter、quake、fofa）的接口整合到一起，通过用户给定的domain参数自动化的将各个平台的结果（全字段）保存为xlsx，计划后续整个指纹识别。
- - icp备案和空间测绘聚合，省的你还得专门查备案然后手动添加
- - 获取的子域名会在ip结果中存在内网地址的时候进行host碰撞
- - 利用fofa搜全网无需认证的代理并验证，免费代理池get

# 脚本编写环境：

- - python3.8.3

# 使用方法
```
# 查询域名
python3 Elapse.py -d <domain> | python3 Elape.py -df <domain_file>
# 通过公司名查控股等
python3 Elapse.py -c <company_name> | python3 Elapse.py -cf <company_name_file>
# 或者查完域名跟着一起查公司信息
python3 Elapse.py -d <domain> -c <company_name> | python3 Elapse.py -d <domain> -cf <company_name_file>  等等
# 查代理并验证
python3 Elapse.py -p
```
使用前请先安装所需要的运行库<br>
```
pip install -r requirements.txt
```
# 更新记录
- - 2022/05/11

1.加入了两个新的模块（hunter、zoomeye）<br>
2.加入了-f，读取文件批量获取<br>

- - 2022/07/01

1.部分模块写了异常处理，一个模块报错不影响了（之前发方便排错没写）<br>
2.增加了利用fofa搜索全网无需验证的socks5代理，并输出.ppx文件（Proxifier代理转发工具的配置文件)，为了方便配合[gost](https://github.com/ginuerzh/gost)，result目录下也会输出一份.txt<br>
2.加入了icp备案模块、爱企查、host碰撞模块（censys、fofa）<br>
3.icp备案模块和空间测绘搜索的进行了融合，假设-d参数只给了一个域名，在icp备案后发现存在其他域名时，会进行询问是否将同备案其他域名一起添加搜素<br>
4.修复了我忘了什么的bug<br>

- - 2022/08/02

1.我可真是个大傻呗，proxy.py写的这么垃圾居然都没反应过来，目前已把验证部分的`wirte`改成`write`了，不会一个ip即显示报错又显示成功了<br>
2.同时文件名也改了，之前不知道脑子里装了什么，按时间戳当文件名居然还放到for里面<br>

- - 2022/10/02

1.发现fofa这种如果搜大企业，太多资产，某一个环节出了问题，原先的程序就会报错，因为是所有数据跑完才保存，现在改为跑一页保存一页<br>
2.icp目前有一些小bug，这个bug非程序上的问题，有时候第一次访问提示出错，但是重新访问的时候就显示正常了，目前的做法是加了一个重试一次的操作，不知道有没有用。。。<br>
3.修复了爱企查同时查询多个企业的时候，保存的数据有问题的bug<br>

# 计划写的
- - 将其他平台也添加进来（shodan，搜索引擎，还有什么空间测绘可以用的也可以推荐一下）
  - 指纹识别
  - 没检测到config.yaml时，自动生成
  

# 参考项目：
- - 爱企查、host碰撞模块（https://github.com/0x727/ShuiZe_0x727) 
- - icp域名备案查询（https://github.com/1in9e/icp-domains）
