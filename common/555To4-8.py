##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.

import argparse
import struct

parser = argparse.ArgumentParser(description='15bit-in-BMP to BMP (4/8bit) converter')
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

def rawTobgr4bpp(imgData, palette):
	#bbbbbggg gggrrrrr --> 12-13-14-15 7-8-9-11 3-4-5-6 10-0-1-2
	outputBytes = bytearray()	
	
	for n in range(int(len(imgData)/3)):
		b = int(imgData[n*3]/8)
		g = int(imgData[n*3+1]/4)
		r = int(imgData[n*3+2]/8)
		binStr = ((str(bin(g))[2:len(str(bin(g)))]).zfill(6))[5]
		binStr += (str(bin(b))[2:len(str(bin(b)))]).zfill(5)
		binStr += ((str(bin(g))[2:len(str(bin(g)))]).zfill(6))[0:5]
		binStr += (str(bin(r))[2:len(str(bin(r)))]).zfill(5)
		pix1 = binStr[0:4]
		pix2 = binStr[4:8]
		pix3 = binStr[8:12]
		pix4 = binStr[12:16]
		binStr = pix4 + pix3 + pix2 + pix1 

		for p in range(4):
			clrNum = int(binStr[p*4])*8+int(binStr[p*4+1])*4+int(binStr[p*4+2])*2+int(binStr[p*4+3])*1
			color = pickFromPalette(clrNum, palette)
			outputBytes.append(color[0])
			outputBytes.append(color[1])
			outputBytes.append(color[2])
	
	return outputBytes

def pickFromPalette(color, palette):
	retColor = (palette[color*3], palette[color*3+1], palette[color*3+2])
	return retColor

data16 = loadBmp(fpath)
imgSize = data16[1]
data16 = data16[0]
paletteData = loadBmp(args.palette)[0]
outImg = rawTobgr4bpp(data16, paletteData)
saveBmp(args.output, outImg, imgSize[0]*4, imgSize[1])

print('File converted.')
