#!/bin/bash

if [ ! -f test-spyro3.bin ]; then
cp spyro3.bin test-spyro3.bin
fi

mkdir -p cd-files
cp ./cdroot/SCUS_944.67 ./cd-files
mkdir -p ./files/img

#change font map
python3 ./tools/file-injector.py raw ./cd-files/SCUS_944.67 ./files/rus_font_table.bin "356296"
#paste new logo
python3 ./tools/graphics/bmpTo8bit.py ./files/pictures-src/logo-rus-alteya-scaled.bmp ./files/logo-palette.bmp --output ./files/img/logo_raw.bin
python3 ./tools/graphics/bmpTo15bit.py ./files/logo-palette.bmp --output ./files/img/logo_raw_palette.bin

python3 ./tools/file-injector.py 8bpp ./sf/sf_7.bin ./files/img/logo_raw.bin "0 4 188 72"
python3 ./tools/file-injector.py 15bpp ./sf/sf_7.bin ./files/img/logo_raw_palette.bin "0 2 256 1"

#convert font
python3 ./tools/graphics/bmpTo8bit.py ./files/pictures-src/rus_font.bmp ./files/font_palette.bmp --output ./files/img/inj_image.bin
python3 ./tools/graphics/bmpTo15bit.py ./files/font_palette.bmp --output ./files/img/inj_image15.bin

#paste font to all non-level subfiles
python3 ./tools/file-injector.py 4bpp ./sf/sf_7.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_7.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_7.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_10.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_10.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_10.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_13.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_13.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_13.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_16.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_16.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_16.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_19.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_19.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_19.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_22.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_22.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_22.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_25.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_25.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_25.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_28.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_28.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_28.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_31.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_31.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_31.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_34.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_34.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_34.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_37.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_37.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_37.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_40.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_40.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_40.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_46.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_46.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_46.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_52.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_52.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_52.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_55.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_55.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_55.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_58.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_58.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_58.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_61.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_61.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_61.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_64.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_64.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_64.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_67.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_67.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_67.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_184.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_184.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_184.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_185.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_185.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_185.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_186.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_186.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_186.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_187.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_187.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_187.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_188.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_188.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_188.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_189.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_189.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_189.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_190.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_190.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_190.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_191.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_191.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_191.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_192.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_192.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_192.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_193.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_193.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_193.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_194.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_194.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_194.bin ./files/img/inj_image15.bin "32 295 16 1"

python3 ./tools/file-injector.py 4bpp ./sf/sf_195.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_195.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_195.bin ./files/img/inj_image15.bin "32 295 16 1"

#paste text to non-level subfiles
python3 ./tools/nts-cmdline.py ./cd-files/SCUS_944.67 ./files/nts-cfg/exe-map.txt ./texts/exe-text.txt 1 ./files/sc.ini
python3 ./tools/nts-cmdline.py ./sf/sf_2.bin ./files/nts-cfg/sf2-map.txt ./texts/sf2-sf180-text.txt 1 ./files/sc.ini
python3 ./tools/nts-cmdline.py ./sf/sf_70.bin ./files/nts-cfg/sf70-map.txt ./texts/sf70-text.txt 1 ./files/sc.ini
python3 ./tools/nts-cmdline.py ./sf/sf_180.bin ./files/nts-cfg/sf180-map.txt ./texts/sf2-sf180-text.txt 1 ./files/sc.ini

echo "Finished."
