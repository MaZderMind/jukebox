jukebox.dtbo: jukebox.dts
	dtc -@ -Hepapr -I dts -O dtb -o jukebox.dtbo jukebox.dts

/boot/overlays/jukebox.dtbo: jukebox.dtbo
	sudo cp jukebox.dtbo /boot/overlays/

install: /boot/overlays/jukebox.dtbo
	@echo "do not forget to add 'dtoverlay=jukebox' and 'dtoverlay=hifiberry-dacplus' to '/boot/config.txt'"
