#!/bin/bash

python3 ./tools/wad/wadPack.py ./sf --output ./cd-files/WAD.WAD

python3 ./tools/file-injector.py "cd" ./test-spyro3.bin ./cd-files/SCUS_944.67 "24"

python3 ./tools/file-injector.py "cd" ./test-spyro3.bin ./cd-files/WAD.WAD "500"

./tools/error_recalc/error_recalc.linux.x86_64 ./test-spyro3.bin

xdelta3 -e -s spyro3.bin test-spyro3.bin new-patch.xdelta

echo "Finished."
