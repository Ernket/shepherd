# 吐槽
写工具好累，想弄一个真正看起来不错的得花好多时间，懒狗不想写了

# 介绍
- 工具作用：
- - 将多个空间测绘引擎（目前为zoomeye、hunter、quake、fofa）的接口整合到一起，通过用户给定的domain参数自动化的将各个平台的结果（全字段）保存为xlsx，计划后续整个指纹识别。

- 脚本编写环境：

- - python3.8.3

- 使用方法
```
python3 Elapse.py -d <domain>
python3 Elapse.py -f <filename>
```
- 更新
- - 2022/05/11

1.加入了两个新的模块（hunter、zoomeye）<br>
2.加入了-f，读取文件批量获取<br>

- - 2022/07/01

1.部分模块写了异常处理，一个模块报错不影响了（之前发方便排错没写）<br>
2.增加了利用fofa搜索全网无需验证的socks5代理，并输出.ppx文件（Proxifier代理转发工具的配置文件)，为了方便配合[gost](https://github.com/ginuerzh/gost)，result目录下也会输出一份.txt<br>
2.加入了icp备案模块、爱企查、host碰撞模块（censys、fofa）<br>
3.icp备案模块和空间测绘搜索的进行了融合，假设-d参数只给了一个域名，在icp备案后发现存在其他域名时，会进行询问是否将同备案其他域名一起添加搜素<br>
3.修复了我忘了什么的bug<br>

- 计划写的
- - 将其他平台也添加进来（shodan，搜索引擎，还有什么空间测绘可以用的也可以推荐一下）
  - 指纹识别
  - 没检测到config.yaml时，自动生成

- 参考项目：
- - 爱企查、host碰撞模块（https://github.com/0x727/ShuiZe_0x727) 
- - icp域名备案查询（https://github.com/1in9e/icp-domains）
