##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.

import argparse
import struct

parser = argparse.ArgumentParser(description='BMP to RAW (bgr 8/4bpp) converter')
parser.add_argument('filepath', type=str, help = 'Path to BMP image file.')
parser.add_argument('palette', type=str, help = 'Path to palette file (BMP 24-bit).')
parser.add_argument('--output', type=str, default = 'image.raw', help = 'Output file name.')

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

def rawTo8bit(imgData, paletteData):
	retData = bytearray()
	for x in range(int(len(imgData)/3)):
		color = (imgData[x*3], imgData[x*3+1], imgData[x*3+2])
		tmpPalConv = compareToPalette(color, paletteData)
		if not tmpPalConv == None:
			clrNum = tmpPalConv
		else:
			print("Палитра не подходит.")
			quit()
		retData.append(clrNum)
	return retData

def rawTo4bit(imgData, paletteData):
	retData = bytearray()
	clrNum = 0
	clrNum2 = 0
	for x in range(int(len(imgData)/3)):
		color = (imgData[x*3], imgData[x*3+1], imgData[x*3+2])
		if divmod(x, 2)[1] == 1:
			clrNum = compareToPalette(color, paletteData)
			clrNum = clrNum << 4
			retData.append(clrNum + clrNum2)
		else:
			tmpPalConv = compareToPalette(color, paletteData)
			if not tmpPalConv == None:
				clrNum2 = tmpPalConv
			else:
				print("Палитра не подходит.")
				quit()
	return retData

def compareToPalette(color, paletteData):
	for n in range(int(len(paletteData)/3)):
		cmpClr = (paletteData[n*3], paletteData[n*3+1], paletteData[n*3+2])
		if color == cmpClr:
			return n
			break

def makeBinStr(intValue, bytesCount):
	retStr = (str(bin(intValue))[2:len(str(bin(intValue)))]).zfill(bytesCount*8)
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

rawData = loadBmp(fpath)[0]
if bitMode == 8:
	rawData = rawTo8bit(rawData, pData)
elif bitMode == 4:
	rawData = rawTo4bit(rawData, pData)
ofile = open(args.output, 'wb')
ofile.write(rawData)
ofile.close()

print('File converted.')
