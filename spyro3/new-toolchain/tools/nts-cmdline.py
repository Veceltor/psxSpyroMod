import argparse

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

def getNulltermStr(inputData):
	txt_list = list()
	lastByte = 123
	txtBuf = ""
	for i in range(len(inputData)):
		if (inputData[i] == 0) and (not lastByte == 0):
			txt_list.append(txtBuf)
			txtBuf = ""
		elif (not inputData[i] == 0):
			txtBuf += (inputData[i:i+1].decode("cp1251", "ignore") )
		lastByte = inputData[i]

	return txt_list

def packNulltermStr(strList, maxSize, cfgpath):
	binData = bytes.fromhex("")
	fullsize = 0
	for s in range(len(strList)):
		fullsize += len(strList[s])
		binData += piratecode(strList[s], cfgpath) + bytes.fromhex("00")*(4 - (len(piratecode(strList[s], cfgpath)) % 4))
	if fullsize > maxSize - 1:
		print("String block is too long!")
		print(strList)
	return binData
		

def readConfigFile(fpath):
	foffset = list()
	fsize = list()
	cf = open(fpath, "r", encoding="utf-8")
	dataStart = False
	for line in cf:
		if dataStart:
			fcount = 0
			sBuf = ""
			for s in line:
				if (s == " ") or (s == "\n"):
					if fcount == 0:
						foffset.append(int(sBuf))
					elif fcount == 1:
						fsize.append(int(sBuf))
					sBuf = ""
					fcount += 1
				else:
					sBuf += s
		dataStart = True
	cf.close()

	return (foffset, fsize)

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

parser = argparse.ArgumentParser(description='File injector.')
parser.add_argument('targetpath', type=str, help = 'Path to target file.')
parser.add_argument('mappath', type=str, help = 'Path to file map.')
parser.add_argument('filepath', type=str, help = 'Path to text file.')
parser.add_argument('mode', type=int, help = '0 = extract, 1 = paste.')
parser.add_argument('scpath', type=str, help = 'Path to sc.ini.')

args = parser.parse_args()

pasteText = False

sfpath = args.targetpath
mfpath = args.mappath

if args.mode == 1:
	pasteText = True

tfpath = args.filepath
cfgParams = readConfigFile(mfpath)

f = open(sfpath, "r+b")
strCountList = list()

if pasteText:
	for i in range(len(cfgParams[0])):
		f.seek((cfgParams[0])[i])
		strArray = getNulltermStr(f.read((cfgParams[1])[i]))
		strCountList.append(len(strArray))

	tList = loadTextFile(tfpath)

	pstrCount = 0
	for i in range(len(strCountList)):
		cList = list()
		for j in range(strCountList[i]):
			if i > 0:
				cList.append(tList[pstrCount])
			else:
				cList.append(tList[pstrCount])
			pstrCount +=1
		wBytes = packNulltermStr(cList, (cfgParams[1])[i], args.scpath)
		wBytes = wBytes + bytes.fromhex("00"*((cfgParams[1])[i] - len(wBytes)))

		f.seek((cfgParams[0])[i])
		nullBuf = bytes.fromhex("00"*(cfgParams[1])[i])
		f.write(nullBuf)
		f.seek((cfgParams[0])[i])
		f.write(wBytes)
else:
	outTxt = open('new-text.txt', 'w', encoding='utf-8')
	for i in range(len(cfgParams[0])):
		f.seek((cfgParams[0])[i])
		strArray = getNulltermStr(f.read((cfgParams[1])[i]))
		for ostr in strArray:
			outTxt.write(ostr + '\n\n')

f.close()
