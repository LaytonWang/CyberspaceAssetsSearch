#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/4/2 17:43
# @Author : <Layton>
# @File : public_method.py
import re
import base64
from urllib.parse import urlparse

from config import URL_PATTERN, DOMAIN_PATTERN, IP_PATTERN, COMMAND


def create_path_pattern():
    # 定义路径各部分的正则组件
    path_segment = r"[a-zA-Z0-9\-._~%!$&'()*+,;=:@]+"  # 路径段
    segments = rf"(?:/{path_segment})*"  # 多个路径段
    query = r"(?:\?[a-zA-Z0-9\-._~%!$&'()*+,;=:@/?]*)?"  # 查询参数(可选)
    fragment = r"(?:#[a-zA-Z0-9\-._~%!$&'()*+,;=:@/?]*)?"  # 哈希片段(可选)
    # 组合完整的正则表达式
    pattern = rf"^{segments}{query}{fragment}$"
    return re.compile(pattern)


def create_command_from_url(url, platform):
    url_result = urlparse(url)

    protocol = url_result.scheme  # 协议
    if platform == "quake":
        protocol = "http" if protocol == "http" else "http/ssl"
    search_command = f'{COMMAND[platform]["protocol="]}"{protocol}"'

    if DOMAIN_PATTERN.fullmatch(hostname := url_result.hostname):  # 域名 或 ip
        search_command += f' {COMMAND[platform]["and"]} {COMMAND[platform]["domain="]}"{hostname}"'
    else:
        search_command += f' {COMMAND[platform]["and"]} {COMMAND[platform]["ip="]}"{hostname}"'

    if port := url_result.port:  # 端口
        search_command += f' {COMMAND[platform]["and"]} {COMMAND[platform]["port="]}"{port}"'

    if path := url_result.path:  # 路径
        if platform == "quake":
            search_command += f' {COMMAND[platform]["and"]} {COMMAND[platform]["url_path="]}"{path}"'
    return search_command


def create_search_command(key_word, platform):
    search_command, b64_search_command = "", ""

    if url_match := URL_PATTERN.fullmatch(key_word):  # 完整的URL
        url = url_match.group(0)
        search_command = create_command_from_url(url, platform)
    elif domain_match := DOMAIN_PATTERN.search(key_word):  # 含有域名
        domain = domain_match.group(0)
        search_command = f'{COMMAND[platform]["domain="]}"{domain}"'
        search_command += f' {COMMAND[platform]["or"]} {COMMAND[platform]["host="]}"{domain}"'
    elif ip_match := IP_PATTERN.search(key_word):  # 含有ip
        ip = ip_match.group(0)
        search_command = f'{COMMAND[platform]["ip="]}"{ip}"'
    elif (path_match := create_path_pattern().search(key_word)) and platform == "quake":  # url路径
        path = path_match.group(0)
        search_command = f'{COMMAND[platform]["url_path="]}"{path}"'
    else:
        search_command = f'{COMMAND[platform]["title="]}"{key_word}"'
        # search_command = (f'{COMMAND[platform]["title="]}"{key_word}" '
        #                   f'{COMMAND[platform]["or"]} {COMMAND[platform]["body="]}"{key_word}"')
    print(f"search_command: {search_command}")

    if platform == "hunter":
        b64_search_command = base64.urlsafe_b64encode(search_command.encode("utf-8"))
    elif platform == "fofa":
        b64_search_command = base64.b64encode(search_command.encode("utf-8"))
    return search_command, b64_search_command


if __name__ == '__main__':
    pass

