#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/25 20:28
# @Author : <Layton>
# @File : hunter_search.py
import re
import json

import requests

from common.file_operation import get_config_value
from common.public_method import create_search_command


def send_fofa_search(api_key, b64_search_command, needed_fields, args):
    url = "https://fofa.info/api/v1/search/all"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0"
    }

    public_fields = {"ip", "port", "protocol", "org", "host", "domain", "os", "server", "icp", "title", "jarm",
                     "header", "banner", "base_protocol", "link", "tls.version", }  # 无需权限的字段
    personal_fields = {"header_hash", "banner_hash", "banner_fid", }  # 个人版的字段
    professional_fields = {"product", "product_category", "version", "lastupdatetime", "cname", }  # 专业版的字段
    business_fields = {"icon_hash", "cert.is_valid", "cname_domain", "body", "cert.is_match",
                       "cert.is_equal", }  # 商业版的字段
    business_fields = {"icon", "fid", "cname_domain", "structinfo", }  # 企业会员的字段

    supported_fields = public_fields | personal_fields | professional_fields
    fields = supported_fields | set(needed_fields)

    params = {
        "key": api_key,  # api-key，用户登录后在个人中心获取
        "qbase64": b64_search_command,  # 经过base64编码后的查询语法，即输入的查询内容
        "fields": ",".join(fields),  # 可选字段，默认host,ip,port
        "page": 1,  # 是否翻页，默认为第一页，按照更新时间排序
        "size": args.page_size,  # 每页查询数量，默认为100条，最大支持10,000条/页
        "full": False,  # 默认搜索一年内的数据，指定为true即可搜索全部数据
        "r_type": "json",  # 可以指定返回json格式的数据
    }
    res = requests.get(url, params=params, headers=headers)
    res.encoding = "utf-8"
    return res


def generate_fofa_link(data):
    host = data.get("host")
    if host and host.startswith("http"):
        link = host
    else:
        link = f"{data.get("protocol")}://"
        if host:
            link += host
        elif domain := data.get("domain"):
            link += domain
        elif ip := data.get("ip"):
            link += ip
        link = f"{link}:{data.get("port")}"

    data.update({"link": link})
    return data


def find_fofa_status_code(data, status_code):
    code_pattern = re.compile(r'HTTP.*? (\d{3}) ')
    if header := data.get("header", ""):
        status_code = code_pattern.search(header).group(1)
    elif banner := data.get("banner", ""):
        status_code = code_pattern.search(banner).group(1)

    data.update({"status_code": status_code})
    return data, status_code


def format_fofa_data(key_word, search_command, data_arr, needed_fields, args):
    for data in data_arr:
        if not data.get("link"):
            data = generate_fofa_link(data)
        status_code = str(data.get("status_code"))
        if len(status_code) != 3:
            data, status_code = find_fofa_status_code(data, status_code)

        format_data = [key_word, search_command]
        for field in needed_fields:
            value = data.get(field)
            format_data.append(str(value))

        if status_code not in args.status_code:
            print(f"format_data: {format_data}")
            continue
        # print(f"format_data: {format_data}")
        yield format_data


def search_by_fofa(api_key, key_word, needed_fields, args):
    search_command, b64_search_command = create_search_command(key_word, args.platform)

    search_result = send_fofa_search(api_key, b64_search_command, needed_fields, args)
    search_result = search_result.json()
    # print(json.dumps(search_result, indent=2, ensure_ascii=False))

    data_arr = search_result.get("results")
    if not data_arr:
        print(f"search_result: {search_result}")
        return None

    format_data = format_fofa_data(key_word, search_command, data_arr, needed_fields, args)
    return format_data


if __name__ == '__main__':
    pass
