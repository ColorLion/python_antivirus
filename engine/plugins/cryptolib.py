# -*- coding:utf-8 -*-
# Author: ColorLion

import hashlib

# ---------------------------------------------------------------------
# md5(data)
# 주어진 데이터에 대해 MD5 해시를 구한다
# 입력값:  data - 데이터
# 리턴값:  MD5해시 문자열
# ---------------------------------------------------------------------
def md5(data):
    return hashlib.md5(data).hexdigest()

# ------------------------------------------------------------------------
# KavMain 클래스
# ------------------------------------------------------------------------
class kavMain:
    # ------------------------------------------------------------------------
    # init(self, plugins-path)
    # 플러그인 엔진 초기화
    # 인자값:  plugins_path - 플러그인 엔진 위치
    # 리턴값:  0 - 성공 / 0이외의 값 - 실패
    # ------------------------------------------------------------------------
    def init(self, plugins_path):
        return 0

    # ------------------------------------------------------------------------
    # uninit(self)
    # 플러그인 엔진 종료
    # 리턴값:  0 - 성공 / 0이외의 값 - 실패
    # ------------------------------------------------------------------------
    def uninit(self):
        return 0

    # ------------------------------------------------------------------------
    # getinfo(self)
    # 플러그인 엔진 정보 출력
    # 리턴값:  플러그인 엔진 정보
    # ------------------------------------------------------------------------
    def getinfo(self):
        info = dict()

        info['author'] = 'ColorLion'        # 제작자
        info['version'] = '1.0'             # 버전
        info['title'] = 'Crypto Libary'     # 엔진 설명
        info['kmd_name'] = 'cryptolib'      # 엔진파일 이름

        return info