#!/bin/bash

#paste font
python3 ./tools/file-injector.py 4bpp ./sf/sf_98.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_98.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_98.bin ./files/img/inj_image15.bin "32 295 16 1"
#paste misc text
python3 ./tools/nts-cmdline.py ./sf/sf_98.bin ./files/nts-cfg/sf98-full-map.txt ./texts/98-misc-text.txt 1 ./files/sc.ini
#paste npc text
python3 ./tools/lvt-pastetext.py ./sf/sf_98.bin ./texts/98-text.txt 4 ./files/sc.ini

#paste font
python3 ./tools/file-injector.py 4bpp ./sf/sf_100.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_100.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_100.bin ./files/img/inj_image15.bin "32 295 16 1"
#paste misc text
python3 ./tools/nts-cmdline.py ./sf/sf_100.bin ./files/nts-cfg/sf100-full-map.txt ./texts/100-misc-text.txt 1 ./files/sc.ini
#paste npc text
python3 ./tools/lvt-pastetext.py ./sf/sf_100.bin ./texts/100-text.txt 4 ./files/sc.ini
python3 ./tools/lvt-pastetext.py ./sf/sf_100.bin ./texts/100-sublevel1-text.txt 6 ./files/sc.ini
python3 ./tools/lvt-pastetext.py ./sf/sf_100.bin ./texts/100-sublevel2-text.txt 8 ./files/sc.ini

#paste font
python3 ./tools/file-injector.py 4bpp ./sf/sf_102.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_102.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_102.bin ./files/img/inj_image15.bin "32 295 16 1"
#paste misc text
python3 ./tools/nts-cmdline.py ./sf/sf_102.bin ./files/nts-cfg/sf102-full-map.txt ./texts/102-misc-text.txt 1 ./files/sc.ini
#paste npc text
python3 ./tools/lvt-pastetext.py ./sf/sf_102.bin ./texts/102-text.txt 4 ./files/sc.ini
python3 ./tools/lvt-pastetext.py ./sf/sf_102.bin ./texts/102-sublevel1-text.txt 6 ./files/sc.ini
python3 ./tools/lvt-pastetext.py ./sf/sf_102.bin ./texts/102-sublevel2-text.txt 8 ./files/sc.ini

#paste font
python3 ./tools/file-injector.py 4bpp ./sf/sf_104.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_104.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_104.bin ./files/img/inj_image15.bin "32 295 16 1"
#paste misc text
python3 ./tools/nts-cmdline.py ./sf/sf_104.bin ./files/nts-cfg/sf104-full-map.txt ./texts/104-misc-text.txt 1 ./files/sc.ini
#paste npc text
python3 ./tools/lvt-pastetext.py ./sf/sf_104.bin ./texts/104-text.txt 4 ./files/sc.ini
python3 ./tools/lvt-pastetext.py ./sf/sf_104.bin ./texts/104-sublevel1-text.txt 6 ./files/sc.ini
python3 ./tools/lvt-pastetext.py ./sf/sf_104.bin ./texts/104-sublevel2-text.txt 8 ./files/sc.ini

#paste font
python3 ./tools/file-injector.py 4bpp ./sf/sf_106.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_106.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_106.bin ./files/img/inj_image15.bin "32 295 16 1"
#paste misc text
python3 ./tools/nts-cmdline.py ./sf/sf_106.bin ./files/nts-cfg/sf106-full-map.txt ./texts/106-misc-text.txt 1 ./files/sc.ini
#paste npc text
python3 ./tools/lvt-pastetext.py ./sf/sf_106.bin ./texts/106-text.txt 4 ./files/sc.ini
python3 ./tools/lvt-pastetext.py ./sf/sf_106.bin ./texts/106-sublevel1-text.txt 6 ./files/sc.ini
python3 ./tools/lvt-pastetext.py ./sf/sf_106.bin ./texts/106-sublevel2-text.txt 8 ./files/sc.ini
python3 ./tools/lvt-pastetext.py ./sf/sf_106.bin ./texts/106-sublevel3-text.txt 10 ./files/sc.ini

#paste font
python3 ./tools/file-injector.py 4bpp ./sf/sf_108.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_108.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_108.bin ./files/img/inj_image15.bin "32 295 16 1"
#paste misc text
python3 ./tools/nts-cmdline.py ./sf/sf_108.bin ./files/nts-cfg/sf108-full-map.txt ./texts/108-misc-text.txt 1 ./files/sc.ini
#paste npc text
python3 ./tools/lvt-pastetext.py ./sf/sf_108.bin ./texts/108-text.txt 4 ./files/sc.ini

#paste font
python3 ./tools/file-injector.py 4bpp ./sf/sf_110.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_110.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_110.bin ./files/img/inj_image15.bin "32 295 16 1"
#paste misc text
python3 ./tools/nts-cmdline.py ./sf/sf_110.bin ./files/nts-cfg/sf110-full-map.txt ./texts/110-misc-text.txt 1 ./files/sc.ini
#paste npc text
python3 ./tools/lvt-pastetext.py ./sf/sf_110.bin ./texts/110-text.txt 4 ./files/sc.ini

#paste font
python3 ./tools/file-injector.py 4bpp ./sf/sf_112.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_112.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_112.bin ./files/img/inj_image15.bin "32 295 16 1"
#paste misc text
python3 ./tools/nts-cmdline.py ./sf/sf_112.bin ./files/nts-cfg/sf112-full-map.txt ./texts/112-misc-text.txt 1 ./files/sc.ini
#paste npc text
python3 ./tools/lvt-pastetext.py ./sf/sf_112.bin ./texts/112-text.txt 4 ./files/sc.ini

#paste font
python3 ./tools/file-injector.py 4bpp ./sf/sf_114.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_114.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_114.bin ./files/img/inj_image15.bin "32 295 16 1"
#paste misc text
python3 ./tools/nts-cmdline.py ./sf/sf_114.bin ./files/nts-cfg/sf114-full-map.txt ./texts/114-misc-text.txt 1 ./files/sc.ini
#paste npc text
python3 ./tools/lvt-pastetext.py ./sf/sf_114.bin ./texts/114-text.txt 4 ./files/sc.ini

#---WORLD 2---

#paste font
python3 ./tools/file-injector.py 4bpp ./sf/sf_116.bin ./files/img/inj_image.bin "0 258 252 46"
python3 ./tools/file-injector.py 15bpp ./sf/sf_116.bin ./files/img/inj_image15.bin "32 294 16 1"
python3 ./tools/file-injector.py 15bpp ./sf/sf_116.bin ./files/img/inj_image15.bin "32 295 16 1"
#paste misc text
python3 ./tools/nts-cmdline.py ./sf/sf_116.bin ./files/nts-cfg/sf116-full-map.txt ./texts/116-misc-text.txt 1 ./files/sc.ini
#paste npc text
python3 ./tools/lvt-pastetext.py ./sf/sf_116.bin ./texts/116-text.txt 4 ./files/sc.ini

echo "Finished."
