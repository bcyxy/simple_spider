# -*- coding:utf-8 -*-

import os, sys
root_dir = sys.path[0]
sys.path.append(root_dir)
sys.path.append(root_dir + "/src")
import glb_vals
glb_vals.g_root_abs_dir = root_dir
from src import main


if __name__ == "__main__":
    pass
    main.main(root_dir)
