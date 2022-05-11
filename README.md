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

1.加入了两个新的模块（hunter、zoomeye）
2.加入了-f，读取文件批量访问

- 计划写的

- - 加入-f参数，读取文件批量去查询
  - 将其他平台也添加进来
  - 指纹识别
  - 没检测到config.yaml时，自动生成
