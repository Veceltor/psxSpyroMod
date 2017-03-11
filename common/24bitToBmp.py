##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.

import argparse
import struct

parser = argparse.ArgumentParser(description='RAW (bgr 24bpp) to BMP converter')
parser.add_argument('filepath', type=str, help = 'Path to RAW image file.')
parser.add_argument('size', type=str, help = 'Size of image. (WxH)')
parser.add_argument('--output', type=str, default = 'image.bmp', help = 'Output file name.')

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

args = parser.parse_args()
fpath = args.filepath

ifile = open(fpath, 'rb')
rawData = ifile.read()
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
