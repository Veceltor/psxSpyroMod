#!/bin/bash

python3 ./tools/cd-unpack.py spyro3.bin
mkdir -p sf
cd sf
python3 ../tools/wad/wadExtract.py ../cdroot/WAD.WAD 0

echo "Finished."
