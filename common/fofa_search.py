#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/25 20:28
# @Author : <Layton>
# @File : hunter_search.py
import json
import base64

import requests

from common.file_operation import get_config_value
from common.public_method import create_search_command


def send_fofa_search(api_key, b64_search_command, args):
    url = "https://fofa.info/api/v1/search/all"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0"
    }
    needed_fields = eval(get_config_value("needed_fields", "fofa_fields"))
    # print(f"needed_fields: {needed_fields}")

    params = {
        "key": api_key,  # api-key，用户登录后在个人中心获取
        "qbase64": b64_search_command,  # 经过base64编码后的查询语法，即输入的查询内容
        "fields": ",".join(needed_fields),  # 可选字段，默认host,ip,port
        "page": args.page,  # 是否翻页，默认为第一页，按照更新时间排序
        "size": args.page_size,  # 每页查询数量，默认为100条，最大支持10,000条/页
        "full": False,  # 默认搜索一年内的数据，指定为true即可搜索全部数据
        "r_type": "json",  # 可以指定返回json格式的数据
    }
    res = requests.get(url, params=params, headers=headers)
    res.encoding = "utf-8"
    return res


def format_fofa_data(key_word, search_command, data_arr, needed_fields):
    for data in data_arr:
        format_data = [key_word, search_command]
        for field in needed_fields:
            value = data.get(field)
            format_data.append(str(value))
        if not data.get("link"):
            if (host := data.get("host", "")).startswith("http"):
                link = host
            else:
                link = f"{data.get("protocol")}://{host}:{data.get("port")}"
            format_data[2] = link
        print(f"format_data: {format_data}")
        yield format_data


def search_by_fofa(api_key, key_word, needed_fields, args):
    search_command, b64_search_command = create_search_command(key_word, args.platform)

    search_result = send_fofa_search(api_key, b64_search_command, args)
    search_result = search_result.json()
    # print(json.dumps(search_result, indent=2, ensure_ascii=False))

    data_arr = search_result.get("results")
    if not data_arr:
        print(f"search_result: {search_result}")
        return None

    format_data = format_fofa_data(key_word, search_command, data_arr, needed_fields)
    return format_data


if __name__ == '__main__':
    pass
