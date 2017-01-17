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

args = parser.parse_args()
fpath = args.filepath

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
			
def rawTobgr555(imgData):
	outputBytes = bytearray()	
		
	for n in range(int(len(imgData)/3)):
		#gbbbbbgg gggrrrrr
		b = int(imgData[n*3]/8)
		g = int(imgData[n*3+1]/4)
		r = int(imgData[n*3+2]/8)
		bitStr = str(bin(b)[2:len(bin(b))]).zfill(5) + str(bin(g)[2:len(bin(g))]).zfill(6) + str(bin(r)[2:len(bin(r))]).zfill(5)
		color = int(bitStr[10])*32768 + int(bitStr[0])*16384 + int(bitStr[1])*8192 + int(bitStr[2])*4096 + int(bitStr[3])*2048 + int(bitStr[4])*1024 + int(bitStr[5])*512 + int(bitStr[6])*256 + int(bitStr[7])*128 + int(bitStr[8])*64 + int(bitStr[9])*32 + int(bitStr[11])*16 + int(bitStr[12])*8 + int(bitStr[13])*4 + int(bitStr[14])*2 + int(bitStr[15])
		try:
			outputBytes.append(struct.pack('<H', color)[0])
			outputBytes.append(struct.pack('<H', color)[1])
		except struct.error:
			print(color)
			quit()

	return outputBytes

def compareToPalette(color, palette):
	retNum = 0
	for n in range(int(len(palette)/3)):
		if color == (palette[n*3], palette[n*3+1], palette[n*3+2]):
			retNum = n
			break
	return retNum

ofile = open(args.output, 'wb')
colorMode = args.colormode

if args.colormode <= 8:
	ltmp = loadBmp(args.palette)

	if ((ltmp[1])[1] == 1):
		if (ltmp[1])[0] == 16:
			colorMode = 4
		elif (ltmp[1])[0] == 256:
			colorMode = 8
		else:
			print('Wrong palette file.')
			quit()
	else:
		print('Wrong palette file.')
		quit()

outputBytes = rawTobgr555(loadBmp(fpath)[0])
ofile.write(outputBytes)
ofile.close()

print('All done.')
