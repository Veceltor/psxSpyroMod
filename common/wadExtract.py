##.WAD archive unpacker


##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.


import argparse
import os
import struct

parser = argparse.ArgumentParser(description='Unpacker for WAD.WAD archive.')
parser.add_argument('filepath', type=str, help = 'Path to WAD.WAD.')
parser.add_argument('subfile', type=int, help = 'Subfile number. 0 - extract all subfiles.')
args = parser.parse_args()

def extractSubfile(sfNum):
	ofile = open('sf_' + str(sfNum) + '.bin', 'wb')
	sfAddr = (subfiles[(sfNum-1)*2])
	sfSize = (subfiles[(sfNum-1)*2+1])
	ifile.seek(sfAddr)
	ofile.write(ifile.read(sfSize))
	ofile.close()


ifile = open(args.filepath, 'rb')
headerFmt = '<' + 'I'*512
subfiles = struct.unpack(headerFmt, ifile.read(struct.calcsize(headerFmt)))
sfCount = 0

for x in range(int(len(subfiles)/2)):
	if not subfiles[x*2+1] == 0:
		sfCount = x+1

if args.subfile > 0:
	extractSubfile(args.subfile)
else:
	for n in range(sfCount):
		extractSubfile(n+1)

ifile.close()

print('Extraction completed.')
