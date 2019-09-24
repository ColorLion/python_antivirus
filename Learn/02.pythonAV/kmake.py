# -*- coding: utf-8 -*-
import sys
import zlib
import hashlib
import os

# Encrypt
def main():
    if len(sys.argv) != 2:
        print 'Usage : kmake.py'
        return

    fname = sys.argv[1] # 대상 파일 읽기
    tname = fname

    fp = open(tname, 'rb')
    buf = fp.read()
    fp.close()

    buf2 = zlib.compress(buf)

    buf3 = ''
    for c in buf2:  # 대상 파일 내용을 압축
        buf3 += chr(ord(c) ^ 0xFF)

    buf4 = 'KAVM' + buf3    # 헤더 생성

    f = buf4
    for i in range(3):  # 지금까지의 내용을 MD5 Hash
        md5 = hashlib.md5()
        md5.update(f)
        f = md5.hexdigest()

    buf4 += f   #암호화 된 내용뒤에 추가

    kmd_name = fname.split('.')[0] + '.kmd'
    fp = open(kmd_name, 'wb')
    fp.write(buf4)
    fp.close()

    print '%s -> %s' % (fname, kmd_name)

if __name__ == '__main__':
    main()