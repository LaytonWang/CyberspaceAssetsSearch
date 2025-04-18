#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/25 9:27
# @Author : <Layton>
# @File : sens_info_search.py
import re
import time
import argparse

from common.hunter_search import search_by_hunter
from common.fofa_search import search_by_fofa
from common.quake_search import search_by_quake
from common.file_operation import read_key_words, get_config_value, result_file_judge, seave_to_file


def arguments_parse():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('platform', type=str, help='support: hunter、fofa、quake、all')

    keyword_group = arg_parser.add_mutually_exclusive_group()
    keyword_group.add_argument('-k', '--keyword', type=str, help='one keyword', default="")
    keyword_group.add_argument('-kf', '--keywords_file', type=str, help='like: keywords.csv', default="")

    arg_parser.add_argument('-rf', '--result_file', type=str, help='support: .txt .csv', default="")
    arg_parser.add_argument('-tp', '--total_pages', type=int, help='default: 1', default=1)
    arg_parser.add_argument('-pz', '--page_size', type=int, help='default: 10', default=10)
    arg_parser.add_argument('-sc', '--status_code', type=str, help='format: "200,302"', default="200")
    arg_parser.add_argument('-st', '--start_time', type=str, help='format: 2025-03-01', default="")
    arg_parser.add_argument('-et', '--end_time', type=str, help='format: 2025-03-30', default="")
    arg_parser.add_argument('-d', '--delay', type=float, help='default: 2.5', default=2.5)

    args = arg_parser.parse_args()
    # print(type(args), args)
    return args


def search_by_page(api_key, keyword, needed_fields, result_file, args):
    if (total_pages := args.total_pages) < 1:
        print(f"!!! total pages must be greater than 1 !!!\n")
        return

    for page in range(1, total_pages + 1):
        print(f"page: {page}, page_size: {args.page_size}")
        args.page = page
        format_data = eval(f"search_by_{args.platform}")(api_key, keyword, needed_fields, args)
        if format_data == "empty":
            print(f"···delay {args.delay}s···\n")
            time.sleep(args.delay)
            break
        if format_data:
            seave_to_file(needed_fields, format_data, result_file)
        print(f"···delay {args.delay}s···\n")
        time.sleep(args.delay)


def search_by_keywords(api_key, needed_fields, result_file, args):
    word_lines = []
    if keyword := args.keyword:
        word_lines = [keyword]
    elif keywords_file := args.keywords_file:
        word_lines = read_key_words(keywords_file)

    for line in word_lines:
        keywords = re.split(r",|，| |、", line)
        for keyword in keywords:
            if keyword:
                print(f"key_word:【{keyword}】")
                search_by_page(api_key, keyword, needed_fields, result_file, args)


def main():
    args = arguments_parse()
    supported_platforms = eval(get_config_value("supported_platforms", "platforms"))

    if args.platform == "all":
        platforms = supported_platforms
    else:
        platforms = re.split(r",|，|、", args.platform)

    for platform in platforms:
        print(f"platform: {platform}")
        if platform not in supported_platforms:
            print(f"!!! {platform} is not supported!", f"only support: {supported_platforms} !!!\n")
            continue
        args.platform = platform
        api_key = get_config_value("api_keys", f"{platform}_key")
        if not api_key:
            print(f"!!! api_key of {platform} is empty !!!\n")
            continue
        needed_fields = eval(get_config_value("needed_fields", f"{platform}_fields"))
        if not needed_fields:
            print(f"!!! needed_fields of {platform} is empty !!!\n")
            continue
        result_file = result_file_judge(args.result_file, platform)

        search_by_keywords(api_key, needed_fields, result_file, args)
        print(f"search result saved to {result_file}\n")


if __name__ == '__main__':
    # arguments_parse()
    main()

