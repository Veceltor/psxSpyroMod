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

parser = argparse.ArgumentParser(description='Inserter of VRAM data.')
parser.add_argument('filepath', type=str, help = 'Path to level subfile.')
parser.add_argument('vram', type=str, help = 'Path to VRAM file.')

args = parser.parse_args()
fpath = args.filepath
sf1 = getSubfileInfo(fpath, 1)

wad = open(fpath, 'rb')
vram = open(args.vram, 'rb')

fbuf = wad.read()
wad.close()
wad = open(fpath, 'wb')

wad.write(fbuf)
wad.seek(sf1[0])
wad.write(vram.read(524288))
wad.close()
vram.close()

print('All done.')
