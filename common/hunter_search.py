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


def send_hunter_search(api_key, b64_search_command, args):
    url = "https://hunter.qianxin.com/openApi/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0"
    }
    if args.page_size % 10 == 0:
        page_size = args.page_size
    else:
        page_size = (args.page_size // 10 + 1) * 10
        print(f"hunter的page_size必须是10的倍数，已将page_size设置为{page_size}。")

    params = {
        "api-key": api_key,  # api-key，用户登录后在个人中心获取
        "search": b64_search_command,  # 经过符合RFC 4648标准的base64url编码编码后的搜索语法，语法规则见首页-查询语法
        "page": 1,  # 页码
        "page_size": page_size,  # 每页资产条数
        "is_web": 3,  # 资产类型，1代表”web资产“，2代表”非web资产“，3代表”全部“
        "status_code": args.status_code,  # 状态码列表，以逗号分隔，如”200,401“
        # "status_code": "",  # 状态码列表，以逗号分隔，如”200,401“
        "start_time": args.start_time,  # 开始时间，格式为2025-03-01(时间范围超出近30天，将扣除权益积分)
        "end_time": args.end_time,  # 结束时间，格式为2025-03-30(时间范围超出近30天，将扣除权益积分)
    }
    res = requests.get(url, params=params, headers=headers)
    res.encoding = "utf-8"
    return res


def format_hunter_data(key_word, search_command, data_arr, needed_fields, args):
    for data in data_arr:
        format_data = [key_word, search_command]
        for field in needed_fields:
            value = data.get(field)
            format_data.append(str(value))

        status_code = data.get("status_code", data)
        if str(status_code) not in args.status_code:
            print(f"format_data: {format_data}")
            continue
        # print(f"format_data: {format_data}")
        yield format_data


def search_by_hunter(api_key, key_word, needed_fields, args):
    search_command, b64_search_command = create_search_command(key_word, args.platform)

    if not args.start_time:
        args.start_time = (datetime.now() - timedelta(days=29)).strftime('%Y-%m-%d')
    if not args.end_time:
        args.end_time = datetime.now().strftime('%Y-%m-%d')

    search_result = send_hunter_search(api_key, b64_search_command, args)
    search_result = search_result.json()
    # print(json.dumps(search_result, indent=2, ensure_ascii=False))

    data = search_result.get("data")
    if not data:
        print(f"search_result: {search_result}")
        return None
    data_arr = data.get("arr")
    if not data_arr:
        print(f"search_result: {search_result}")
        return None

    format_data = format_hunter_data(key_word, search_command, data_arr, needed_fields, args)
    return format_data


if __name__ == '__main__':
    pass
