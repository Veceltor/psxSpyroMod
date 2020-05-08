#!/bin/bash

#convert images
python3 ./tools/graphics/bmpTo8bit.py ./files/pictures-src/atlas_rus_alteya.bmp ./files/atlas-logo-rus-palette.bmp --output ./files/img/atlas-logo.bin
python3 ./tools/graphics/bmpTo15bit.py ./files/atlas-logo-rus-palette.bmp --output ./files/img/atlas-logo-palette.bin

#paste sf_179 data
python3 ./tools/file-injector.py 8bpp ./sf/sf_179.bin ./files/img/atlas-logo.bin "104 53 132 104"
python3 ./tools/file-injector.py 15bpp ./sf/sf_179.bin ./files/img/atlas-logo-palette.bin "52 30 256 1"
