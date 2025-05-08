#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/4/2 17:43
# @Author : <Layton>
# @File : public_method.py
import re
from urllib.parse import urlparse

from config import URL_PATTERN, DOMAIN_PATTERN, IP_PATTERN, COMMANDS

__all__ = ['create_search_command', 'get_field_value', 'has_search_finished', ]


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
    search_command = f'{COMMANDS[platform]["protocol="]}"{protocol}"'

    if DOMAIN_PATTERN.fullmatch(hostname := url_result.hostname):  # 域名 或 ip
        search_command += f' && {COMMANDS[platform]["domain="]}"{hostname}"'
    else:
        search_command += f' && {COMMANDS[platform]["ip="]}"{hostname}"'

    if port := url_result.port:  # 端口
        search_command += f' && {COMMANDS[platform]["port="]}"{port}"'

    if path := url_result.path:  # 路径
        if platform == "quake":
            search_command += f' && {COMMANDS[platform]["url_path="]}"{path}"'
    return search_command


def create_search_command(keyword, status_code, platform):
    if url_match := URL_PATTERN.fullmatch(keyword):  # 完整的URL
        url = url_match.group(0)
        search_command = create_command_from_url(url, platform)
    elif domain_match := DOMAIN_PATTERN.search(keyword):  # 含有域名
        domain = domain_match.group(0)
        search_command = f'{COMMANDS[platform]["domain="]}"{domain}"'
        search_command += f' || {COMMANDS[platform]["host="]}"{domain}"'
    elif ip_match := IP_PATTERN.search(keyword):  # 含有ip
        ip = ip_match.group(0)
        search_command = f'{COMMANDS[platform]["ip="]}"{ip}"'
    elif (path_match := create_path_pattern().search(keyword)) and platform == "quake":  # url路径
        path = path_match.group(0)
        search_command = f'{COMMANDS[platform]["url_path="]}"{path}"'
    else:
        search_command = f'{COMMANDS[platform]["title="]}"{keyword}"'
        # search_command = f'{COMMANDS[platform]["title="]}"{key_word}" || {COMMANDS[platform]["body="]}"{key_word}"'

    if status_code:
        if "||" in search_command:
            search_command = f'({search_command})'
        search_command = f'{search_command} && {COMMANDS[platform]["status_code="]}"{status_code}"'
    print(f"search_command: {search_command}")
    return search_command


def get_field_value(field, data):
    sub_data = data
    sub_fields = field.split('.')
    for sub_field in sub_fields:
        sub_data = sub_data.get(sub_field)
        if not sub_data:
            return None
    field_value = sub_data
    return field_value


def has_search_finished(total_size, args):
    if total_size not in ["", "None", None]:
        if total_size <= args.page_size:
            return True
        else:
            args.sum_page_size += args.page_size
            if total_size <= args.sum_page_size:
                return True
            elif args.sum_page_size == (args.total_pages * args.page_size):
                return True


if __name__ == '__main__':
    pass
