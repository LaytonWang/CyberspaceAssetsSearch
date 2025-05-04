#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2025/5/3 15:55
# @Author: <Layton>
# @File: csv_utils.py
import os
import csv


def csv_has_header(file):
    if not os.path.exists(file):
        return False
    if os.path.getsize(file) == 0:
        return False
    with open(file, "r", encoding="utf-8-sig", newline='') as f:
        if not f.read(1024):
            return False
    return True


def write_to_csv(file, mode="a", data=None):
    with open(file, mode, encoding="utf-8-sig", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(data)


def read_from_csv(file):
    with open(file, "r", encoding="utf-8-sig") as f:
        csv_reader = csv.reader(f)
        yield from csv_reader


if __name__ == '__main__':
    pass
