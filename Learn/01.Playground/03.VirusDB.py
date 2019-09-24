# -*- coding: utf-8 -*-

# Dic
VirusDB = [
    '44d88612fea8a8f36de82e1278abb02f:EICAR Test',
    '77bff0b143e480ae73d4582a8914a43:Dummy Test'
]

vdb = []  # 가공된 악성코드 DB가 저장

def MakeViursDB():
    for pattern in VirusDB:
        t = []
        v = pattern.split(':')
        t.append(v[0])
        t.append(v[1])
        vdb.append(t)

MakeViursDB()
print(vdb)