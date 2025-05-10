#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/25 20:28
# @Author : <Layton>
# @File : hunter_search.py
import re
import base64

import requests


def send_hunter_search(search_command, args):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0"
    }
    b64_search_command = base64.urlsafe_b64encode(search_command.encode("utf-8"))

    if args.page_size % 10 == 0:
        page_size = args.page_size
    else:
        page_size = (args.page_size // 10 + 1) * 10
        print(f"hunter的page_size必须是10的倍数，已将page_size设置为{page_size}。")

    params = {
        "api-key": args.api_key,  # api-key，用户登录后在个人中心获取
        "search": b64_search_command,  # 经过符合RFC 4648标准的base64url编码编码后的搜索语法，语法规则见首页-查询语法
        "page": args.page,  # 页码
        "page_size": page_size,  # 每页资产条数
        "is_web": 3,  # 资产类型，1代表”web资产“，2代表”非web资产“，3代表”全部“
        "status_code": "",  # 状态码列表，以逗号分隔，如”200,401“
        "start_time": args.start_time,  # 开始时间，格式为2025-03-01(时间范围超出近30天，将扣除权益积分)
        "end_time": args.end_time,  # 结束时间，格式为2025-03-30(时间范围超出近30天，将扣除权益积分)
    }
    res = requests.get(args.platform_url, params=params, headers=headers)
    res.encoding = "utf-8"
    return res


def find_hunter_icon(data):
    url, icon_url =  data.get("url"), ""
    banner =  data.get("banner")

    icon_pattern = re.compile(r'<link rel=\\+"icon\\+".*?href=\\+"\.?(.*?)\\+".*?>')
    icon_match = icon_pattern.search(banner)
    if icon_match:
        icon_url = url + icon_match.group(1)

    data.update({"icon": icon_url})
    return data


def format_hunter_data(needed_fields, data_arr):
    for data in data_arr:
        if not data.get("icon"):
            data = find_hunter_icon(data)

        format_data = []
        for field in needed_fields:
            field_value = data.get(field)
            format_data.append(str(field_value))
        # print(f"format_data: {format_data}")
        yield format_data


if __name__ == '__main__':
    pass
