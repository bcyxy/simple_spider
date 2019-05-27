# -*- coding:utf-8 -*-

import re
import glb_vals
from handle_union_key import union_key_handler


parser_key = "tkd"

limit_set = set()

url_reg = re.compile(r'https?:\\?/\\?/[\w\d\.\-]+')
title_reg = re.compile(r'<title>([^<]+)</title>')
def handle_rsp(union_key, rsp_obj):
    parser_key, req_time, sub_key = union_key_handler.split_union_key(union_key)
    
    content_type = rsp_obj.headers.get("Content-Type", "")
    if not content_type.startswith("text/html"):
        return
    html_str = rsp_obj.read().decode('utf-8')

    # 取title
    re_rst = title_reg.findall(html_str)
    if len(re_rst) > 0:
        print(sub_key, re_rst[0])

    # 跳转
    re_rst = url_reg.findall(html_str)
    for new_url in re_rst:
        new_url = new_url.replace("\\", "")
        if new_url in limit_set or len(limit_set) > 2000:
            continue
        limit_set.add(new_url)
        
        new_union_key = "%s||||1||||%s" %(parser_key, new_url)
        glb_vals.g_in_queue.put(new_union_key)


def make_req(union_key):
    parser_key, req_time, sub_key = union_key_handler.split_union_key(union_key)

    req_dict = {
        "type": "get",
        "url": sub_key,
        "header": {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Accept-Encoding": "deflate",
        },
        "date": {},
    }
    return req_dict
