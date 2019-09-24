# -*- coding:utf-8 -*-
# Author: ColorLion

import sys
import k2kmdfile

if __name__ == '__main__':
    # --------------------------------------------------------------------------------------
    # 인자값 체크
    # --------------------------------------------------------------------------------------
    if len(sys.argv) != 2:
        print 'Usage: kmake.py [python source]'
        exit()

    k2kmdfile.make(sys.argv[1], True)