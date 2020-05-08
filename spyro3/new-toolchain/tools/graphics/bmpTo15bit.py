##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.

import argparse
import struct

parser = argparse.ArgumentParser(description='BMP to RAW (bgr 15bpp) converter')
parser.add_argument('filepath', type=str, help = 'Path to BMP image file.')
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

def rawTo555(imgData):
	retData = bytearray()
	for x in range(int(len(imgData)/3)):
		b = imgData[x*3]
		g = imgData[x*3+1]
		r = imgData[x*3+2]
		binStr = '0' + makeBinStr(b,1)[0:5] + makeBinStr(g,1)[0:5] + makeBinStr(r,1)[0:5]
		retData.append(makeByteFromStr(binStr[8:16]))
		retData.append(makeByteFromStr(binStr[0:8]))
	return retData

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

rawData = loadBmp(fpath)[0]
rawData = rawTo555(rawData)
ofile = open(args.output, 'wb')
ofile.write(rawData)
ofile.close()

print('File converted.')
