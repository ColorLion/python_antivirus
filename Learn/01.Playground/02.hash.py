# coding=utf-8
import hashlib
import os

fp = open('eicar.txt', 'rb')
fbuf = fp.read()
fp.close()

m = hashlib.md5()
m.update(fbuf)
fmd5 = m.hexdigest()

# EICAR test file MD5와 비교
if fmd5 == '44d88612fea8a8f36de82e1278abb02f':
    print 'virus'
    os.remove('eicar.txt')
elif fmd5 == '77bff0b143e480ae73d4582a8914a43':
    print 'Dummy virus'
else:
    print 'no virus'
