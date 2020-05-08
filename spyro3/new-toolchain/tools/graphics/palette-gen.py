import argparse
import struct

parser = argparse.ArgumentParser(description='Palette generator. (8bpp)')
parser.add_argument('filepath', type=str, help = 'Path to palette TXT file.')
parser.add_argument('--output', type=str, default = 'new-palette.bmp', help = 'Output file name.')
args = parser.parse_args()

def saveBmp(filepath, imgData, imgWidth, imgHeight):
	f = open(filepath, 'wb')
	fileSize = 58 + len(imgData)
	f.write('BM'.encode('cp1251', errors='ignore'))
	f.write(struct.pack('<I', fileSize))
	f.write(bytes.fromhex('00000000'))
	f.write(struct.pack('<I', 58)) ##image data offset
	f.write(struct.pack('<I', 40)) ##size of DIB header
	f.write(struct.pack('<I', imgWidth))
	f.write(struct.pack('<I', imgHeight))
	f.write(struct.pack('<H', 1))
	f.write(struct.pack('<H', 24)) #bpp
	f.write(struct.pack('<I', 0))
	f.write(struct.pack('<I', 0))
	f.write(struct.pack('<I', 0))
	f.write(struct.pack('<I', 0))
	f.write(struct.pack('<I', 0))
	f.write(struct.pack('<I', 0))
	
	f.seek(58)
	for h in range(imgHeight):
		for w in range(imgWidth):
			f.write(imgData[((imgHeight-h-1)*imgWidth+w)*3:((imgHeight-h-1)*imgWidth+w+1)*3])
	f.close()


#load palette from text file
txtfile = open(args.filepath, "r", encoding="utf-8")

countLine = True
newImgData = bytearray()
for line in txtfile.readlines():
	if countLine:
		print("skipping bit-mode detection...")
		countLine = False
	else:
		tmpPixels = list()
		sBuf = ""
		for sym in line:
			if sym == "," or sym == "\n":
				tmpPixels.append(int(sBuf))
				sBuf = ""
			else:
				sBuf += sym
		newImgData.append(tmpPixels[2])
		newImgData.append(tmpPixels[1])
		newImgData.append(tmpPixels[0]) #B-G-R --> R-G-B

saveBmp(args.output, newImgData, 256, 1)
