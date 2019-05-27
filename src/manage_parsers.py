# -*- coding:utf-8 -*-

import glob
import logging
import os

class ParsersManager(object):
    def __init__(self):
        self.parsers_dir = "src/parsers/"
        self.import_path_base = "parsers."
        self.module_no_parser = set([
            "__init__",
        ])
        self.parsers_pool = {}

    def load_parsers(self):
        module_fpath_list = glob.glob("%s*.py" %self.parsers_dir)
        for module_fpath in module_fpath_list:
            module_fname = os.path.basename(module_fpath)
            module_name, ext = os.path.splitext(module_fname)
            if module_name in self.module_no_parser:
                continue
            import_path = "%s%s" %(self.import_path_base, module_name)
            parser_module = __import__(import_path, {} , {}, [module_name])
            
            # check parser module
            getattr(parser_module, "parser_key")
            getattr(parser_module, "handle_rsp")
            getattr(parser_module, "make_req")
            
            # add parser pool
            parser_key = parser_module.parser_key
            self.parsers_pool[parser_key] = parser_module
            
            logging.info("Load parser module file success. &fpath='%s'" %module_fpath)

    def gen_req(self, union_key):
        parser_module = self.__get_parser_module(union_key)
        if parser_module == None:
            logging.info("Have no parser_module for union_key. &union_key='%s'" %union_key)
            return
        try:
            req_dict = parser_module.make_req(union_key)
        except Exception as e:
            logging.warning(
                "Call parser_module.gen_req error. "
                "&union_key='%s' &e='%s'" 
                %(union_key, str(e))
            )
            return None
        return req_dict

    def handle_rsp(self, union_key, rsp_obj):
        parser_module = self.__get_parser_module(union_key)
        if parser_module == None:
            logging.info("Have no parser_module for union_key. &union_key='%s'" %union_key)
            return
        try:
            parser_module.handle_rsp(union_key, rsp_obj)
        except Exception as e:
            logging.warning(
                "Call parser_module.handle_rsp error. "
                "&union_key='%s' &e='%s'" 
                %(union_key, str(e))
            )
    
    def __get_parser_module(self, union_key):
        uk_slices = union_key.split("||||")
        if len(uk_slices) != 3:
            logging.debug("Union_key formal error. &union_key='%s'" %union_key)
            return
        parser_key = uk_slices[0].strip()
        parser_module = self.parsers_pool.get(parser_key, None)
        return parser_module
