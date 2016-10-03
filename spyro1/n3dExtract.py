#Extract 3d models with normals

import argparse
import struct
import os

def n3d2obj(mdl, num):
    ofile = open(str(num) + '.obj', 'w')
    bytes0 = mdl[0:16]
    vcount = bytes0[0]
    pcount = bytes0[1]
    voffset = bytes0[4] + bytes0[5]*256 + bytes0[6]*65536 + bytes0[7]*16777216
    poffset = bytes0[12] + bytes0[13]*256 + bytes0[14]*65536 + bytes0[15]*16777216

    bytes0 = mdl[voffset:voffset+vcount*3]
    vlist = list()
    for x in range(len(bytes0)):
        if divmod(x, 3)[1] == 0:
            if bytes0[x] < 128:
                buffer0 = bytes0[x]
            else:
                buffer0 = bytes0[x]-256
        if divmod(x, 3)[1] == 1:
            if bytes0[x] < 128:
                vlist.append(bytes0[x])
            else:
                vlist.append(bytes0[x]-256)
        if divmod(x, 3)[1] == 2:
            if bytes0[x] < 128:
                vlist.append(bytes0[x])
            else:
                vlist.append(bytes0[x]-256)
            vlist.append(buffer0)

    bytes0 = mdl[poffset:poffset+(pcount*8)]
    plist = list()
    nlist = list()
    tr = False
    for x in range(len(bytes0)):
        if divmod(x, 8)[1] == 0:
            buffer0 = bin(bytes0[x])[2:len(bin(bytes0[x]))].zfill(8) + bin(bytes0[x+1])[2:len(bin(bytes0[x+1]))].zfill(8) + bin(bytes0[x+2])[2:len(bin(bytes0[x+2]))].zfill(8) + bin(bytes0[x+3])[2:len(bin(bytes0[x+3]))].zfill(8)
            plist.append(int(buffer0[15])*64 + int(buffer0[0])*32 + int(buffer0[1])*16 + int(buffer0[2])*8 + int(buffer0[3])*4 + int(buffer0[4])*2 + int(buffer0[5]))
            plist.append(int(buffer0[8])*64 + int(buffer0[9])*32 + int(buffer0[10])*16 + int(buffer0[11])*8 + int(buffer0[12])*4 + int(buffer0[13])*2 + int(buffer0[14]))
            plist.append(int(buffer0[17])*64 + int(buffer0[18])*32 + int(buffer0[19])*16 + int(buffer0[20])*8 + int(buffer0[21])*4 + int(buffer0[22])*2 + int(buffer0[23]))
            plist.append(int(buffer0[26])*64 + int(buffer0[27])*32 + int(buffer0[28])*16 + int(buffer0[29])*8 + int(buffer0[30])*4 + int(buffer0[31])*2 + int(buffer0[16]))
        if divmod(x, 8)[1] >= 5:
            if bytes0[x] < 128:
                nlist.append(bytes0[x])
            else:
                nlist.append(bytes0[x]-256)
    for x in range(len(plist)): 
        if plist[x] > vcount-1:
            plist.pop(x)
            plist.insert(x, vcount-1)

    ncounter = 1
    for x in range(vcount):
        ofile.write('v ' + str(round(vlist[x*3]*0.1, 6)) + ' ' + str(round(vlist[x*3+1]*0.1, 6)) + ' ' + str(round(vlist[x*3+2]*0.1, 6)) + '\n')
    for x in range(pcount):
        ofile.write('vn ' + str(round(nlist[x*3]/127, 6)) + ' ' + str(round(nlist[x*3+1]/127, 6)) + ' ' + str(round(nlist[x*3+2]/127, 6)) + '\n')
    for x in range(pcount):
        if plist[x*4+1] == plist[x*4]:
            ofile.write('f ' + str(plist[x*4+1]+1) + '//' + str(ncounter) + ' ' + str(plist[x*4+2]+1) + '//' + str(ncounter) + ' ' + str(plist[x*4+3]+1) + '//' + str(ncounter) + '\n')
        else:
            ofile.write('f ' + str(plist[x*4]+1) + '//' + str(ncounter) + ' ' + str(plist[x*4+2]+1) + '//' + str(ncounter) + ' ' + str(plist[x*4+3]+1) + '//' + str(ncounter) + ' ' + str(plist[x*4+1]+1) + '//' + str(ncounter)  + '\n')
        ncounter = ncounter+1

    ofile.close()

parser = argparse.ArgumentParser(description='Extract 3d models with normal data.')
parser.add_argument('filepath', type=str, help = 'Path to subfile with models.')

args = parser.parse_args()

filepath = args.filepath

f = open (filepath, 'rb')

counter = 0
prev_offset = 0
while True:
	f.seek(counter*8+16)
	sfnum = struct.unpack('<I', f.read(4))[0]
	sfoffset = struct.unpack('<I', f.read(4))[0]
	
	if sfoffset > 0:
		f.seek(prev_offset)
		data = f.read(sfoffset - prev_offset)
		if counter > 0:
			n3d2obj(data, counter)
		counter+=1
		prev_offset = sfoffset
	else:
		f.seek(prev_offset)
		data = f.read()
		n3d2obj(data, counter)
		break