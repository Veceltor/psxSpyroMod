##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.

import argparse
import struct

parser = argparse.ArgumentParser(description='RAW (bgr 15bpp) to BMP converter')
parser.add_argument('filepath', type=str, help = 'Path to RAW image file.')
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

def bgr555toRaw(imgData):
	outputBytes = bytearray()	
	
	cntList = list()
	for n in range(int(len(imgData)/2)):
		#gbbbbbgg gggrrrrr
		
		color = struct.unpack('<H', imgData[n*2:n*2+2])[0]		
		
		binStr = (str(bin(color))[2:len(str(bin(color)))]).zfill(16)
		b = int(binStr[1])*16 + int(binStr[2])*8 + int(binStr[3])*4 + int(binStr[4])*2 + int(binStr[5])
		g = int(binStr[6])*32 + int(binStr[7])*16 + int(binStr[8])*8 + int(binStr[9])*4 + int(binStr[10])*2 + int(binStr[0])
		r = int(binStr[11])*16 + int(binStr[12])*8 + int(binStr[13])*4 + int(binStr[14])*2 + int(binStr[15])
		
		outputBytes.append(b*8) 
		outputBytes.append(g*4)
		outputBytes.append(r*8)

	return outputBytes

args = parser.parse_args()
fpath = args.filepath

ifile = open(fpath, 'rb')
rawData = bgr555toRaw(ifile.read())
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
