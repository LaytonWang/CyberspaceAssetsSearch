#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/25 9:27
# @Author : <Layton>
# @File : sens_info_search.py
import os
import re
import time
import json
import argparse
from datetime import datetime, timedelta

from config import TOTAL_SIZE_FIELDS, DATA_ARR_FIELDS
from common import SEND_SEARCH_FUNCS, FORMAT_DATA_FUNCS
from common.public_method import *
from common.file_operation import *


def arguments_parse():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('platform', type=str, help='support: hunter、fofa、quake、all')

    keyword_group = arg_parser.add_mutually_exclusive_group()
    keyword_group.add_argument('-k', '--keywords', type=str, help='keywords for search', default="")
    keyword_group.add_argument('-kf', '--keywords_file', type=str, help='like: keywords.csv', default="")

    arg_parser.add_argument('-rf', '--result_file', type=str, help='support: .csv .html', default="")
    arg_parser.add_argument('-tp', '--total_pages', type=int, help='default: 1', default=1)
    arg_parser.add_argument('-pz', '--page_size', type=int, help='default: 10', default=10)
    arg_parser.add_argument('-sc', '--status_code', type=str, help='format: "200"', default="")
    arg_parser.add_argument('-st', '--start_time', type=str, help='format: 2025-03-01', default="")
    arg_parser.add_argument('-et', '--end_time', type=str, help='format: 2025-03-30', default="")
    arg_parser.add_argument('-d', '--delay', type=float, help='default: 2.5', default=2.5)

    args = arg_parser.parse_args()
    return args


def send_platform_search(search_command, args):
    if not args.start_time:
        args.start_time = (datetime.now() - timedelta(days=29)).strftime('%Y-%m-%d')
    if not args.end_time:
        args.end_time = datetime.now().strftime('%Y-%m-%d')

    search_result = SEND_SEARCH_FUNCS[args.platform](search_command, args)
    search_result = search_result.json()
    # print(json.dumps(search_result, indent=2, ensure_ascii=False))

    data_arr_field = DATA_ARR_FIELDS[args.platform]
    data_arr = get_field_value(data_arr_field, search_result)
    if not data_arr:
        print(f"search_result: {search_result}")
        args.is_finished = True
        return None

    total_size_field = TOTAL_SIZE_FIELDS[args.platform]
    total_size = get_field_value(total_size_field, search_result)
    if has_search_finished(total_size, args):
        args.is_finished = True

    format_data = FORMAT_DATA_FUNCS[args.platform](args.needed_fields, data_arr)
    return format_data


def search_by_pages(keyword, search_command, result_files, args):
    if (total_pages := args.total_pages) < 1:
        print(f"!!! total pages must be greater than 1 !!!\n")
        return
    args.sum_page_size = 0
    args.is_finished = False

    for page in range(1, total_pages + 1):
        print(f"page: {page}, page_size: {args.page_size}")
        args.page = page

        format_data = send_platform_search(search_command, args)
        if format_data:
            seave_to_file(keyword, search_command, format_data, result_files, args)
            args.has_data_saved = True

        print(f"···delay {args.delay}s···\n")
        time.sleep(args.delay)

        if args.is_finished:
            break


def search_by_keywords(result_files, args):
    if keywords := args.keywords:
        keywords_lines = [keywords]
    elif keywords_file := args.keywords_file:
        keywords_lines = read_keywords(keywords_file)
    else:
        print("!!! keyword cannot be missing !!!\n")
        return

    for line in keywords_lines:
        keywords = re.split(r",|，| |、", line)
        for keyword in keywords:
            if keyword:
                print(f"key_word: [{keyword}]")
                args.keyword, args.is_new_keyword = keyword, True
                search_command = create_search_command(keyword, args.status_code, args.platform)
                search_by_pages(keyword, search_command, result_files, args)


def search_by_platforms():
    args = arguments_parse()
    supported_platforms = eval(get_config_value("supported_platforms", "platforms"))

    if args.platform == "all":
        platforms = supported_platforms
    else:
        platforms = re.split(r",|，|、", args.platform)

    for platform in platforms:
        print(f"platform:【{platform}】")
        if platform not in supported_platforms:
            print(f"!!! {platform} is not supported!", f"only support: {supported_platforms} !!!\n")
            continue
        args.platform = platform

        platform_url = get_config_value("platform_urls", f"{platform}_url")
        if not platform_url:
            print(f"!!! platform_url of {platform} is empty !!!\n")
            continue
        args.platform_url = platform_url

        api_key = get_config_value("api_keys", f"{platform}_key")
        if not api_key:
            print(f"!!! api_key of {platform} is empty !!!\n")
            continue
        args.api_key = api_key

        needed_fields = eval(get_config_value("needed_fields", f"{platform}_fields"))
        if not needed_fields:
            print(f"!!! needed_fields of {platform} is empty !!!\n")
            continue
        args.needed_fields = needed_fields

        result_files = init_result_files(args)
        search_by_keywords(result_files, args)
        end_result_files(result_files, args)


if __name__ == '__main__':
    # arguments_parse()
    search_by_platforms()
