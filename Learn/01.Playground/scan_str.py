# -*- coding: utf-8 -*-

#특정 위치검색
def ScanStr(fp, offset, mal_str):
    size = len(mal_str)

    # 특정 위치에 악성코드 문자열이 존재하는지 체크
    fp.seek(offset) #악성코드 문자열 예상위치로 이동
    buf = fp.read(size) #악성코드 문자열만큼 읽기

    if buf == mal_str:
        return True
    else:
        return False

#파일을 읽어 악성코드 검사
fp = open('eicar.txt', 'rb')
print ScanStr(fp, 0, 'X50')
fp.close()