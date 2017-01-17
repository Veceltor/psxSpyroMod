##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.

import argparse
import struct

parser = argparse.ArgumentParser(description='BMP to 15bit-in-BMP converter')
parser.add_argument('filepath', type=str, help = 'Path to BMP image file.')
parser.add_argument('--colormode', type=int, default = 4, help = 'Convert image with N bits per pixel.')
parser.add_argument('--palette', type=str, default = 'font_palette.bmp', help = 'Palette for 8bpp/4bpp image.')
parser.add_argument('--output', type=str, default = 'image.bmp', help = 'Output file name.')

args = parser.parse_args()
fpath = args.filepath

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

def bgr4bppToRaw(imgData, palette):
	outputBytes = bytearray()	
	
	for n in range(int(len(imgData)/12)):
		binStr = ''
		pixelsCnt = 4
		for p in range(4):
			color = (imgData[n*12+p*3], imgData[n*12+p*3+1], imgData[n*12+p*3+2])
			color = compareToPalette(color, palette)
			binStr += str(bin(color)[2:len(bin(color))]).zfill(4)
		
		binStr = binStr[12:16] + binStr[8:12] + binStr[4:8] + binStr[0:4]
		binStr = binStr[1:11] + binStr[0] + binStr[11:16]

		b = int(binStr[0])*128+int(binStr[1])*64+int(binStr[2])*32+int(binStr[3])*16+int(binStr[4])*8
		g = int(binStr[5])*128+int(binStr[6])*64+int(binStr[7])*32+int(binStr[8])*16+int(binStr[9])*8+int(binStr[10])*4
		r = int(binStr[11])*128+int(binStr[12])*64+int(binStr[13])*32+int(binStr[14])*16+int(binStr[15])*8	

		outputBytes.append(b)
		outputBytes.append(g)
		outputBytes.append(r)
	
	return outputBytes

def compareToPalette(color, palette):
	retNum = 0
	for n in range(int(len(palette)/3)):
		if color == (palette[n*3], palette[n*3+1], palette[n*3+2]):
			retNum = n
			break
	return retNum

data16 = loadBmp(fpath)
imgSize = data16[1]
data16 = data16[0]
paletteData = loadBmp(args.palette)[0]
outImg = bgr4bppToRaw(data16, paletteData)
saveBmp(args.output, outImg, int(imgSize[0]/4), imgSize[1])

print('File converted.')
