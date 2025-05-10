#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/25 20:48
# @Author : <Layton>
# @File : file_operation.py
import os
import itertools
from datetime import datetime
from configparser import ConfigParser

from config import PROJECT_BASE_DIR, CONFIG_DIR, RESULTS_DIR
from common.csv_utils import write_to_csv, init_csv_file
from common.html_utils import *

__all__ = ['get_config_value', 'read_keywords', 'init_result_files', 'end_result_files', 'seave_to_file', ]


def get_config_value(section, key):
    conf = ConfigParser()
    conf.read(os.path.join(CONFIG_DIR, 'config.ini'), encoding="utf-8")
    value = conf[f"{section}"][f"{key}"]
    return value


def read_keywords(file):
    if os.access(file, os.F_OK) is not True:
        print(f"File ({file}) is not exist!")
        return
    elif os.access(file, os.R_OK) is not True:
        print(f"File ({file}) is unreadable!")
        return

    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            # print(line.strip())
            yield line.strip()


def init_result_files(args):
    result_files, file_types = [], [".csv", ".html"]
    args.has_data_saved = False
    os.makedirs(RESULTS_DIR, exist_ok=True)

    if not args.result_file:
        cur_datetime = datetime.now().strftime('%Y%m%d-%H%M%S')
        for file_type in file_types:
            result_file = os.path.join(RESULTS_DIR, f"{args.platform}_result_{cur_datetime}{file_type}")
            result_files.append(result_file)
    else:
        filename, file_type = os.path.splitext(args.result_file)
        if file_type not in file_types:
            file_type = ".csv"
        result_file = os.path.join(RESULTS_DIR, f"{filename}{file_type}")
        result_files.append(result_file)

    for result_file in result_files:
        if os.path.exists(result_file):
            with open(result_file, 'a+', encoding='utf-8') as f:
                f.truncate(0)

        if result_file.endswith(".csv"):
            init_csv_file(result_file, args.needed_fields)
        elif result_file.endswith(".html"):
            init_html_base(result_file)

    return result_files


def end_result_files(result_files, args):
    if not args.has_data_saved:
        for result_file in result_files:
            os.remove(result_file)
        print("No result was saved!\n")
        return

    for result_file in result_files:
        if result_file.endswith(".html"):
            end_clear(result_file)

    rel_result_file = os.path.relpath(RESULTS_DIR, PROJECT_BASE_DIR)
    print(f"Search result saved to: .\\{rel_result_file}\\ \n")


def seave_to_file(keyword, search_command, format_data, result_files, args):
    format_datas = itertools.tee(format_data, len(result_files))

    for i, result_file in enumerate(result_files):
        _, file_type = os.path.splitext(result_file)

        if file_type == ".csv":
            csv_data = ([keyword, search_command, *item] for item in format_datas[i])
            write_to_csv(result_file, mode="a", data=csv_data)
        elif file_type == ".html":
            if args.is_new_keyword:
                args.data_index = 1
                init_html_panel(keyword, search_command, result_file)
                table_header = create_table_header(args.needed_fields)
                init_html_table(table_header, result_file)
                args.is_new_keyword = False

            table_body = ""
            for body_data in format_datas[i]:
                table_body += create_table_body(args.needed_fields, body_data, args.data_index)
                args.data_index += 1
            update_table_body(table_body, result_file)
        else:
            print("File type is not supported!")


if __name__ == '__main__':
    pass
