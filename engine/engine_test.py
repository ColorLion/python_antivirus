# -*- coding:utf-8 -*-
# Author: ColorLion

import kavcore.k2engine

# listvirus의 callback함수
def listvirus_callback(plugin_name, vnames):
    for vname in vnames:
        print '%-50s [%s.kmd]' % (vname, plugin_name)


k2 = kavcore.k2engine.Engine(debug=True)
if k2.set_plugins('plugins'):       # 성공?
    kav = k2.create_instance()      # 백신 엔진 인스턴스 생성
    if kav:
        print '[*] Success : create_instance'

        ret = kav.init()
        info = kav.getinfo()

        vlist = kav.listvirus(listvirus_callback) # 플러그인의 바이러스 목록 출력

        print '[*] Used Callback        : %d' % len(vlist)

        vlist = kav.listvirus()                   # 플러그인의 바이러스 목록을 얻음
        print '[*] Not used Callback: %d' % len(vlist)

        # 스캔
        #ret, vname, mid, eid = kav.scan('eicar.txt')

        #if ret:
        #    kav.disinfect('eicar.txt', mid, eid)
        kav.uninit()