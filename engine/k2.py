# -*- coding:utf-8 -*-
# Author: ColorLion

import sys
import os
from ctypes import windll, Structure, c_short, c_ushort, byref
from optparse import OptionParser
import kavcore.k2engine


# ------------------------------------------------------------------------
# 주요 상수
# ------------------------------------------------------------------------
KAV_VERSION = '0.27'
KAV_BUILDDATE = 'SEP 09 2019'
KAV_LASTYEAR = KAV_BUILDDATE[len(KAV_BUILDDATE)-4:]

# ------------------------------------------------------------------------
# 콘솔에 색깔 출력을 위한 클래스 및 함수들
# ------------------------------------------------------------------------
FOREGROUND_BLACK = 0x0000
FOREGROUND_BLUE = 0x0001
FOREGROUND_GREEN = 0x0002
FOREGROUND_CYAN = 0x0003
FOREGROUND_RED = 0x0004
FOREGROUND_MAGENTA = 0x0005
FOREGROUND_YELLOW = 0x0006
FOREGROUND_GREY = 0x0007
FOREGROUND_INTENSITY = 0x0008   # foreground color is intensified.

BACKGROUND_BLACK = 0x0000
BACKGROUND_BLUE = 0x0001
BACKGROUND_GREEN = 0x0002
BACKGROUND_CYAN = 0x0003
BACKGROUND_RED = 0x0004
BACKGROUND_MAGENTA = 0x0005
BACKGROUND_YELLOW = 0x0006
BACKGROUND_GREY = 0x0007
BACKGROUND_INTENSITY = 0x0008   # background color is intensified

SHORT = c_short
WORD = c_ushort

class Coord(Structure):
    _fields_ = [
        ("X", SHORT),
        ("Y", SHORT)
    ]


class SmallRect(Structure):
    _fields_ = [
        ("Left", SHORT),
        ("Top", SHORT),
        ("Right", SHORT),
        ("Bottom", SHORT)
    ]


class ConsoleScreenBufferInfo(Structure):
    _fields_ = [
        ("dwSize", Coord),
        ("dwCursorPosition", Coord),
        ("wAttributes", WORD),
        ("srWindow", SmallRect),
        ("dwMaximumWindowSize", Coord)
    ]

# winbase.h
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo

def get_text_attr():
    csbi = ConsoleScreenBufferInfo()
    GetConsoleScreenBufferInfo(stdout_handle, byref(csbi))
    return csbi.wAttributes

def set_text_attr(color):
    SetConsoleTextAttribute(stdout_handle, color)

def cprint(msg, color):
    default_colors = get_text_attr()
    default_bg = default_colors & 0x00F0

    set_text_attr(color | default_bg)
    sys.stdout.write(msg)
    set_text_attr(default_colors)

    sys.stdout.flush()

def print_error(msg):
    cprint('Error: ', FOREGROUND_RED | FOREGROUND_INTENSITY)
    print(msg)

# ------------------------------------------------------------------------
# print_k2logo()
# 백신 로고 출력
# ------------------------------------------------------------------------
def print_k2logo():
    logo = '''KICOM Anti-Virus II (for %s) Ver %s (%s)
Copyright (C) 1995-%s ColorLion. All rights reserved.
'''

    print '---------------------------------------------------------------'
    s = logo % (sys.platform.upper(), KAV_VERSION, KAV_BUILDDATE, KAV_LASTYEAR)
    cprint(s, FOREGROUND_CYAN | FOREGROUND_INTENSITY)
    print '---------------------------------------------------------------'

# ------------------------------------------------------------------------
# 파이썬의 옵션 파서 정의
# 에러문을 세세하게 조정 가능
# ------------------------------------------------------------------------
class OptionParsingError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg

class OptionParsingExit(Exception):
    def __init__(self, status, msg):
        self.msg = msg
        self.status = status

class ModifiedOptionParser(OptionParser):
    def error(self, msg):
        raise OptionParsingError(msg)

    def exit(self, status=0, msg=None):
        raise OptionParsingExit(status, msg)

