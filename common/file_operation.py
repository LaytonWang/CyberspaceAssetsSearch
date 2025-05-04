#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/25 20:48
# @Author : <Layton>
# @File : file_operation.py
import os
from datetime import datetime
from configparser import ConfigParser

from config import CONFIG_DIR, RESULTS_DIR
from common.csv_utils import write_to_csv


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


def init_csv_file(result_file, needed_fields):
    table_header = [["关键字", "查询命令", *needed_fields]]
    write_to_csv(result_file, mode="a", data=table_header)


def init_result_file(result_file, platform, needed_fields):
    if not result_file:
        file_type = ".csv"
        cur_time = datetime.now().strftime('%Y%m%d-%H%M%S')
        result_file = os.path.join(RESULTS_DIR, f"{platform}_result_{cur_time}{file_type}")
    else:
        filename, file_type = os.path.splitext(result_file)
        if not file_type:
            file_type = ".csv"
        result_file = os.path.join(RESULTS_DIR, f"{filename}{file_type}")

    if os.path.exists(result_file):
        with open(result_file, 'a+', encoding='utf-8-sig') as f:
            f.truncate(0)

    init_csv_file(result_file, needed_fields)
    return result_file


def seave_to_file(needed_fields, format_data, result_file):
    _, file_type = os.path.splitext(result_file)

    if file_type == ".csv":
        write_to_csv(result_file, mode="a", data=format_data)
    else:
        print("File type is not supported!")


if __name__ == '__main__':
    pass
