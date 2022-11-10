

# Compress algorithm
def unicode_compress(bytes):
    o = b'E'
    for c in bytes:
        # Skip carriage returns
        if c == 13:
            continue
        # Check for invalid code points
        if (c < 20 or c > 126) and c != 10:
            raise Exception("Cannot encode character with code point " + str(c))
        # Code point translation
        v = (c-11)%133-21
        o += ((v >> 6) & 1 | 0b11001100).to_bytes(1,'big')
        o += ((v & 63) | 0b10000000).to_bytes(1,'big')
    return o

# Decompress algorithm (Code golfed)
def unicode_decompress(b):
    return ''.join([chr(((h<<6&64|c&63)+22)%133+10)for h,c in zip(b[1::2],b[2::2])])

# If run as main, use argv[1] for input, argv[2] for output
if __name__ == "__main__":
    import sys

    with open(sys.argv[1] if len(sys.argv) >= 2 else "in.py", 'r', encoding='utf8') as inp:
        with open(sys.argv[2] if len(sys.argv) >= 3 else "out.py", 'wb') as f:

            # Read input file.
            orig = inp.read()

            # Compress
            E = unicode_compress(orig.encode('utf8'))

            # Check that everything worked according to keikaku
            test_back = unicode_decompress(E)
            print("This should be True: ", all(a == b for a,b in zip(orig.splitlines(),test_back.splitlines())))

            # Write output to file, along with code-golfed decompressor.
            f.write(b"b='"+E+b"'.encode();exec(''.join(chr(((h<<6&64|c&63)+22)%133+10)for h,c in zip(b[1::2],b[2::2])))")

