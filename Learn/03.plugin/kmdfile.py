# -*- coding:utf-8 -*-
# Author: ColorLion

import k2rsa
import k2kmdfile

pu = k2rsa.read_key('key.pkr')  # 복호화 할 공개키를 로딩
k = k2kmdfile.KMD('dummy.kmd', pu)  # dummy.kmd 파일 읽기

# k.body에 dummy.kmd의 파이썬 코드가 복호화
module = k2kmdfile.load('dummy', k.body)
print dir(module)
