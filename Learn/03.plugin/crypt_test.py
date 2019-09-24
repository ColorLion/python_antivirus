import k2rsa
import k2kmdfile

k2rsa.create_key('key.pkr', 'key.skr')

ret = k2kmdfile.make('kicom.lst')
if ret:
    pu = k2rsa.read_key('key.pkr')
    k = k2kmdfile.KMD('kicom.kmd', pu)
    print k.body