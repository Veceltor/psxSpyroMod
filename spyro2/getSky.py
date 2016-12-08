##Level sky model extractor.


##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.

import argparse
import struct

def getSubfileInfo(filepath, subfile):
	info_list = list()
	ifile = open(filepath, 'rb')
	ifile.seek((subfile-1)*8)
	info_list.append(struct.unpack('<I', ifile.read(4))[0])
	info_list.append(struct.unpack('<I', ifile.read(4))[0])
	ifile.close()

	return info_list

def jumper(filepath, start, jumpcount):
	jumpbuf = 0
	ifile = open(filepath, 'rb')
	for n in range(jumpcount):
		ifile.seek(start+jumpbuf)
		bytes0 = ifile.read(4)
		jumpbuf += struct.unpack('<I', bytes0)[0]

	return start+jumpbuf

def getRawSkyData(filepath):
	sf = getSubfileInfo(filepath, 2)
	of2 = jumper(filepath, sf[0], 6)
	sky_addr = 0
	offset = jumper(filepath, of2+12, 1)
	sky_addr = offset+4
	print(sky_addr)
	ifile = open(filepath, 'rb')
	ifile.seek(sky_addr)
	sky_size = struct.unpack('<I', ifile.read(4))[0]+4
	ifile.seek(sky_addr)
	sky_data = ifile.read(sky_size)
	ifile.close()
	
	return sky_data


parser = argparse.ArgumentParser(description='Extractor of sky model raw data.')
parser.add_argument('filepath', type=str, help = 'Path to level subfile.')
parser.add_argument('--output', type=str, default = 'sky.sky', help = 'Output file name.')

args = parser.parse_args()
fpath = args.filepath
model_raw = getRawSkyData(fpath)
ofile = open(args.output, 'wb')
ofile.write(model_raw)
ofile.close()

print('All done.')
