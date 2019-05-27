# -*- coding:utf-8 -*-

import sys
import threading


# worker主动从任务队列中取任务
# 完成任务后将结果放到输出队列中
class Worker(threading.Thread):
    def __init__(self, task_func, in_queue, out_queue, worker_id):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.worker_id = worker_id
        self.task_func = task_func
        self.__in_queue = in_queue
        self.__out_queue = out_queue

    def run(self):
        while True:
            task_argv = self.__in_queue.get()  # 阻塞函数
            try:
                run_rst = self.task_func(task_argv)
            except Exception as e:
                print(e)
                continue
            if self.__out_queue != None:
                self.__out_queue.put(run_rst)


# 多线程执行用户的任务函数
class ThreadPool(object):
    # out_queue为None时，task_func的返回值直接丢弃
    def __init__(self, task_func, in_queue, out_queue, threads_count):
        self.__in_queue = in_queue
        self.__out_queue = out_queue
        self.workers = []
        for i in range(threads_count):
            worker = Worker(task_func, self.__in_queue, self.__out_queue, i)
            self.workers.append(worker)
    
    def start(self):
        for work in self.workers:
            work.start()


if __name__ == "__main__":  # For test
    # 任务函数
    # 要求：必须只有一个参数
    def test_func(aaa):
        a, b = aaa
        return a, a + b

    # 输入输出队列
    import queue
    in_queue = queue.Queue()
    out_queue = queue.Queue()

    # 构建和启动线程池
    thread_pool = ThreadPool(test_func, in_queue, out_queue, 5)
    thread_pool.start()

    # 任务入队
    for i in range(0, 200):
        in_queue.put((i, i + 1))
    
    # 结果出队
    import time
    time.sleep(1)
    while not out_queue.empty():
        print(out_queue.get())
