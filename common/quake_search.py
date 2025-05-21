#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/25 20:28
# @Author : <Layton>
# @File : quake_search.py
import re
from urllib.parse import urlparse

import requests

from common.public_method import get_field_value


def send_quake_search(search_command, args):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "X-QuakeToken": args.api_key,  # api-key，用户登录后在个人中心获取
        "Content-Type": "application/json"
    }

    data = {
        "query": f"""{search_command}""",  # 查询语法，即输入的查询内容
        "start": (args.page - 1) * args.page_size,  # 返回结果的下标切片位置, 默认为0
        "size": args.page_size,  # 返回结果的切片长度, 默认为10
        "ignore_cache": False,  # 是否忽略缓存, 默认为False
        "start_time": args.start_time,  # 查询起始时间，接受 2025-3-1 00:00:00 格式的数据，时区为UTC
        "end_time": args.end_time,  # 查询截止时间，接受 2025-3-30 00:00:00 格式的数据，时区为UTC
        "include": [],  # 包含字段, List(str)
        "exclude": [],  # 排除字段, List(str)
        "latest": True,  # 是否使用最新数据, 默认为False
        "shortcuts": []  # 对应web页面里的 过滤无效请求 排除蜜罐 排除CDN（最新值请从WEB的url里获取）, List(str)
    }
    res = requests.post(args.platform_url, headers=headers, json=data)
    res.encoding = "utf-8"
    return res


def generate_quake_url(data):
    ipv6_pattern = re.compile(r'^([0-9a-fA-F]{0,4}:)+([0-9a-fA-F]{0,4})$')
    protocol = get_field_value("service.name", data)
    url = f"{protocol if protocol == "http" else "https"}://"

    if domain := get_field_value("domain", data):
        url += domain
    elif host := get_field_value("service.http.host", data):
        if ipv6_match := ipv6_pattern.fullmatch(host):
            host = f"[{ipv6_match.group(0)}]"
        url += host
    elif ip := get_field_value("ip", data):
        if ipv6_match := ipv6_pattern.fullmatch(ip):
            ip = f"[{ipv6_match.group(0)}]"
        url += ip

    url_result = urlparse(url)
    if not url_result.port:
        port = get_field_value("port", data)
        url = f"{url}:{port}"

    path = get_field_value("service.http.path", data)
    url = url + path if path else url
    data.update({"url": url})
    return data


def format_quake_data(needed_fields, data_arr):
    for data in data_arr:
        if not data.get("url"):
            data = generate_quake_url(data)

        format_data = []
        for field in needed_fields:
            field_value = get_field_value(field, data)
            format_data.append(str(field_value))
        # print(f"format_data: {format_data}")
        yield format_data


if __name__ == '__main__':
    pass
