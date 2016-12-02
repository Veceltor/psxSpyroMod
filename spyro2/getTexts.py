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

jumps = 8 ## 9/13
offset = 44 ## 44/48
tenc = 'cp1251' ##cp932 or 1251

parser = argparse.ArgumentParser(description='Text extractor for Spyro 2.')
parser.add_argument('filepath', type=str, help = 'Path to level file.')
parser.add_argument('--output', type=str, default = 's2_text.txt', help = 'Output file name.')


args = parser.parse_args()

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

def jumper(filepath, start, jumpcount):
	jumpbuf = 0
	ifile = open(filepath, 'rb')
	for n in range(jumpcount):
		ifile.seek(start+jumpbuf)
		bytes0 = ifile.read(4)
		jumpbuf += struct.unpack('<I', bytes0)[0]

	return start+jumpbuf

def getPointersAddr(filepath, subfile):
	vardat_list = list()
	varlen_list = list()
	ptr_list = list()

	wtmp = getSubfileInfo(filepath, subfile)	
	filestart = wtmp[0]
	sf_size = wtmp[1]

	print(filestart+offset)
	objaddr = jumper(filepath, filestart+offset, jumps) + 8
	print(objaddr)

	wad = open(filepath, 'rb')
	wad.seek(objaddr-4)
	objcount = struct.unpack('<I', wad.read(4))[0]	

	objlist = list()

	for x in range(objcount):
		wad.seek(objaddr+x*88)
		obuf = wad.read(88)
		varaddr = struct.unpack('<I', obuf[0:4])[0]
		
		wad.seek(filestart+varaddr)
		lbuf = wad.read(64)

		lentest = True

		if x < objcount-1:
			wad.seek(objaddr+(x+1)*88)
			obuf = wad.read(88)
			varaddr2 = struct.unpack('<I', obuf[0:4])[0]
			if (varaddr2 - varaddr) < 20:
				lentest = False
	
			if lentest:
				varlen_list.append(varaddr2 - varaddr)
				objlist.append(objaddr+x*88)

	##print(objlist)
	rlist = list()
	for x in range(len(objlist)):
		wad.seek(objlist[x])
		obuf = wad.read(88)
		varaddr = struct.unpack('<I', obuf[0:4])[0]
		wad.seek(filestart+varaddr)
		lbuf = wad.read(256)
		
		onum = int((objlist[x]-objaddr)/88)
		lstart = struct.unpack('<I', lbuf[12:16])[0]
		if lstart > varaddr and lstart < sf_size:
			wad.seek(filestart+lstart)
			idbyte = wad.read(1)[0]
			etest = wad.read(1)
			wad.seek(filestart+lstart+1)
			if not idbyte == 255 and len(etest) == 1:
				lTrig = True
				lsize = 0
				while lTrig:
					if etest[0] == 0:
						lTrig = False
					else:
						lsize += 1
					etest = wad.read(1)
					
				if lsize > 2:
					ptr_list.append(varaddr+12)
					ptr_list.append(0)

		wad.seek(filestart+varaddr)
		llist = list()
		plist = list()
		errcount = 0

		varlen = varlen_list[x]
		
		for v in range(int(varlen/4)-4):
			lstart = struct.unpack('<I', lbuf[16+v*4:20+v*4])[0]
			errcount = 0
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
				txt = filestart+llist[tl]+idbyte
				wad.seek(txt)

				lTrig = True
				lsize = 0
				while lTrig:
					if wad.read(1)[0] == 0:
						lTrig = False
					else:
						lsize += 1

				wad.seek(txt)
				tbuf = wad.read(lsize)
				if (lsize > 2):
					ptr_list.append(plist[tl])
					ptr_list.append(1)
	wad.close()
	return ptr_list

def getTexts(filepath, subfile):
	wtmp = getSubfileInfo(filepath, subfile)	
	filestart = wtmp[0]
	sf_size = wtmp[1]

	txt_list = list()
	pointers = getPointersAddr(filepath, subfile)	

	wad = open(filepath, 'rb')
	for t in range(int(len(pointers)/2)):
		wad.seek(filestart+pointers[t*2])
		txtbuf = wad.read(4)
		lstart = struct.unpack('<I', txtbuf)[0]
		wad.seek(filestart+lstart)
		lTrig = True
		lsize = 0
		txtstart = filestart+lstart
		wad.seek(filestart+lstart)
		if (pointers[t*2 + 1] == 1):
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
		
		txt_list.append(etbuf.decode(tenc, 'ignore'))
		
	wad.close()
	return txt_list

fpath = args.filepath
texts = getTexts(fpath, 4)

ofile = open(args.output, 'w', encoding = 'utf-8')
for line in texts:
	ofile.write(line + '\n')
ofile.close()
