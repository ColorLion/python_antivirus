# -*- coding: utf-8 -*-
import sys, os, hashlib

VirusDB = []
vdb = []
vsize = []

def LoadVirusDB():
    fp = open('virus.db', 'rb')

    while True:
        line = fp.readline()
        if not line: break

        line = line.strip()
        VirusDB.append(line)

    fp.close()

# VirusDB를 가공해 vdb에 저장
def MakeVirusDB():
    for pattern in VirusDB:
        t = []
        v = pattern.split(':')
        t.append(v[1])
        t.append(v[2])
        vdb.append(t)

        size = int(v[0])
        if vsize.count(size) == 0:
            vsize.append(size)

#악성코드 검사
def SearchVDB(fmd5):
    for t in vdb:
        if t[0] == fmd5:
            return True, t[1]
    return False, ''

if __name__ == '__main__':
    MakeVirusDB()

    # 커맨드 라인으로 악성코드 검사
    # 커맨드라인의 입력방식 체크
    if len(sys.argv) != 2:
        print 'Usage: antivirus.py [file]'
        exit(0)

    # 악성코드 검사 대상 파일
    fname = sys.argv[1]

    size = os.path.getsize(fname)
    if vsize.count(size):
        fp = open(fname, 'rb')
        buf = fp.read()
        fp.close()

        m = hashlib.md5()
        m.update(buf)
        fmd5 = m.hexdigest()

        ret, vname, = SearchVDB(fmd5)
        if ret == True:
            print '%s : %s' % (fname, vname)
            os.remove(fname)
        else:
            print '%s : ok' % (fname)