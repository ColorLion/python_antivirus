# coding=utf-8

import os

class KavMain:
    #--------------------------------------------------------------------------------------
    # init(self, plugins_path)
    # 플러그인 엔진 초기화
    # 인자값: plugins_path - 플러그인 엔진 위치
    # 리턴값: 0 - 성공, 0이외의 값 - 실패
    #--------------------------------------------------------------------------------------
    def init(self, plugin_path):    # 플러그인 엔진 초기화
        # 진단/치료하는 악성코드 이름
        self.virus_name = 'Dummy-Test File (not a virus)'
        # 악성코드 패턴 등록
        self.dummy_pattern = 'Dummy Engine test file - Anti-Virus Project'

        return 0    # 플러그인 엔진 초기화 성공

    #--------------------------------------------------------------------------------------
    # uninit(self)
    # 플러그인 엔진 종료
    #--------------------------------------------------------------------------------------
    def uninit(self):        # 플러그인 엔진 종료
        del self.virus_name    #메모리 해제(악성코드 이름 관련)
        del self.dummy_pattern    # 메모리 해제(악성코드 패턴)

        return 0    # 플러그인 엔진 종료 성공

    #--------------------------------------------------------------------------------------
    # scan(self, filehandle, filename)
    # 악성코드 검사
    # 인자값    :    filehandle    - 파일 핸들
    #          :    filename      - 파일 이름
    # 리턴값    :    (악성코드 발견 여부, 악성코드 이름, 악성코드 ID) 등등
    #--------------------------------------------------------------------------------------
    def scan(self, filehandle, filename):
        try:
            # 파일을 열어 악성코드 패턴만큼 파일에서 읽는다
            fp = open(filename)
            buf = fp.read(len(self.dummy_pattern))        #패턴은 49Byte 크기
            fp.close()

            # 악성코드 패턴 비교
            if buf == self.dummy_pattern:
                # 악성코드 패턴이 같다면 결과 값을 리턴
                return True, self.virus_name, 0
        except IOError:
            pass

        # 악성코드를 발견하지 못한 경우
        return False, '', -1

    #--------------------------------------------------------------------------------------
    # disinfect(self, filename, malware_id)
    # 악성코드 치료
    # 인자값    :    filehandle    - 파일 핸들
    #          :    malware_id    - 치료할 악성코드 ID
    # 리턴값    :    악성코드 치료 여부
    #--------------------------------------------------------------------------------------
    def disinfect(self, filename, malware_id):    # 악성코드 치료
        try:
            # 악성코드 진단 결과에서 받은 ID 값이 0인가?
            if malware_id == 0:
                os.remove(filename)
                return True
        except IOError:
            pass
        return False    # 치료 실패 시 리턴

    # --------------------------------------------------------------------------------------
    # listvirus(self)
    # 진단/치료 가능한 악성코드의 목록 출력
    # 리턴값    :    악성코드 목록
    # --------------------------------------------------------------------------------------
    def listvirus(self):
        vlist = list()

        vlist.append(self.virus_name)  # 진단/치료하는 악성코드 이름 등록

        return vlist

    # --------------------------------------------------------------------------------------
    # getinfo(self)
    # 플러그인 엔진의 주요 정보 출력(제작자, 버전 등등)
    # 리턴값    :    플러그인 엔진 정보
    # --------------------------------------------------------------------------------------
    def getinfo(self):
        info = dict()

        info['author'] = 'ColorLion'  # 제작자
        info['version'] = '1.0'  # 버전
        info['title'] = 'Dummy Scan Engine'  # 엔진 설명
        info['kmd_name'] = 'dummy'  # 엔진 파일 이름

        return info