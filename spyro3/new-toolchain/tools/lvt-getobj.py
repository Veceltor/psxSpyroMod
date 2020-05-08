##Text extractor.


##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.

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

def jumper(filepath, start, jumpcount):
	jumpbuf = 0
	ifile = open(filepath, 'rb')
	for n in range(jumpcount):
		ifile.seek(start+jumpbuf)
		bytes0 = ifile.read(4)
		jumpbuf += struct.unpack('<I', bytes0)[0]

	return start+jumpbuf

def getObjectsList(filepath, subfile):
	varlen_list = list()

	wtmp = getSubfileInfo(filepath, subfile)	
	filestart = wtmp[0]
	sf_size = wtmp[1]

	objaddr = jumper(filepath, filestart+offset, jumps) + 8

	wad = open(filepath, 'rb')
	wad.seek(objaddr-4)
	objcount = struct.unpack('<I', wad.read(4))[0]	

	objlist = list()
	for x in range(objcount):
		wad.seek(objaddr+x*88)
		obuf = wad.read(88)
		varaddr = struct.unpack('<I', obuf[0:4])[0]
		
		wad.seek(filestart+varaddr)
		lentest = True

		if x < objcount-1:
			wad.seek(objaddr+(x+1)*88)
			obuf = wad.read(88)
			varaddr2 = struct.unpack('<I', obuf[0:4])[0]
			if (varaddr2 - varaddr) == 0:
				lentest = False
	
			if lentest:
				varlen_list.append(varaddr2 - varaddr)
				objlist.append(objaddr+x*88)
		else:
			varlen_list.append(sf_size - varaddr)
			objlist.append(objaddr+x*88)

	#multiple objects pointing to same var-memory case
	ret_objlist = list()
	for x in range(len(objlist)):
		dupobj = False

		wad.seek(objlist[x])
		obuf = wad.read(88)
		varaddr_x = struct.unpack('<I', obuf[0:4])[0]

		for y in range(len(objlist)):
			wad.seek(objlist[y])
			obuf = wad.read(88)
			varaddr_y = struct.unpack('<I', obuf[0:4])[0]

			if (varaddr_x == varaddr_y) and (not x == y):
				dupobj = True
		if not dupobj:
			ret_objlist.append(objlist[x])

	wad.close()

	return (objaddr, ret_objlist, varlen_list)

#def getLineCount():

def getSpeakingObjects(filepath, subfile):
	wtmp = getSubfileInfo(filepath, subfile)	
	filestart = wtmp[0]
	sf_size = wtmp[1]

	wtmp = getObjectsList(filepath, subfile)
	objaddr = wtmp[0]
	objlist = wtmp[1]
	varlen_list = wtmp[2]

	wad = open(filepath, 'rb')
	wad.seek(objaddr-4)
	sobj_var = list()
	sobj_varlen = list()

	for x in range(len(objlist)):
		wad.seek(objlist[x])
		obuf = wad.read(88)
		varaddr = struct.unpack('<I', obuf[0:4])[0]
		wad.seek(filestart+varaddr)
		lbuf = wad.read(256)

		lstart = struct.unpack('<I', lbuf[12:16])[0]
		if not (lstart == 0) and (lstart > varaddr) and (lstart < sf_size):
			wad.seek(filestart+lstart)
			idbyte = wad.read(1)[0]
			etest = wad.read(1)
			wad.seek(filestart+lstart+1)
			lTrig = True
			lsize = 0
			while lTrig:
				if etest[0] == 0:
					lTrig = False
				else:
					lsize += 1
				etest = wad.read(1)
					
			sobj_var.append(varaddr)
			sobj_varlen.append(varlen_list[x])
	
	return(sobj_var, sobj_varlen)

def getPointersAddr(filepath, subfile):
	ptr_list = list()

	wtmp = getSubfileInfo(filepath, subfile)	
	filestart = wtmp[0]
	sf_size = wtmp[1]

	wtmp = getObjectsList(filepath, subfile)
	objaddr = wtmp[0]
	objlist = wtmp[1]
	varlen_list = wtmp[2]

	wtmp = getSpeakingObjects(filepath, subfile)
	sobj_list = wtmp[0]
	sv_len_list = wtmp[1]

	wad = open(filepath, 'rb')

	for x in range(len(sobj_list)):
		varaddr = sobj_list[x]
		ptr_list.append(varaddr+12)
		ptr_list.append(0)
		
		wad.seek(filestart+varaddr)

		llist = list()
		plist = list()

		varlen = sv_len_list[x]
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

def getLineAddr(filepath, subfile, pointeraddr, namePointer):
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
	#wad.seek(txtstart)
	#etbuf = wad.read(lsize)
	wad.close()

	return (txtstart, lsize)

def loadTextFile(fpath):
	retList = list()

	tf = open(fpath, "r", encoding="utf-8")
	lcount = 0
	
	tfList = list()
	for line in tf.readlines():
		tfList.append(line[:-1])

	for l in range(int(len(tfList)/2)):
		retList.append(tfList[l*2+1])

	return retList


parser = argparse.ArgumentParser(description='Text extractor for Spyro 3.')
parser.add_argument('filepath', type=str, help = 'Path to level file.')
parser.add_argument('--output', type=str, default = 's3_text.txt', help = 'Output file name.')

args = parser.parse_args()

fpath = args.filepath
sfcount = getSubfilesCount(fpath)

for s in range(int((sfcount-4)/2)+1):
	ofile = open('output' + str(4+s*2) + '.txt', 'w', encoding='utf-8')
	wtmp = getSpeakingObjects(fpath, 4+s*2)
	for obj in range(len(wtmp[0])):
		ofile.write(str((wtmp[0])[obj]) + '\n')
		ofile.write(str((wtmp[1])[obj]) + '\n')
	ofile.close()

print('Text extraction completed.')
