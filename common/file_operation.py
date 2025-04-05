#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2025/3/25 20:48
# @Author : <Layton>
# @File : file_operation.py
import os
import csv
from datetime import datetime
from configparser import ConfigParser

from config import CONFIG_DIR, RESULTS_DIR


def get_config_value(section, key):
    # 创建ConfigParser对象
    conf = ConfigParser()
    # 读取ini文件
    conf.read(os.path.join(CONFIG_DIR, 'config.ini'), encoding="utf-8")
    # 获取值
    value = conf[f"{section}"][f"{key}"]
    return value


def read_key_words(file):
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


def csv_has_header(file):
    if not os.path.exists(file):
        # print(f"File is not exist!")
        return False
    if os.path.getsize(file) == 0:
        # print(f"File is empty!")
        return False

    with open(file, "r", encoding="utf-8-sig", newline='') as f:
        if not f.read(1024):
            # print(f"File (1024) is empty!")
            return False
    return True


def result_file_judge(file, platform):
    if not file:
        file_type = ".csv"
        cur_time = datetime.now().strftime('%Y%m%d-%H%M%S')
        result_file = os.path.join(RESULTS_DIR, f"{platform}_result_{cur_time}{file_type}")
    else:
        filename, file_type = os.path.splitext(file)
        if not file_type:
            file_type = ".csv"
        result_file = os.path.join(RESULTS_DIR, f"{filename}{file_type}")

    if os.path.exists(result_file):
        # os.remove(result_file)
        with open(result_file, 'a+', encoding='utf-8-sig') as f:
            f.truncate(0)
    return result_file


def seave_to_file(needed_fields, format_data, result_file):
    _, file_type = os.path.splitext(result_file)
    if file_type == ".txt":
        with open(result_file, "a", encoding="utf-8") as f:
            for data in format_data:
                # print(f"data: {data}")
                f.write(f"{','.join(data)}\n")
    elif file_type == ".csv":
        if not csv_has_header(result_file):
            with open(result_file, "a", encoding="utf-8-sig", newline='') as f:
                csv_writer = csv.writer(f)
                table_header = ["关键字", "查询命令", *needed_fields]
                # print(f"table_header: {table_header}")
                csv_writer.writerow(table_header)  # 写入表头
        with open(result_file, "a", encoding="utf-8-sig", newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(format_data)  # 写入数据行
    else:
        print("File type is not supported!")


if __name__ == '__main__':
    test_file = ""
    has_header = csv_has_header(test_file)
    print(has_header)