# ------------------------------------------------------------------------
# define_options()
# 백신의 옵션 정의
# ------------------------------------------------------------------------
def define_options():
    usage = 'Usage: %prog path[s] [options]'
    parser = ModifiedOptionParser(add_help_option=False, usage=usage)

    parser.add_option("-f", "--files", action="store_true", dest="opt_files", default=True)
    parser.add_option("-I", "--list", action="store_true", dest="opt_list", default=False)
    parser.add_option("-V", "--vlist", action="store_true", dest="opt_vlist", default=False)

    parser.add_option("-?", "--help", action="store_true", dest="opt_help", default=False)

    return parser

# ------------------------------------------------------------------------
# parser_options()
# 백신의 옵션 분석
# ------------------------------------------------------------------------
def parser_options():
    parser = define_options()

    if len(sys.argv) < 2 :
        return 'NONE_OPTION', None
    else:
        try:
            (options, args) = parser.parse_args()
            if len(args) == 0:
                return options, None
        except OptionParsingError, e:
            return 'ILLEGAL_OPTION', e.msg
        except OptionParsingExit, e:
            return 'ILLEGAL_OPTION', e.msg

        return options, args

# ------------------------------------------------------------------------
# print_usage()
# 백신의 사용법을 출력
# ------------------------------------------------------------------------
def print_usage():
    print '\nUsage: k2.py path[s] [options]'

# ------------------------------------------------------------------------
# print_options()
# 백신의 옵션 출력
# ------------------------------------------------------------------------
def print_options():
    options_string = \
    '''Options:
                    -f,      --files          scan files *
                    -I,      --list           display all files
                    -V,      --vlist          display virus list
                    -?,      --help           this help
                                              * = default option'''
    print options_string

# ------------------------------------------------------------------------
# listvirus의 콜백 함수
# ------------------------------------------------------------------------
def listvirus_callback(plugin_name, vnames):
    for vname in vnames:
        print '%-50s [%s.kmd]' % (vname, plugin_name)

# ------------------------------------------------------------------------
# main()
# ------------------------------------------------------------------------
def main():
    # 옵션 분석
    options, args = parser_options()

    # 로고 출력
    print_k2logo()

    # 잘못된 옵션인지 확인
    if options == 'NONE_OPTION':
        print_usage()
        print_options()
        return 0
    elif options == 'ILLEGAL_OPTION':
        print_usage()
        print 'Error: %s' % args
        return 0

    # help
    if options.opt_help:
        print_usage()
        print_options()
        return 0

    # 백신 엔진 구동
    k2 = kavcore.k2engine.Engine()
    if not k2.set_plugins('plugins'):
        print
        print_error('KICOM Anti-Virus Engine set_plugins')
        return 0

    kav = k2.create_instance()
    if not kav:
        print
        print_error('KICOM Anti-Virus Engine create_instance')
        return 0

    #if not kav.init():
    #    print
    #    print_error('KICOM Anti-Virus Engine init')
    #    return 0

    # 엔진 버전 출력
    c = kav.get_version()
    msg = '\rLast updated %s UTC\n\n' % c.ctime()
    cprint(msg, FOREGROUND_GREY)

    # 진단/치료 가능한 악성코드 수 출력
    msg = 'Signature number: %d\n\n' % kav.get_signum()
    cprint(msg, FOREGROUND_GREY)

    # 옵션 설정 > option을 통해 백신 커널로 전달
    kav.set_options(options)

    if options.opt_vlist is True:
        kav.listvirus(listvirus_callback)
    else:
        if args:
            # 검사용 Path(다중경로 지원)
            for scan_path in args:                      # 옵션을 제외한 첫 번째가 검사 대상
                scan_path = os.path.abspath(scan_path)

                if os.path.exists(scan_path):           # 폴더 혹은 파일이 존재하는가?
                    print scan_path
                else:
                    print_error('Invalid path: %s' % scan_path)

    kav.uninit()

if __name__ == '__main__':
    main()