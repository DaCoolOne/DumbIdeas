

import gzip

test_string = "This is a test string".encode()

bytes = gzip.compress(test_string)

# 11110xxx	10xxxxxx	10xxxxxx	10xxxxxx
def unicode_compress(bytes):
    o = b'E'
    for c in bytes:
        v = (c-11)%133-21
        o += ((v >> 6) & 1 | 0b11001100).to_bytes(1,'big')
        o += ((v & 63) | 0b10000000).to_bytes(1,'big')
    return o

def unicode_decompress(b):
    return ''.join([chr(((h<<6&64|c&63)+22)%133+10)for h,c in zip(b[1::2],b[2::2])])

with open("in.py", 'r') as inp:
    with open("out.py", 'wb') as f:
        orig = inp.read()
        c = unicode_compress(orig.encode('utf8'))
        test_back = unicode_decompress(c)
        print(orig == test_back)
        f.write(b"b='"+c+b"'.encode()\nexec(''.join(chr(((h<<6&64|c&63)+22)%133+10)for h,c in zip(b[1::2],b[2::2])))")

