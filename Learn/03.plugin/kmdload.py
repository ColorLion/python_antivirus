# -*- coding:utf-8 -*-
# Author: ColorLion

import k2rsa
import k2kmdfile

pu = k2rsa.read_key('key.pkr')  # 복호화 할 공개키를 로딩
k = k2kmdfile.KMD('dummy.kmd', pu)  # dummy.kmd 파일 읽기

# k.body에 dummy.kmd 파이썬 코드가 복호화
module = k2kmdfile.load('dummy', k.body)  # dummy 플러그인 엔진 모듈을 등록

# --------------------------------------------------------------------------------------
# 사용방법 (1)
# kmdfile.load 함수의 리턴값으로 직접 사용 가능
# --------------------------------------------------------------------------------------
kav = module.KavMain()      # dummy 플러그인 엔진의 KavMain 인스턴스 생성
kav.init('.')               # 플러그인 엔진 초기화
print kav.getinfo()         # 플러그인 엔진 정보 확인
kav.uninit()                # 플러그인 엔진 종료