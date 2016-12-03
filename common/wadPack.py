##.WAD archive packer


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
parser.add_argument('filepath', type=str, help = 'Path to folder with subfiles. Files must be named "sf_*number*.bin", where *number* is number of subfile, starting from 1.')
parser.add_argument('--output', type=str, default = 'new_WAD.WAD', help = 'Output file name.')

args = parser.parse_args()

if (args.filepath[0] == '"') or (args.filepath[0] == "'"):
	fpath = args.filepath[1:len(args.filepath)-1]
else:
	fpath = args.filepath

workfolder = os.getcwd()
filelist = os.listdir(fpath)
wad = open(args.output, 'wb')
offset = 2048
counter0 = 0
for x in range(len(filelist)):
    subfile = open(fpath + '/' + 'sf_' + str(x+1) + '.bin', 'rb')

    bytes0 = subfile.read()
    sfsize = len(bytes0)
    wad.seek(counter0 * 8)
    wad.write(offset.to_bytes(4, byteorder='little'))
    
    wad.seek(counter0*8 + 4)
    wad.write(sfsize.to_bytes(4, byteorder='little'))
    counter0 = counter0 + 1
    wad.seek(offset)
    wad.write(bytes0)
    offset = offset + sfsize
    subfile.close()
    
wad.close()
print('WAD file created.')

