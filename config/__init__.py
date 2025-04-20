#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/25 22:50
# @Author : <Layton>
# @File : __init__.py
import os
import re

# 目录配置
PROJECT_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_DIR = os.path.join(PROJECT_BASE_DIR, 'config')
RESULTS_DIR = os.path.join(PROJECT_BASE_DIR, 'results')

# 正则匹配配置
URL_PATTERN = re.compile(
    r'^(https?|ftp)://'  # 协议（http, https, ftp）
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # 域名
    r'localhost|'  # localhost
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IPv4地址
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IPv6地址
    r'(?::\d+)?'  # 端口号
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
DOMAIN_PATTERN = re.compile(r'(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63}(?<!-))*\.[A-Za-z]{2,}')
IP_PATTERN = re.compile(r'(\d{1,3}\.){3}\d{1,3}')

# 查询命令配置
COMMANDS = {
    "hunter": {
        "and": "&&",
        "or": "||",
        "protocol=": "protocol=",
        "domain=": "domain=",
        "host=": "domain.suffix=",
        "ip=": "ip=",
        "port=": "ip.port=",
        "title=": "web.title=",
        "body=": "web.body=",
    },
    "fofa": {
        "and": "&&",
        "or": "||",
        "protocol=": "protocol=",
        "domain=": "domain=",
        "host=": "host=",
        "ip=": "ip=",
        "port=": "port=",
        "title=": "title=",
        "body=": "body=",
    },
    "quake": {
        "and": "AND",
        "or": "OR",
        "protocol=": "service:",
        "domain=": "domain:",
        "host=": "hostname:",
        "ip=": "ip:",
        "port=": "port:",
        "title=": "title:",
        "body=": "body:",
        "url_path=": "http_path:",
    }
}

# 数据总数字段
TOTAL_SIZE_FIELDS = {
    "hunter": "data.total",
    "fofa": "size",
    "quake": "meta.pagination.total",
}

# 数据列表字段
DATA_ARR_FIELDS = {
    "hunter": "data.arr",
    "fofa": "results",
    "quake": "data",
}

if __name__ == '__main__':
    # print(PROJECT_BASE_DIR)
    # print(CONFIG_DIR)
    # print(RESULTS_DIR)
    print(COMMANDS["hunter"])
    print(COMMANDS["hunter"]["and"])
