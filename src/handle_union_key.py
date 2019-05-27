# -*- coding:utf-8 -*-

import logging

class UnionKeyHandler(object):
    def __init__(self):
        self.uk_delimiter = "||||"
        self.uk_slices_len = 3

    def make_union_key(self, spider_key, req_time, sub_key):
        # Check parameters.
        try:
            int(req_time)
        except:
            logging.warning("Make union_key error. &req_time=%s" %str(req_time))
            return
            
        union_key = (
            "%s%s%s%s%s" 
            %(
                spider_key, self.uk_delimiter, 
                req_time, self.uk_delimiter, sub_key
            )
        )
        return union_key
        
    def split_union_key(self, union_key):
        uk_slices = union_key.split(self.uk_delimiter)
        if len(uk_slices) != self.uk_slices_len:
            logging.warning("Split union_key error. &union_key=%s" %union_key)
            return
        spider_key = uk_slices[0]
        try:
            req_time = int(uk_slices[1])
        except:
            logging.warning("Split union_key error. &union_key=%s" %union_key)
            return
        sub_key = uk_slices[2]
        
        union_key_mult = (spider_key, req_time, sub_key)
        return union_key_mult
        

union_key_handler = UnionKeyHandler()
