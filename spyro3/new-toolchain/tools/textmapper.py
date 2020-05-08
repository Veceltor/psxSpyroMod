import argparse

parser = argparse.ArgumentParser(description='Palette generator. (8bpp)')
parser.add_argument('filepath', type=str, help = 'Path to target binary file')
parser.add_argument('cfgpath', type=str, help = 'Path to initial TXT map file.')
parser.add_argument('--output', type=str, default = 'new_map.txt', help = 'Output file name.')
args = parser.parse_args()

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

cfg = readConfigFile(args.cfgpath)
sf = open(args.filepath, "rb")
mapfile = open(args.output, "w", encoding = "utf-8")
mapfile.write("OFFSET SIZE\n")

for x in range(len(cfg[0])):
	sf.seek((cfg[0])[x])
	strend = 0
	strstart = (cfg[0])[x]
	strsize = 0
	txtTrig = True
	for i in range((cfg[1])[x]):
		valbuf = sf.read(1)
		if valbuf[0] == 0 and txtTrig:
			strend = (cfg[0])[x] + i
			if x == 0:
				strsize = (strend - strstart) + 1
			else:
				strsize = ((strend - strstart) // 4)*4 + 4
			mapfile.write(str(strstart) + " " + str(strsize) + "\n")
			print((strstart, strend, strsize))

			txtTrig = False
		elif not valbuf[0] == 0 and (not txtTrig):
			strstart = (cfg[0])[x] + i
			txtTrig = True

sf.close()
mapfile.close()
