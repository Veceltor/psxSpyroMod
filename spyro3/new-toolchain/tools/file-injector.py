import os
import argparse

def writeSector(filepath, lba, wdata):
	f = open(filepath, 'r+b')
	f.seek(lba*2352+24)
	f.write(wdata)
	f.close()

def cdInject(flba, tfpath, ifpath):
	fsize = os.path.getsize(ifpath)
	ifile = open(ifpath, 'rb')
	ws = 0

	while fsize > ws*2048:
		writeSector(tfpath, flba+ws, ifile.read(2048))
		ws += 1
	ifile.close()


def img8Inject(mode_4bpp, posx, posy, imgwidth, imgheight, tfpath, ifpath):
	f = open(tfpath, 'r+b')
	ifile = open(ifpath, 'rb')
	width = 1024
	height = 512

	if mode_4bpp:
		imgwidth = int(imgwidth/2)

	for y in range(imgheight):
		f.seek(((posy+y)*width) + posx)
		f.write(ifile.read(imgwidth))

	f.close()
	ifile.close()

def img15Inject(posx, posy, imgwidth, imgheight, tfpath, ifpath):
	f = open(tfpath, 'r+b')

	ifile = open(ifpath, 'rb')
	width = 512
	height = 512

	for y in range(imgheight):
		f.seek(((posy+y)*width)*2 + posx*2)
		f.write(ifile.read(imgwidth*2))

	f.close()
	ifile.close()

parser = argparse.ArgumentParser(description='File injector.')
parser.add_argument('mode', type=str, help = 'Inject mode.')
parser.add_argument('targetpath', type=str, help = 'Path to target file.')
parser.add_argument('filepath', type=str, help = 'Path to injected file.')
parser.add_argument('options', type=str, help = 'Additional parameters.')

args = parser.parse_args()

#print('File_Injector, last modified - 4-05-2020')
mode = args.mode

optbuf = ""
optlist = list()
for symbol in args.options:
	if symbol == " ":
		optlist.append(optbuf)
		optbuf = ""
	else:
		optbuf += symbol

optlist.append(optbuf)
optbuf = ""

if mode == "cd":
	cdInject(int(optlist[0]), args.targetpath, args.filepath)
elif mode == "4bpp":
	img8Inject(True, int(optlist[0]), int(optlist[1]), int(optlist[2]), int(optlist[3]), args.targetpath, args.filepath)
elif mode == "8bpp":
	img8Inject(False, int(optlist[0]), int(optlist[1]), int(optlist[2]), int(optlist[3]), args.targetpath, args.filepath)
elif mode == "15bpp":
	img15Inject(int(optlist[0]), int(optlist[1]), int(optlist[2]), int(optlist[3]), args.targetpath, args.filepath)
elif mode == "raw":
	injoffset = int(optlist[0])
	tfile = open(args.targetpath, "r+b")
	injfile = open(args.filepath, "rb")
	tfile.seek(injoffset)
	tfile.write(injfile.read())
	tfile.close()
	injfile.close()
else:
	print("Invalid mode! Nothing changed.")

print("Completed.")
