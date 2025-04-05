#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/25 20:28
# @Author : <Layton>
# @File : hunter_search.py
import json
from datetime import datetime, timedelta

import requests

from common.file_operation import get_config_value
from common.public_method import create_search_command


def send_quake_search(api_key, search_command, args):
    url = "https://quake.360.net/api/v3/search/quake_service"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "X-QuakeToken": api_key,  # api-key，用户登录后在个人中心获取
        "Content-Type": "application/json"
    }
    # needed_fields = eval(get_config_value("needed_fields", "quake_fields"))
    # print(f"needed_fields: {needed_fields}")

    data = {
        "query": f"""{search_command}""",  # 查询语法，即输入的查询内容
        "start": 0,  # 返回结果的下标切片位置, 默认为0
        "size": args.page_size,  # 返回结果的切片长度, 默认为10
        "ignore_cache": False,  # 是否忽略缓存, 默认为False
        "start_time": args.start_time,  # 查询起始时间，接受 2025-3-1 00:00:00 格式的数据，时区为UTC
        "end_time": args.end_time,  # 查询截止时间，接受 2025-3-30 00:00:00 格式的数据，时区为UTC
        "include": [],  # 包含字段, List(str)
        "exclude": [],  # 排除字段, List(str)
        "latest": True,  # 是否使用最新数据, 默认为False
        "shortcuts": []  # 对应web页面里的 过滤无效请求 排除蜜罐 排除CDN（最新值请从WEB的url里获取）, List(str)
    }
    res = requests.post(url, headers=headers, json=data)
    res.encoding = "utf-8"
    return res


def format_quake_data(key_word, search_command, data_arr, needed_fields):
    for data in data_arr:
        protocol = ""
        format_data = [key_word, search_command]
        for field in needed_fields:
            sub_data = data
            sub_fields = field.split('.')
            # print(f"sub_fields: {sub_fields}")
            for sub_field in sub_fields:
                sub_data = sub_data.get(sub_field)
                # print(f"sub_data: {sub_data}")
            format_data.append(str(sub_data))
            if field == "service.name":
                protocol = sub_data
        protocol = "http" if protocol == "http" else "https"
        url = f"{protocol}://{data.get("domain")}:{data.get("port")}"
        format_data[2] = url
        print(f"format_data: {format_data}")
        yield format_data


def search_by_quake(api_key, key_word, needed_fields, args):
    search_command, _ = create_search_command(key_word, args.platform)

    if not args.start_time:
        args.start_time = (datetime.now() - timedelta(days=29)).strftime('%Y-%m-%d')
    if not args.end_time:
        args.end_time = datetime.now().strftime('%Y-%m-%d')

    search_result = send_quake_search(api_key, search_command, args)
    if search_result.status_code != 200:
        print(f"search_result: {search_result}", "请检查api key是否正确")
        return None
    search_result = search_result.json()
    # print(json.dumps(search_result, indent=2, ensure_ascii=False))

    data_arr = search_result.get("data")
    if not data_arr:
        print(f"search_result: {search_result}")
        return None

    format_data = format_quake_data(key_word, search_command, data_arr, needed_fields)
    return format_data


if __name__ == '__main__':
    pass
