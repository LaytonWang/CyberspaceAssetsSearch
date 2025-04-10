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


def create_search_command(key_word, platform):
    b64_search_command = ""
    if URL_PATTERN.fullmatch(key_word):
        url_result = urlparse(key_word)
        if platform == "quake":
            protocol = url_result.scheme if url_result.scheme == "http" else "http/ssl"
            search_command = f'{COMMAND[platform]["protocol="]}"{protocol}"'
        else:
            search_command = f'{COMMAND[platform]["protocol="]}"{url_result.scheme}"'
        if DOMAIN_PATTERN.fullmatch(hostname := url_result.hostname):  # 域名
            search_command += f' {COMMAND[platform]["and"]} {COMMAND[platform]["domain="]}"{hostname}"'
        else:
            search_command += f' {COMMAND[platform]["and"]} {COMMAND[platform]["ip="]}"{hostname}"'
        if port := url_result.port:
            search_command += f' {COMMAND[platform]["and"]} {COMMAND[platform]["port="]}"{port}"'
    elif domain := DOMAIN_PATTERN.search(key_word):  # 域名
        search_command = (f'{COMMAND[platform]["domain="]}"{domain.group(0)}" '
                          f'{COMMAND[platform]["or"]} {COMMAND[platform]["host="]}"{domain.group(0)}"')
    elif ip := IP_PATTERN.search(key_word):  # ip
        search_command = f'{COMMAND[platform]["ip="]}"{ip.group(0)}"'
    elif (path := create_path_pattern().search(key_word)) and platform == "quake":  # url path
        search_command = f'{COMMAND[platform]["url_path="]}"{path.group(0)}"'
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

