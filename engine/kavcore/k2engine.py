# -*- coding:utf-8 -*-
# Author: ColorLion

import os
import StringIO
import datetime
import types
import mmap

import k2kmdfile
import k2rsa

# ------------------------------------------------------------------------
# Engine 클래스
# ------------------------------------------------------------------------
class Engine:
    # ------------------------------------------------------------------------
    # __init__(self, debug=False)
    # 클래스를 초기화
    # 인자값:  debug - 디버그 여부
    # ------------------------------------------------------------------------
    def __init__(self, debug=False):
        self.debug = debug  # 디버깅 여부

        self.plugins_path = None    # 플러그인 경로
        self.kmdfiles = []          # 우선순위가 기록된 kmd 리스트
        self.kmd_modules = []       # 메모리에 로딩된 모듈

        # 플러그인 엔진의 가장 최신 시간 값을 가짐
        # 초기값으론 1980-01-01 지정
        self.max_datetime = datetime.datetime(1980, 1, 1, 0, 0, 0, 0)

    # ------------------------------------------------------------------------
    # set_plugins(self, plugins_path)
    # 주어진 경로에서 플러그인 엔진을 로딩 준비
    # 인자값:  plugins_path - 플러그인 엔진 경로
    # 리턴값:  성공 여부
    # ------------------------------------------------------------------------
    def set_plugins(self, plugins_path):
        # 플러그인 경로 저장
        self.plugins_path = plugins_path
        #print 'plugins_path: ' + plugins_path

        # 공개키 로딩
        pu = k2rsa.read_key(plugins_path + os.sep + 'key.pkr')
        #print pu
        if not pu:
            return False

        # 우선순위 체크
        ret = self.__get_kmd_list(plugins_path + os.sep + 'kicom.kmd', pu)
        if not ret:
            return False

        if self.debug:
            print '[*] load kicom.kmd:'
            print '   ', self.kmdfiles

        # 우선순위 대로 KMD파일 로딩
        for kmd_name in self.kmdfiles:
            kmd_path = plugins_path + os.sep + kmd_name
            k = k2kmdfile.KMD(kmd_path, pu)                         # 모든 KMD 파일 복호화
            module = k2kmdfile.load(kmd_name.split('.')[0], k.body)

            if module:      # 메모리 로딩 성공
                self.kmd_modules.append(module)
                # 메모리 로딩에 성공한 KMD에서 플러그인 엔진의 시간 값 읽기
                # 최신 업데이트 날짜가 된다
                self.__get_last_kmd_build_time(k)

        if self.debug:
            print '[*] kmd_modules:'
            print '     ', self.kmd_modules
            print '[*] Last updated %s UTC' % self.max_datetime.ctime()

        return True


    # ------------------------------------------------------------------------
    # __get_last_kmd_build_time(self, kmd_info)
    # 복호화된 플러그인 엔진의 빌드 시간 값 중 최신 값 보관
    # 인자값:  kmd_info - 복호화된 플러그인 엔진 정보
    # ------------------------------------------------------------------------
    def __get_last_kmd_build_time(self, kmd_info):
        d_y, d_m, d_d = kmd_info.date
        t_h, t_m, t_s = kmd_info.time
        t_datetime = datetime.datetime(d_y, d_m, d_d, t_h, t_m, t_s)

        if self.max_datetime < t_datetime:
            self.max_datetime = t_datetime


    # ------------------------------------------------------------------------
    # __get_kmd_list(self, kicom_kmd_file, pu)
    # 인자값:  kicom_kmd_file  - kicom.kmd 파일의 전체 경로
    #         pu              - 공개키
    # 리턴값:  성공여부
    # ------------------------------------------------------------------------
    def __get_kmd_list(self, kicom_kmd_file, pu):
        kmdfiles = []   # 우선순위 목록

        k = k2kmdfile.KMD(kicom_kmd_file, pu)       # kicom.kmd 파일 복호화

        if k.body:      # kicom.kmd파일이 읽혔는가?
            msg = StringIO.StringIO(k.body)

            while True:
                # 한줄을 읽어 엔터키 제거
                line = msg.readline().strip()

                if not line:
                    break
                elif line.find('.kmd') != -1:   # KMD 확장자가 존재한다면
                    kmdfiles.append(line)       # KMD 우선순위 목록에 추가
                else:
                    continue

        if len(kmdfiles):                       # 우선순위 목록의 내용이 1줄이라도 있다면
            self.kmdfiles = kmdfiles
            return True
        else:                                   # 우선순위 목록의 내용이 없다면
            return False

    # ------------------------------------------------------------------------
    # create_instance(self):
    # 백신 엔진의 인스턴스 생성
    # ------------------------------------------------------------------------
    def create_instance(self):
        ei = EngineInstance(self.plugins_path, self.max_datetime, self.debug)
        if ei.create(self.kmd_modules):
            return ei
        else:
            return None


