import argparse
import struct
import os

parser = argparse.ArgumentParser(description='Unpacker for WAD.WAD archive.')
parser.add_argument('filepath', type=str, help = 'Path to WAD.WAD.')
parser.add_argument('subfile', type=int, help = 'Subfile number.')
##parser.add_argument('--part', type=int, default=0, help = 'Read header of subfile and extract only n-th part. 0 (default) - extract whole file instead.')

args = parser.parse_args()

sf = args.subfile - 1
##ssf = args.part
ssf = 0
path = args.filepath

f = open(path, 'rb')

header = f.read(2048)
addr = struct.unpack('<I', header[0+sf*8:4+sf*8])[0]
sfsize = struct.unpack('<I', header[4+sf*8:8+sf*8])[0]

f.seek(addr)
subfile = f.read(sfsize)

ofile = open('sf.bin', 'wb')

if ssf == 0:
	ofile.write(subfile)
	
elif ssf > 0:
	pass
	
else:
	print('Wrong part number: ' + str(ssf))
	
f.close()
ofile.close()