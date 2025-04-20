#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2025/4/20 09:58
# @Author: <Layton>
# @File: __init__.py

from common.hunter_search import send_hunter_search, format_hunter_data
from common.fofa_search import send_fofa_search, format_fofa_data
from common.quake_search import send_quake_search, format_quake_data

# 发送请求的函数
SEND_SEARCH_FUNCS = {
    "hunter": send_hunter_search,
    "fofa": send_fofa_search,
    "quake": send_quake_search,
}

# 格式化数据的函数
FORMAT_DATA_FUNCS = {
    "hunter": format_hunter_data,
    "fofa": format_fofa_data,
    "quake": format_quake_data,
}


if __name__ == '__main__':
    print(SEND_SEARCH_FUNCS["hunter"])
    print(FORMAT_DATA_FUNCS["fofa"])
