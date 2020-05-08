import struct
import argparse
import os

def readSector(filepath, lba):
	f = open(filepath, 'rb')
	f.seek(lba*2352+24)
	sData = f.read(2048)
	f.close()

	return sData

def processDirectory(dtb, dirName):
	entryLen = dtb[0]
	procBytes = 0
	resList = list()

	while entryLen > 0:
		fType = 'unknown'

		entry = dtb[procBytes:procBytes+entryLen]
		fLba = struct.unpack('<I', entry[2:6])[0]
		fSize = struct.unpack('<I', entry[10:14])[0]
		nEnd = 33
		fName = dirName

		for e in range(entryLen-33):
			if e == 0:
				if entry[e+33] == 0:
					fName = '.'
					nEnd = 34
					break
				elif entry[e+33] == 1:
					fName = '..'
					nEnd = 34
					break
			if not entry[e+33] == 0:
				fName += entry[e+33:e+34].decode('cp1251', 'ignore')
			else:
				nEnd = 33+e
				break
		idByte = 0
		for x in range(entryLen-nEnd):
			idByte = (entry[nEnd+x:nEnd+x+1])[0]
			if not idByte == 0:
				break
			
		if idByte == 141:
			fType = 'directory'
		elif idByte == 37:
			fType = 'file-m2f2'
			fName = fName[:len(fName)-2]
		elif idByte == 13:
			fType = 'file-m2f1'
			fName = fName[:len(fName)-2]

		resList.append((fType, fName, fLba, fSize))
		procBytes += entryLen
		entryLen = dtb[procBytes]
	return resList

def readDirectory(dLba, dName):
	dirData = readSector(fPath, dLba)
	dirContent = processDirectory(dirData, dName)
	fileList = list()
	for n in dirContent:
		if not n[0] == 'directory':
			fileList.append(n)

	dirList = list()

	for n in dirContent:
		if n[0] == 'directory':
			if not (n[1] == '.' or n[1] == '..'):
				dirList.append(n)

	return (fileList, dirList)

def extractFile(imgPath, eMode, ePath, eLba, eSize):
	dataSize = 2048
	if eMode == 'file-m2f2':
		dataSize = 2324
	cdImg = open(imgPath, 'rb')
	cdImg.seek(eLba*2352)

	outFile = open(ePath, 'wb')
	logFile = open('./cdx-log.txt', 'a', encoding='utf-8')
	logFile.write('Extracting ' + (os.path.split(ePath)[1]) + ' , LBA = ' + str(eLba) + '\n')

	remainingSize = eSize
	while remainingSize > 0:
		cdImg.seek(24, 1)
		if remainingSize < dataSize:
			outFile.write(cdImg.read(remainingSize))
		else:
			outFile.write(cdImg.read(dataSize))
			cdImg.seek(2352-(24+dataSize), 1)
		remainingSize -= dataSize
	outFile.close()
	cdImg.close()

# Begin main program
parser = argparse.ArgumentParser(description='CD image extractor.')
parser.add_argument('filepath', type=str, help = 'Path to cd-image file.')
args = parser.parse_args()


print('CD_Extractor, Last modified: 4-05-2020')

fPath = args.filepath
f = open(fPath, 'rb')

f.seek(16*2352+24+8)
text = True
while text:
	rbyte = f.read(1)[0]
	if rbyte == 0:
		text = False

f.seek(7+8+32+38, 1)
sector = struct.unpack('<I', f.read(4))[0]

print ('Root LBA: ' + str(sector))
f.close()

dirName = '/'

extrList = readDirectory(sector, dirName)[0]
procList = readDirectory(sector, dirName)[1]

while len(procList) > 0:
	tmpBuf = readDirectory((procList[0])[2], (procList[0])[1] + '/')
	for fe in tmpBuf[0]:
		extrList.append(fe)
	for de in tmpBuf[1]:
		procList.append(de)
	procList.pop(0)

if not os.access('./cdroot', os.F_OK):
	os.mkdir('./cdroot', mode=0o777)
	for z in extrList:
		mdBuf = os.path.dirname(z[1])
		if os.path.split(mdBuf) == '' or os.path.split(mdBuf) == '/':
			if not os.access('./cdroot' + mdBuf, os.F_OK):
				os.mkdir('./cdroot' + mdBuf, mode=0o777)
		else:
			for ch in range(len(mdBuf)):
				if mdBuf[ch] == '/':
					if not os.access('./cdroot' + mdBuf[0:ch], os.F_OK):
						os.mkdir('./cdroot' + mdBuf[0:ch], mode=0o777)
			if not os.access('./cdroot' + mdBuf, os.F_OK):
				os.mkdir('./cdroot' + mdBuf, mode=0o777)
		print(os.path.basename(z[1]))
		extractFile(fPath, z[0], './cdroot' + z[1], z[2], z[3])
else:
	print('cdroot directory already exists! Quitting.')
