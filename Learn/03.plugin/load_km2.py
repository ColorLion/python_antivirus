import k2rsa
import kmdfile


pu = k2rsa.read_key('key.pkr')
k = kmdfile.KMD('dummy.kmd', pu)

module = kmdfile.load('dummy', k.body)
