##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.

import argparse
import struct

parser = argparse.ArgumentParser(description='RAW (bgr 8bpp/4bpp) to BMP converter')
parser.add_argument('filepath', type=str, help = 'Path to RAW image file.')
parser.add_argument('palette', type=str, help = 'Path to palette file (BMP 24-bit).')
parser.add_argument('size', type=str, help = 'Size of image. (WxH)')
parser.add_argument('--output', type=str, default = 'image.bmp', help = 'Output file name.')

def loadBmp(filepath):
	f = open(filepath, 'rb')
	f.seek(10)
	datOffset = struct.unpack('<I', f.read(4))[0]
	f.seek(18)
	imgWidth = struct.unpack('<I', f.read(4))[0]
	imgHeight = struct.unpack('<I', f.read(4))[0]
	imgSize = (imgWidth, imgHeight)
	f.seek(datOffset)
	bmpData = f.read(imgWidth*imgHeight*3)
	imgData = bytearray()
	for h in range(imgHeight):
		for w in range(3*imgWidth):
			imgData.append(bmpData[(imgHeight-h-1)*(3*imgWidth)+w])
	f.close()
	return (imgData, imgSize)

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

def bgr8toRaw(imgData, paletteData):
	outputBytes = bytearray()	
	
	cntList = list()
	for n in range(len(imgData)):
		clrNum = imgData[n]		
		color = (paletteData[clrNum*3], paletteData[clrNum*3+1], paletteData[clrNum*3+2])
		
		outputBytes.append(color[0]) 
		outputBytes.append(color[1])
		outputBytes.append(color[2])

	return outputBytes

def bgr4toRaw(imgData, paletteData):
	outputBytes = bytearray()	
	
	cntList = list()
	for n in range(len(imgData)):
		clrNum2 = imgData[n] >> 4
		clrNum1 = divmod(imgData[n] << 4, 256)[1]
		clrNum1 = clrNum1 >> 4
		color1 = (paletteData[clrNum1*3], paletteData[clrNum1*3+1], paletteData[clrNum1*3+2])
		color2 = (paletteData[clrNum2*3], paletteData[clrNum2*3+1], paletteData[clrNum2*3+2])
		
		outputBytes.append(color1[0]) 
		outputBytes.append(color1[1])
		outputBytes.append(color1[2])
		outputBytes.append(color2[0]) 
		outputBytes.append(color2[1])
		outputBytes.append(color2[2])

	return outputBytes

def makeBinStr(intValue, bytesCount):
	retStr = (str(bin(intValue))[2:len(str(bin(intValue)))]).zfill(int(bytesCount)*8)
	return retStr

def makeByteFromStr(inStr):
	retVal = -1
	if not len(inStr) == 8:
		print('Wrong input length')
	else:
		retVal = int(inStr[0])*128 + int(inStr[1])*64 + int(inStr[2])*32 + int(inStr[3])*16 + int(inStr[4])*8 + int(inStr[5])*4 + int(inStr[6])*2 + int(inStr[7])
	return retVal

args = parser.parse_args()
fpath = args.filepath

pData = loadBmp(args.palette)
pSize = pData[1]
pData = pData[0]

bitMode = 8
if pSize == (256, 1):
	bitMode = 8
elif pSize == (16, 1):
	bitMode = 4
else:
	print('Wrong palette file!')
	quit()

ifile = open(fpath, 'rb')
if bitMode == 8:
	rawData = bgr8toRaw(ifile.read(), pData)
elif bitMode == 4:
	rawData = bgr4toRaw(ifile.read(), pData)
ifile.close()
hTrig = False
width = ''
height = ''
for s in args.size:
	if s == 'x':
		hTrig = True
	else:
		if hTrig:
			height += s
		else:
			width += s
width = int(width)
height = int(height)
saveBmp(args.output, rawData, width, height)

print('File converted.')
