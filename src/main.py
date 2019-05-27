# -*- coding:utf-8 -*-
import os
import glb_vals
import logging
from logging.handlers import TimedRotatingFileHandler
def initial():
    r_hander = TimedRotatingFileHandler(
        filename = os.path.join(glb_vals.g_root_abs_dir, "./log/ou.log"),
        when = 'D',
        interval = 1,
        backupCount = 10,
        encoding = None, 
        delay = False, 
        utc = False
    )
    fmt = logging.Formatter(
        fmt='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(message)s',
        datefmt='%Y%m%d_%H%M%S'
    )
    r_hander.setFormatter(fmt)
    logging.getLogger().addHandler(r_hander)
    log_level = getattr(logging, "DEBUG")
    logging.getLogger().setLevel(log_level)
initial()

import time
from big_queue import BigStrQueue
from download import DownloadTask
from manage_parsers import ParsersManager
from threadpool import ThreadPool


def main(root_dir):
    ## 加载爬虫模块
    parsers_manager = ParsersManager()
    parsers_manager.load_parsers()

    ## 初始化爬虫任务
    download_task = DownloadTask(parsers_manager)

    glb_vals.g_in_queue = BigStrQueue(f_dir=os.path.join(glb_vals.g_root_abs_dir,
                                                         "data",
                                                         "big_queue_dir"))

    ## 创建下载线程
    download_threads = ThreadPool(download_task.dnload_html_task, glb_vals.g_in_queue, None, 5)
    download_threads.start()
    
    while True:
        time.sleep(10)
