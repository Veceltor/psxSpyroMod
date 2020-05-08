import struct

def getJumpAddr(fpath, jumps, offset, sublevel):
	wad = open(fpath, 'rb')
	wad.seek(8*(3+sublevel*2))
	bytes0 = wad.read(8)
	filestart = struct.unpack('<I', bytes0[0:4])[0]
	sf_size = struct.unpack('<I', bytes0[4:8])[0]
	jumpbuf = 0
	objlist = list()
	jstart = 0
	for n in range(jumps+1):
		wad.seek(filestart+offset+jumpbuf)
		bytes0 = wad.read(4)
		jumpbuf += struct.unpack('<I', bytes0)[0]
		if n == (jumps-1):
			jstart = filestart+offset+jumpbuf

	jend = filestart+offset+jumpbuf
	wad.close()
	return (jstart, jend)



sfpath = input("Enter path to file: ")
slnum = int(input("Enter sublevel number (0 - main level): "))

dbuf = getJumpAddr(sfpath, 8, 48, slnum)
print(dbuf)

