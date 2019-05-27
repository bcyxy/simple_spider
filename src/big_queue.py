# -*- coding:utf-8 -*-
import os
import queue
import threading
import time


class BigStrQueue(threading.Thread):
    def __init__(self, f_dir="big_queue_dir", in_queue_limit=1024):
        self.__in_queue = queue.Queue()
        self.__out_queue = queue.Queue()
        self.__in_queue_limit = in_queue_limit
        self.__f_dir = f_dir
        try:
            os.makedirs(self.__f_dir)
        except:
            pass
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.start()

    def put(self, item, block=True, timeout=None):
        return self.__in_queue.put(item, block, timeout)
    
    def get(self, block=True, timeout=None):
        return self.__out_queue.get(block, timeout)
    
    def empty(self):
        return self.__out_queue.empty()

    def run(self):
        while True:
            time.sleep(0.5)
            if self.__in_queue.qsize() >= self.__in_queue_limit:
                self.__w_file()
            if self.__out_queue.empty():
                ## 检查文件
                fpath = self.__get_one_fpath()
                if fpath == "":
                    ## 触发输入队列写入文件
                    fpath = self.__w_file()
                if fpath != "":
                    ## 加载文件
                    self.__r_file(fpath)
    
    def __get_one_fpath(self):
        min_fname = "z"
        names = os.listdir(self.__f_dir)
        for name in names:
            if not name.startswith("bq_"):
                continue
            path = os.path.join(self.__f_dir, name)
            if not os.path.isfile(path):
                continue
            if name < min_fname:
                min_fname = name
        if min_fname != "z":
            return os.path.join(self.__f_dir, min_fname)
        return ""

    def __w_file(self):
        w_file_str = ""
        for i in range(0, self.__in_queue_limit):
            if self.__in_queue.empty():
                break
            w_file_str += self.__in_queue.get(block=False) + "\n"
        if w_file_str == "":
            return ""
        f_name = "bq_%f" %time.time()
        fpath = os.path.join(self.__f_dir, f_name)
        f_oh = open(fpath, "w")
        f_oh.write(w_file_str)
        f_oh.close()
        return fpath
    
    def __r_file(self, fpath):
        ## 读
        f_ih = open(fpath, "r")
        for line in f_ih:
            line = line.strip()
            if line == "":
                continue
            self.__out_queue.put(line)
        f_ih.close()

        ## 删除文件
        try:
            os.remove(fpath)
        except:
            pass


if __name__ == "__main__":  # For test
    my_queue = BigStrQueue()
    my_queue.put("asdf")
    time.sleep(1)
    print(my_queue.get(block=False))
