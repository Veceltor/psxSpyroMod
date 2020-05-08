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

parser = argparse.ArgumentParser(description='Text insert tool for Spyro 3.')
parser.add_argument('filepath', type=str, help = 'Path to level file.')
parser.add_argument('txtpath', type=str, help = 'Path to text file.')
parser.add_argument('subfile', type=int, help = 'Subfile number (4, 6, 8...).')
parser.add_argument('cfgpath', type=str, help = 'Path to sc.ini.')
parser.add_argument('--output', type=str, default = 's3_text.txt', help = 'Output file name.')


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
	cfgBuf = tf.readlines()

	curLine = 0
	while curLine < len(cfgBuf):
		tfList = list()
		objaddr = int(cfgBuf[curLine])
		curLine += 1
		varlen = int(cfgBuf[curLine])
		curLine += 1
		strCount = int(cfgBuf[curLine])
		curLine += 2
		tfList.append(objaddr)
		tfList.append(varlen)
		tfList.append(strCount)
		for cl in range(strCount):
			tfList.append(cfgBuf[curLine])
			curLine += 2
		curLine -= 1
		retList.append(tfList)

	return retList

def piratecode(textline, cfgpath):
    import configparser
    config = configparser.ConfigParser()
    config.read(cfgpath, encoding = 'cp1251')
    stb = bytes.fromhex("")
    for symbol in textline:
        bytes0 = symbol.encode(encoding='cp1251', errors='ignore')
        try:
            stb += int((config['BYTES'])[str(bytes0[0])]).to_bytes(1, byteorder='little')
        except KeyError:
            stb += bytes0
    return stb

def pasteText(filepath, subfile, textpath, cfgpath):
	wtmp = getSubfileInfo(filepath, subfile)
	filestart = wtmp[0]
	sf_size = wtmp[1]

	textList = loadTextFile(textpath)

	wad = open(filepath, 'r+b')
	for oc in range(len(textList)):
		curData = textList[oc]
		pointers = getPointersAddr(filepath, subfile, int(curData[0]), int(curData[1]))

		for t in range(int(curData[2])):
			if pointers[t*2+1] == 1:
				wtmp = getLineAddr(filepath, subfile, pointers[t*2], False)
			else:
				wtmp = getLineAddr(filepath, subfile, pointers[t*2], True)
			
			wad.seek(wtmp[0])
			lsize = wtmp[1]
			if not curData[t+3] == "[SKIP]\n":
				etbuf = piratecode((curData[t+3])[0:-1], cfgpath)
				if len(etbuf) <= lsize:
					etbuf = etbuf + (bytes.fromhex("00")*(lsize-len(etbuf)))
					wad.write(etbuf)
				else:
					print("Line is too long, skipping.")
					print((curData[t+3])[0:-1])
			else:
				print("Skipped line.")
		
	wad.close()

fpath = args.filepath
sfcount = getSubfilesCount(fpath)

print(fpath)

pasteText(fpath, args.subfile, args.txtpath, args.cfgpath)

print('Completed.')
