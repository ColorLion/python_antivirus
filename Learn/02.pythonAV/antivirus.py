# -*- coding: utf-8 -*-
import sys, hashlib
import zlib, StringIO
import scanmod
import curemod
import imp

VirusDB = []
vdb = []
sdb = []
vsize = []

# Decrypt
def DecodeKMD(fname):
    try:
        fp = open(fname, 'rb')
        buf = fp.read()
        fp.close()

        buf2 = buf[:-32]    #암호화 내용 분리 > 헤더 제거
        fmd5 = buf[-32:]    #MD5 분리 > 푸터 제거

        f = buf2
        for i in range(3):  #암호화 내용의 MD5를 구함 > 파일이 변조되었는지 확인
            md5 = hashlib.md5()
            md5.update(f)
            f = md5.hexdigest()

        if f != fmd5:   #MD5가 서로 동일한가?
            raise SystemError

        buf3 = ''
        for c in buf2[4:]:  #0xFF로 XOR
            buf3 += chr(ord(c) ^ 0xFF)

        buf4 = zlib.decompress(buf3)
        return buf4
    except:
        pass

    return None

def LoadVirusDB():
    buf = DecodeKMD('virus.kmd')
    fp = StringIO.StringIO(buf)

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

        scan_func = v[0]    #악성코드 검사 함수
        cure_func = v[1]    #악성코드 치료 함수

        if scan_func == 'ScanMD5':
            t.append(v[3])
            t.append(v[4])
            vdb.append(t)

            size = int(v[2])
            if vsize.count(size) == 0:
                vsize.append(size)
        elif scan_func == 'ScanStr':
            t.append(int(v[2]))
            t.append(v[3])
            t.append(v[4])
            sdb.append(t)

if __name__ == '__main__':
    LoadVirusDB()
    MakeVirusDB()

    # 커맨드 라인으로 악성코드 검사
    # 커맨드라인의 입력방식 체크
    if len(sys.argv) != 2:
        print 'Usage: antivirus.py [file]'
        sys.exit(0)

    # 악성코드 검사 대상 파일
    fname = sys.argv[1]

    try:
        m = 'scanmod'
        f, filename, desc = imp.find_module(m, [''])
        module = imp.load_module(m, f, filename, desc)
        # 진단함수 호출 명령어 구성
        cmd = 'ret, vname = module.ScanVirus(vdb, vsize, sdb, fname)'
        exec cmd
    except ImportError:
        ret, vname = scanmod.ScanVirus(vdb, vsize, sdb, fname)

    if ret == True:
        print '%s : %s' % (fname, vname)
        curemod.CureDelete(fname)
    else:
        print '%s : ok' % (fname)