#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2025/5/4 17:29
# @Author: <Layton>
# @File: html_utils.py
import os
import time
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from config import RESULTS_DIR, TEMPLATES_DIR

__all__ = ['read_from_html', 'write_to_html', 'create_table_header', 'create_table_body', 'init_html_base',
           'init_html_panel', 'init_html_table', 'update_table_body', 'end_clear', ]

TEMP_ENV = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
RESULT_ENV = Environment(loader=FileSystemLoader(RESULTS_DIR))


def read_from_html(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        html_text = f.read()
        return html_text


def write_to_html(html_file, mode="w", html_text=None):
    with open(html_file, mode, encoding="utf-8") as f:
        f.write(html_text)


def create_table_header(header_data):
    table_header = "<tr>"
    table_header += f'<th data-field="index" data-sortable="true">index</th>'
    for item in header_data:
        table_header += f'<th data-field="{item}" data-sortable="true">{item}</th>'
    table_header += "</tr>"
    return table_header


def create_table_body(header_data, body_data, data_index):
    table_body = "<tr>"
    table_body += f"<td>{data_index}</td>"
    for header_item, body_item in zip(header_data, body_data):
        if header_item in ["url", "link"]:
            body_item = f'<a href="{body_item}" target="_blank">{body_item}</a>'
        table_body += f"<td>{body_item}</td>"
    table_body += "</tr>"
    return table_body


def init_html_base(result_file):
    template = TEMP_ENV.get_template("base_template.html")
    html_text = template.render(title=os.path.basename(result_file), panel="{{ panel }}")
    write_to_html(result_file, mode="w", html_text=html_text)


def init_html_panel(keyword, search_command, result_file):
    collapse_id = f"collapse_{datetime.now().strftime('%H%M%S')}"

    template = TEMP_ENV.get_template("panel_template.html")
    panel_text = template.render(keyword=keyword, search_command=search_command, collapse_id=collapse_id,
                                table="{{ table }}")
    template = RESULT_ENV.get_template(os.path.basename(result_file))
    html_text = template.render(panel=panel_text + "{{ panel }}")
    time.sleep(0.1)
    write_to_html(result_file, mode="w", html_text=html_text)


def init_html_table(table_header, result_file):
    template = TEMP_ENV.get_template("table_template.html")
    table_text = template.render(table_header=table_header, table_body="{{ table_body }}")
    template = RESULT_ENV.get_template(os.path.basename(result_file))
    html_text = template.render(table=table_text, panel="{{ panel }}")
    time.sleep(0.1)
    write_to_html(result_file, mode="w", html_text=html_text)


def update_table_body(table_body, result_file):
    template = RESULT_ENV.get_template(os.path.basename(result_file))
    html_text = template.render(table_body=table_body + "{{ table_body }}", panel="{{ panel }}")
    time.sleep(0.5)
    write_to_html(result_file, mode="w", html_text=html_text)


def end_clear(result_file):
    template = RESULT_ENV.get_template(os.path.basename(result_file))
    html_text = template.render()
    time.sleep(0.1)
    write_to_html(result_file, mode="w", html_text=html_text)


if __name__ == '__main__':
    pass
