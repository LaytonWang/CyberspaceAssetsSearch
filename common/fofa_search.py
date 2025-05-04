#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/25 20:28
# @Author : <Layton>
# @File : fofa_search.py
import re
import base64

import requests


def send_fofa_search(args, search_command):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0"
    }
    b64_search_command = base64.b64encode(search_command.encode("utf-8"))

    public_fields = {"ip", "port", "protocol", "org", "host", "domain", "os", "server", "icp", "title", "jarm",
                     "header", "banner", "base_protocol", "link", "tls.version", }  # 无需权限的字段
    personal_fields = {"header_hash", "banner_hash", "banner_fid", }  # 个人版的字段
    professional_fields = {"product", "product_category", "version", "lastupdatetime", "cname", }  # 专业版的字段
    business_fields = {"icon_hash", "cert.is_valid", "cname_domain", "body", "cert.is_match",
                       "cert.is_equal", }  # 商业版的字段
    business_fields = {"icon", "fid", "cname_domain", "structinfo", }  # 企业会员的字段

    supported_fields = public_fields | personal_fields | professional_fields
    fields = supported_fields | set(args.needed_fields)

    params = {
        "key": args.api_key,  # api-key，用户登录后在个人中心获取
        "qbase64": b64_search_command,  # 经过base64编码后的查询语法，即输入的查询内容
        "fields": ",".join(fields),  # 可选字段，默认host,ip,port
        "page": args.page,  # 是否翻页，默认为第一页，按照更新时间排序
        "size": args.page_size,  # 每页查询数量，默认为100条，最大支持10,000条/页
        "full": False,  # 默认搜索一年内的数据，指定为true即可搜索全部数据
        "r_type": "json",  # 可以指定返回json格式的数据
    }
    res = requests.get(args.platform_url, params=params, headers=headers)
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


def format_fofa_data(args, search_command, data_arr):
    for data in data_arr:
        if not data.get("link"):
            data = generate_fofa_link(data)

        format_data = [args.keyword, search_command]
        for field in args.needed_fields:
            value = data.get(field)
            format_data.append(str(value))
        # print(f"format_data: {format_data}")
        yield format_data


if __name__ == '__main__':
    pass
