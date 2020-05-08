import argparse
import struct
import string

jumps = 12 ## 8/12
offset = 48 ## 44/48
tenc = 'cp1251' ##cp932 or 1251

def isUppercase(tSym):
	retVal = False
	compStr = string.ascii_uppercase
	for symbol in compStr:
		if tSym == symbol:
			
			retVal = True
	return retVal

def getSubfileInfo(filepath, subfile):
	info_list = list()
	ifile = open(filepath, 'rb')
	ifile.seek((subfile-1)*8)
	info_list.append(struct.unpack('<I', ifile.read(4))[0])
	info_list.append(struct.unpack('<I', ifile.read(4))[0])
	ifile.close()

	return info_list

def getSubfilesCount(filepath):
	sfile = 1
	while sfile <= 256:
		tmpinfo = getSubfileInfo(filepath, sfile)
		if tmpinfo[0] == 0:
			break
		else:
			sfile += 1

	return sfile-1

def getLine(filepath, subfile, pointeraddr, namePointer):
	wad = open(filepath, 'rb')
	wtmp = getSubfileInfo(filepath, subfile)
	filestart = wtmp[0]
	sf_size = wtmp[1]

	wad.seek(filestart+pointeraddr)
	txtbuf = wad.read(4)
	lstart = struct.unpack('<I', txtbuf)[0]
	wad.seek(filestart+lstart)
	lTrig = True
	lsize = 0
	txtstart = filestart+lstart
	wad.seek(filestart+lstart)
	if (not namePointer):
		txtbuf = wad.read(1)
		txtstart = (filestart+lstart+txtbuf[0])
	wad.seek(filestart+lstart)
	txtbuf = wad.read(txtbuf[0])
			
	wad.seek(txtstart)
	while lTrig:
		if wad.read(1)[0] == 0:
			lTrig = False
		else:
			lsize += 1
	wad.seek(txtstart)
	etbuf = wad.read(lsize)
	wad.close()

	return etbuf.decode(tenc, 'ignore')

def getPointersAddr(filepath, subfile, varaddr, varlen):
	ptr_list = list()

	wtmp = getSubfileInfo(filepath, subfile)	
	filestart = wtmp[0]
	sf_size = wtmp[1]

	wad = open(filepath, 'rb')

	ptr_list.append(varaddr+12)
	ptr_list.append(0)
		
	wad.seek(filestart+varaddr)

	llist = list()
	plist = list()

	lbuf = wad.read(varlen)

	if varlen == 0:
		print('Bug - varlength...')

	for v in range(int(varlen/4)-4):
		lstart = struct.unpack('<I', lbuf[16+v*4:20+v*4])[0]
		if not lstart > varaddr:
			break
		elif not lstart < sf_size:
			break
		else:
			plist.append(varaddr+16+v*4)
			llist.append(lstart)	

	for tl in range(len(llist)):
		wad.seek(filestart+llist[tl])
		idbyte = wad.read(1)[0]
		if not idbyte == 255:
			ptr_list.append(plist[tl])
			ptr_list.append(1)

	wad.close()
	return ptr_list

def getTexts(filepath, subfile, objaddr, objvarlen):
	wtmp = getSubfileInfo(filepath, subfile)
	print(wtmp)
	filestart = wtmp[0]
	sf_size = wtmp[1]

	txt_list = list()
	pointers = getPointersAddr(filepath, subfile, objaddr, objvarlen)
	wad = open(filepath, 'rb')
	for t in range(int(len(pointers)/2)):
		if pointers[t*2+1] == 1:
			txt_list.append(getLine(filepath, subfile, pointers[t*2], False))
		else:
			txt_list.append(getLine(filepath, subfile, pointers[t*2], True))
		
	wad.close()
	return txt_list

def readConfig(cfgpath):
	cffile = open(cfgpath, 'r', encoding = 'utf-8')
	
	objList = list()
	objlenList = list()

	cfTrig = True
	for line in cffile.readlines():
		print(int(line))
		if cfTrig:
			objList.append(int(line))
			cfTrig = False
		else:
			objlenList.append(int(line))
			cfTrig = True

	return (objList, objlenList)

parser = argparse.ArgumentParser(description='Text extractor for Spyro 3.')
parser.add_argument('filepath', type=str, help = 'Path to level file.')
parser.add_argument('cfgpath', type=str, help = 'Path to config file.')
parser.add_argument('subfile', type=int, help = 'Subfile number.')
parser.add_argument('--output', type=str, default = 's3_text.txt', help = 'Output file name.')

args = parser.parse_args()

fpath = args.filepath
sfcount = getSubfilesCount(fpath)

ofile = open(args.output, 'w', encoding = 'utf-8')
cur_sf = args.subfile

oinfo = readConfig(args.cfgpath)
sobj_list = oinfo[0]
sv_len_list = oinfo[1]

for objindex in range(len(sobj_list)): 
	texts = getTexts(fpath, cur_sf, sobj_list[objindex], sv_len_list[objindex])
	ofile.write(str(sobj_list[objindex]) + '\n')
	ofile.write(str(sv_len_list[objindex]) + '\n')
	ofile.write(str(len(texts)) + '\n')
	for line in texts:
		ofile.write(line + '\n\n')
ofile.close()

print('Text extraction completed.')
