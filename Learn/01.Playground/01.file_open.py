import os

fp = open('eicar.txt', 'rb')
fbuf = fp.read()

if fbuf[0:3] == 'X50':  # 파일의 앞 3byte가 'X50'인가
    print 'Virus'
    os.remove('eicar.txt')  # 파일을 삭제해 치료
else:
    print 'no Virus'

fp.close()