# -*- coding: utf-8 -*-
import os
import hashlib

# 악성코드 검사 진행
def ScanVirus(vdb, vsize, sdb, fname):
    print '[*] New Scan Virus'

    #MD5 해시를 이용해 악성코드 검사
    ret, vname = ScanMD5(vdb, vsize, fname)
    if ret == True:
        return ret, vname

    #특정위치 검사법
    fp = open(fname, 'rb')
    for t in sdb:
        if ScanStr(fp, t[0], t[1]) == True:
            ret = True
            vname = t[2]
            break
    fp.close()

    return ret, vname

#악성코드 검사
def SearchVDB(vdb, fmd5):
    for t in vdb:
        if t[0] == fmd5:
            return True, t[1]
    return False, ''

# MD5를 이용해 악성코드 검사
def ScanMD5(vdb, vsize, fname):
    ret = False #악성코드 발견 유무
    vname = ''  #발견된 악성코드명

    size = os.path.getsize(fname)   #검사 대상 파일 크기
    if vsize.count(size):
        fp = open(fname, 'rb')
        buf = fp.read()
        fp.close()

        m = hashlib.md5()
        m.update(buf)
        fmd5 = m.hexdigest()

        ret, vname = SearchVDB(vdb, fmd5)

    return ret, vname

#특정 위치검색
def ScanStr(fp, offset, mal_str):
    size = len(mal_str)

    # 특정 위치에 악성코드 문자열이 존재하는지 체크
    fp.seek(offset) #악성코드 문자열 예상위치로 이동
    buf = fp.read(size) #악성코드 문자열만큼 읽기

    if buf == mal_str:
        return True #악성코드  on
    else:
        return False #악성코드 off