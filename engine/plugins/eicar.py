# -*- coding:utf-8 -*-
# Author: ColorLion

import os
import cryptolib

#--------------------------------------------------------------------------------------
# KavMain 클래스
#--------------------------------------------------------------------------------------
class KavMain:
    #--------------------------------------------------------------------------------------
    # init(self, plugins_path)
    # 플러그인 엔진 초기화
    # 인자값: plugins_path - 플러그인 엔진 위치
    # 리턴값: 0 - 성공, 0이외의 값 - 실패
    #--------------------------------------------------------------------------------------
    def init(self):
        return 0    # 플러그인 엔진 초기화

    #--------------------------------------------------------------------------------------
    # uninit(self)
    # 플러그인 엔진 종료
    # 리턴값: 0 - 성공, 0이외의 값 - 실패
    #--------------------------------------------------------------------------------------
    def uninit(self):
        return 0    # 플러그인 엔진 종료 성공

    #--------------------------------------------------------------------------------------
    # scan(self, filehandle, filename)
    # 악성코드 검사
    # 인자값: filehandle - 파일 핸들
    #        filename   - 파일 이름
    # 리턴값: (악성코드 발견 여부, 악성코드 이름, 악성코드ID) 등등
    #--------------------------------------------------------------------------------------
    def scan(self, filehandle, filename):
        try:
            mm = filehandle

            size = os.path.getsize(filename)    # 검사 대상 파일의 크기 계산
            if size == 68:
                # 크기가 일치한다면 MD5 해시 계산
                fmd5 = cryptolib.md5(mm[:68])

                # 파일에서 얻은 해시 값과 EICAR Test 악성코드의 해시 값이 일치하는가?
                if fmd5 == '44d88612fea8a8f36de82e1278abb02f':
                    return True, 'EICAR-Test-File (not a virus)', 0
        except IOError:
            pass

    # 악성코드 발견 못하면
        return False, '', -1

    # --------------------------------------------------------------------------------------
    # disinfect(self, filename, malware_id)
    # 악성코드 치료
    # 입력값:  filename - 파일이름
    #         malware_id - 치료할 악성코드 id
    # 리턴값: 악성코드 치료 여부
    # --------------------------------------------------------------------------------------
    def disinfect(self, filename, malware_id):
        try:
            # 악성코드 진단 결과에서 받은 id값이 0인가?
            if malware_id == 0:
                os.remove(filename)
                return True
        except IOError:
            pass

        return False

    #--------------------------------------------------------------------------------------
    # listvirus(self)
    # 진단/치료 가능한 악성코드 목록 출력
    # 리턴값: 악성코드 목록
    #--------------------------------------------------------------------------------------
    def listvirus(self):
        vlist = list()

        # 진단/치료하는 악성코드 이름 등록
        vlist.append('EICAR-Test-File (not a virus)')

        return vlist

    #--------------------------------------------------------------------------------------
    # getinfo(self)
    # 플러그인 엔진 주요정보 출력
    # 리턴값: 플러그인 엔진 정보
    #--------------------------------------------------------------------------------------
    def getinfo(self):
        info = dict()

        info['author'] = 'ColorLion'
        info['version'] = '1.1'
        info['title'] = 'EICAR Scan Engine'
        info['kmd_name'] = 'eicar'
        info['sig_num'] = 1

        return info