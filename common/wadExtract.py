##.WAD archive unpacker


##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.


import argparse
import struct
import os

parser = argparse.ArgumentParser(description='Unpacker for WAD.WAD archive.')
parser.add_argument('filepath', type=str, help = 'Path to WAD.WAD.')
parser.add_argument('subfile', type=int, help = 'Subfile number. 0 - extract all subfiles.')
##parser.add_argument('--part', type=int, default=0, help = 'Read header of subfile and extract only n-th part. 0 (default) - extract whole file instead.')

args = parser.parse_args()

def get_subfiles_count():
	path = args.filepath

	f = open(path, 'rb')
	header = f.read(2048)

	addr = 0
	sfsize = 0
	lastsf = 0
	for sf in range(256):
		addr = struct.unpack('<I', header[0+sf*8:4+sf*8])[0]
		sfsize = struct.unpack('<I', header[4+sf*8:8+sf*8])[0]
		if sfsize > 0:
			lastsf = sf+1

	return lastsf

def get_subfile(sf_num):
	sf = sf_num
	##ssf = args.part
	ssf = 0
	path = args.filepath

	f = open(path, 'rb')

	header = f.read(2048)
	addr = struct.unpack('<I', header[0+sf*8:4+sf*8])[0]
	sfsize = struct.unpack('<I', header[4+sf*8:8+sf*8])[0]

	f.seek(addr)
	subfile = f.read(sfsize)

	if ssf == 0:
		return subfile
	
	elif ssf > 0:
		return subfile
	
	else:
		print('Wrong part number: ' + str(ssf))

if args.subfile > 0:
	ofile = open('sf_' + str(args.subfile) + '.bin', 'wb')
	ofile.write(get_subfile(args.subfile-1))
	ofile.close()
else:
	for n in range(get_subfiles_count()):
		ofile = open('sf_' + str(n+1) + '.bin', 'wb')
		ofile.write(get_subfile(n))
		ofile.close()

print('Extraction completed.')
