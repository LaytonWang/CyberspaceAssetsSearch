# 简介

调用“网络空间搜索引擎”的api接口，搜索出相应的资产信息，进而进行信息的获取筛选，或敏感信息泄露的排查。



# 运行环境

- 使用Python 3.12开发。
- 代码中使用了海象符（:=），运行环境必须是Python 3.8以上。

- 运行建议：

```bash
# 创建虚拟环境
py -3.12 -m venv venv
# 激活虚拟环境
.\venv\Scripts\activate
# 安装依赖包（使用清华源）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```



# 使用说明

## 配置说明

- config/config.ini文件

![image-20250403103304290](./assets/image-20250403103304290.png)

- [api_key]：配置“空间测绘平台”的api key（如：hunter（鹰图）、fofa、quake）
- [needed_fields]：配置需要从搜索结果中获取的字段。



## 简单使用

- 指定"单个平台"、“单个关键字”查询

```bash
python assets_search.py hunter -k keyword
```

- 指定"单个平台"、“含有多个关键字的文件”查询（一行含有多个关键字，用逗号、空格、顿号隔开）

```bash
python assets_search.py fofa -kf keywords.txt
```

- 指定“所有平台”查询

```bash
python assets_search.py all -k keyword
python assets_search.py all -kf keywords.txt
```

- 指定“结果存放的文件”（支持：.txt .csv）

```bash
python assets_search.py quake -k keyword -rf result.csv
```



# 参数说明

- 查看帮助

```bash
python assets_search.py -h
```

```bash
usage: assets_search.py [-h] [-k KEYWORD | -kf KEYWORDS_FILE] [-rf RESULT_FILE] [-p PAGE] [-pz PAGE_SIZE] [-sc STATUS_CODE] [-st START_TIME] [-et END_TIME] [-d DELAY]
                           platform

positional arguments:
  platform              support: hunter、fofa、quake、all

options:
  -h, --help            show this help message and exit
  -k KEYWORD, --keyword KEYWORD
                        one keyword
  -kf KEYWORDS_FILE, --keywords_file KEYWORDS_FILE
  -kf KEYWORDS_FILE, --keywords_file KEYWORDS_FILE
                        like: keywords.csv
  -rf RESULT_FILE, --result_file RESULT_FILE
                        support: .txt .csv
  -p PAGE, --page PAGE  default: 1
  -pz PAGE_SIZE, --page_size PAGE_SIZE
                        default: 10
  -sc STATUS_CODE, --status_code STATUS_CODE
                        format: "200,302" only for hunter
  -st START_TIME, --start_time START_TIME
                        format: 2025-03-01
  -et END_TIME, --end_time END_TIME
                        format: 2025-03-30
  -d DELAY, --delay DELAY
                        default: 2.5
```



# 更新日志



##  v1.0.0  2025.04.05

- 给定“关键字”，调用“hunter(鹰图)、fofa、quake”的api接口，查询网络空间资产
- 支持“all”参数，所有平台依次查询