class EngineInstance:
    # ------------------------------------------------------------------------
    # __init__(self, plugins_path, max_datetime, debug=False)
    # 클래스 초기화
    # 인자값:  plugins_path - 플러그인 엔진 경로
    #         max_datetime - 플러그인 엔진의 최신 시간 값
    #         debug        - 디버그 여부
    # 리턴값:  성공여부
    # ------------------------------------------------------------------------
    def __init__(self, plugins_path, max_datetime, debug=False):
        self.debug = debug                  # 디버깅 여부

        self.plugins_path = plugins_path    # 플러그인 경로
        self.max_datetime = max_datetime    # 플러그인 엔진의 최신 시간 값

        self.options = {}                   # 옵션
        self.set_options()                  # 기본옵션 설정

        self.kavmain_inst = []              # 모든 플러그인의 KavMain 인스턴스


    # ------------------------------------------------------------------------
    # create(self, kmd_modules)
    # 백신 엔진의 인스턴스 생성
    # 인자값:  kmd_modules - 메모리에 로딩된 kmd 리스트
    # 리턴값:  성공여부
    # ------------------------------------------------------------------------
    def create(self, kmd_modules):
        for mod in kmd_modules:
            try:
                t = mod.KavMain()  # 각 플러그인 KavMain 인스턴스 생성
                self.kavmain_inst.append(t)
            except AttributeError:  # KavMain 클래스가 존재하지 않음
                continue

        if len(self.kavmain_inst):
            if self.debug:
                print '[*] Count of KavMain : %d' % (len(self.kavmain_inst))
            return True
        else:
            return False

    # ------------------------------------------------------------------------
    # init(self)
    # 플러그인 엔진 전체 초기화
    # 리턴값:  성공여부
    # ------------------------------------------------------------------------
    def init(self):
        # self.kavmain_inst는 최종 인스턴스가 아님
        # init 초기화 명령어를 실행 해 정상인 플러그인 만 최종 등록
        t_kavmain_inst = []

        if self.debug:
            print '[*] KavMain.init()'

        for inst in self.kavmain_inst:
            try:
                # 플러그인 엔진의 init함수 호출
                #ret = inst.init(self.plugins_path)
                ret = inst.init()
                if not ret:
                    t_kavmain_inst.append(inst)

                    if self.debug:
                        print '[-] %s.inst() :%d' % (inst.__module__, ret)
            except AttributeError:
                continue

        self.kavmain_inst = t_kavmain_inst  # 최종 인스턴스 등록

        if len(self.kavmain_inst):
            if self.debug:
                print '[*] Count of KavMain.init() : %d' % (len(self.kavmain_inst))

                return True
        else:
            return False

    # ------------------------------------------------------------------------
    # uninit(self)
    # 플러그인 엔진 전체 종
    # 리턴값:  성공여부
    # ------------------------------------------------------------------------
    def uninit(self):
        if self.debug:
            print '[*] KavMain.uninit()'

        for inst in self.kavmain_inst:
            try:
                ret = inst.uninit()
                if self.debug:
                    print '[-] %s.uninit() : %d'  % (inst.__module__, ret)
            except AttributeError:
                continue


    # ------------------------------------------------------------------------
    # getinfo(self)
    # 플러그인 엔진 정보를 얻음
    # 리턴값: 플러그인 엔진 정보 리스트
    # ------------------------------------------------------------------------
    def getinfo(self):
        ginfo = []  # 플러그인 엔진 정보 저장할 배열

        if self.debug:
            print '[*] KavMain.getinfo()'

        for inst in self.kavmain_inst:
            try:
                ret = inst.getinfo()
                ginfo.append(ret)

                if self.debug:
                    print   '       [-] %s.getinfo() : ' % inst.__module__
                    for key in ret.keys():
                        print '         - %-10s : %s' % (key, ret[key])
            except AttributeError:
                continue

        return ginfo

    # ------------------------------------------------------------------------
    # listvirus(self, *callback)
    # 플러그인 엔진이 진단/치료할 수 있는 악성코드 목록을 얻음
    # 입력값:  callback - 콜백 함수(생략 가능)
    # 리턴값:  악성코드 (콜백함수 사용 시 아무런 값도 없음)
    # ------------------------------------------------------------------------
    def listvirus(self, *callback):
        vlist = []  # 진단/치료 가능한 악성코드 목록

        argc = len(callback)

        if argc == 0:   # 인자가 없으면
            cb_fn = None
        elif argc == 1: # callback함수가 존재하는지 체크
            cb_fn = callback[0]
        else:           # 인자가 너무 많으면
            return []

        if self.debug:
            print '[*] KavMain.listvirus()'

        for inst in self.kavmain_inst:
            try:
                ret = inst.listvirus()

                # callback 함수가 있다면 callback 함수 호출
                if isinstance(cb_fn, types.FunctionType):
                    cb_fn(inst.__module__, ret)
                else:   # callback함수가 없다면 악성코드 목록을 누적하여 리턴
                    vlist += ret

                if self.debug:
                    print '     [-] %s.listvirus() :' % inst.__module__
                    for vname in ret:
                        print '         - %s' % vname
            except AttributeError:
                continue

        return vlist


    # ------------------------------------------------------------------------
    # scan(self, filename)
    # 플러그인 엔진에게 악성코드 검사를 요청
    # 입력값:  fielname - 악성코드 검사 대상 파일 이름
    # 리턴값:  (악성코드 발견 유무, 악성코드 이름, 악성코드 ID, 플러그인 엔진 ID)
    # ------------------------------------------------------------------------
    def scan(self, filename):
        if self.debug:
            print '[*] KavMain.scan()'

        try:
            ret = False
            vname = ''
            mid = -1
            eid = -1

            fp = open(filename, 'rb')
            mm = mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ)

            for i, inst in enumerate(self.kavmain_inst):
                try:
                    ret, vname, mid = inst.scan(mm, filename)
                    if ret:                                         # 악성코드 발견 시 추가 악성코드 검사 중단
                        eid = i                                     # 악성코드를 발견한 플러그인 엔진 ID

                        if self.debug:
                            print '[-] %s.scan() : %s' % (inst.__module__, vname)

                        break
                except AttributeError:
                    continue

            if mm:
                mm.close()
            if fp:
                fp.close()

            return ret, vname, mid, eid
        except IOError:
            pass

        return False, '', -1, -1


    # ------------------------------------------------------------------------
    # disinfect(self, filename, malware_id, engine_id)
    # 플러그인 엔진에게 악성코드 치료 요청
    # 입력값:  fielname - 악성코드 치료 대상 파일 이름
    #         malware_id - 악성코드 id
    #         engine_id  - 악성코드를 발견한 엔진 id
    # 리턴값:  악성코드 치료 여부
    # ------------------------------------------------------------------------
    def disinfect(self, filename, malware_id, engine_id):
        ret = False

        if self.debug:
            print '[*] KavMain.disinfect(): '

        try:
            # 악성코드 진단 플러그인 엔진에게 치료 요청
            inst = self.kavmain_inst[engine_id]
            ret = inst.disinfect(filename, malware_id)

            if self.debug:
                print '     [-] %s.disinfect() : %s' % (inst.__module__, ret)
        except AttributeError:
            pass

        return ret

    # ------------------------------------------------------------------------
    # get_version(self)
    # 전체 플러그인 엔진의 최신 버전 정보 전달
    # 리턴값: 최신 버전 정보
    # ------------------------------------------------------------------------
    def get_version(self):
        return self.max_datetime

    # ------------------------------------------------------------------------
    # get_signum(self)
    # 백신 엔진이 진단/치료 가능한 악성코드 수를 얻음
    # 리턴값: 진단/치료 가능한 악성코드 수
    # ------------------------------------------------------------------------
    def get_signum(self):
        signum = 0

        for inst in self.kavmain_inst:
            try:
                ret = inst.getinfo()

                # 플러그인 엔진 정보에 진단/치료 가능한 악성코드 수 누적
                if 'sig_num' in ret:
                    signum += ret['sig_num']
            except AttributeError:
                continue

        return signum

    # ------------------------------------------------------------------------
    # set_options(self, options)
    # 옵션을 설정
    # ------------------------------------------------------------------------
    def set_options(self, options=None):
        if options:
            self.options['opt_list'] = options.opt_list
        else:
            self.options['opt_list'] = False
        return True