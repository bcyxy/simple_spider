# -*- coding:utf-8 -*-

import logging
import random
import time
import urllib.request
from handle_union_key import union_key_handler

class DownloadTask(object):
    def __init__(self, spiders):
        self.__spiders = spiders
        self.__wait_tm_range = [1, 2]  # 随机等待时间范围，单位：秒
        self.__open_timeout = 10  # 爬虫超时时间，单位：秒

    def dnload_html_task(self, argv):
        union_key = argv
        req_dict = self.__spiders.gen_req(union_key)

        req_type = req_dict.get("type", "get")
        url = req_dict.get("url", "")
        headers = req_dict.get("header", {})
        post_data = req_dict.get("data", None)

        if req_type == "get":
            req_obj = urllib.request.Request(url, None, headers)
        elif req_type == "post":
            req_obj = urllib.request.Request(url, post_data, headers)
        else:
            return

        # 随机等待
        wait_tm = random.uniform(self.__wait_tm_range[0], self.__wait_tm_range[1])
        time.sleep(wait_tm)

        try:
            rsp_obj = urllib.request.urlopen(req_obj, timeout=self.__open_timeout)
            self.__spiders.handle_rsp(union_key, rsp_obj)
        except Exception as e:
            logging.warning("Download html fail. &e=%s" %str(e))
