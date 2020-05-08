import argparse

parser = argparse.ArgumentParser(description='Copy regions of VRAM / RAW images')
parser.add_argument('filepath', type=str, help = 'Path to RAW image file.')
parser.add_argument('x', type=int, help = 'X coordinate.')
parser.add_argument('y', type=int, help = 'Y coordinate.')
parser.add_argument('width', type=int, help = 'Width.')
parser.add_argument('height', type=int, help = 'Height.')
parser.add_argument('--output', type=str, default = 'raw_image.bin', help = 'Output file name.')
args = parser.parse_args()

print('VRAM_Cutter, last modified - 7-05-2020')
#8-bit mode

fpath = args.filepath

f = open(fpath, 'rb')
ofile = open(args.output, 'wb')
width = 1024 #fixed for now

posx = args.x
posy = args.y 

imgwidth = args.width
imgheight = args.height

print((posy*width) + posx)

for y in range(imgheight):
	f.seek(((posy+y)*width) + posx)
	ofile.write(f.read(imgwidth))

f.close()
ofile.close()
