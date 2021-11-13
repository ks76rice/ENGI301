USB Music Player with the PocketBeagle

How to Build:
1. The first step is to wire the breadboard to add a USB Port. To do this, the ID (P1_13) and GND (P1_15) pins of the PocketBeagle must be soldered together. This should also be done with the VI (P1_7) to VB (P1_5) pins. Next, the four pin USB port is wired to connect VCC to P1_4, D- to P1_6, D+ to P1_8, ID to P1_10, and GND to ID
2. The next step is to wire the PocketBeagle to the SPI screen. First, the IM1, IM2, and IM3 pads need to be soldered
3. Then, connect the GND, Vin, CLK, MISO, MOSI, CS, D/C, and RST pins on the SPI screen to the GND bus, 3.3V bus, P1_08, P1_10, P1_12, P1_06, P1_04, and P1_02, respectively. 
4. The final step is to wire the PocketBeagle to the buttons. This is done by connecting P2_02, P2_04, P2_06, P2_08 to the down, up, play, and pause buttons, respectively. The buttons are wired so that a 1kOhm resistor bridged the 3.3V bus to one end of the button, and the other end of the button was connected to the Ground bus. 
5. Finally, simply plug the powered USB hub to the USB port. Then plug the USB with songs and the USB speaker to the powered USB hub. 

How to Run:
1. Download latest PocketBeagle image from PocketBeagle.org
2. Install the VLC media player package with this command: sudo pip3 install python-vlc
3. Run the following lines to install basic system tools and Adafruit libraries:
      sudo apt-get update
      sudo apt-get install build-essential python-dev python-setuptools python-smbus -y
      sudo apt-get install python-pip python3-pip -y
      sudo apt-get install zip

      sudo pip3 install --upgrade setuptools
      sudo pip3 install --upgrade Adafruit_BBIO
      sudo pip3 install adafruit-blinka
4. Open the folder and change the run permissions: chmod 755 run
5. Enter "sudo chrontab -e" in the command line
6. Paste this line into the window: @reboot sleep 30 && sh <path to 'run' script> > /var/lib/cloud9/logs/cronlog2>&1
7. Create a place in Cloud9 for your USB to automatically act as extra storage, detailed at https://linuxpropaganda.wordpress.com/2018/10/10/beaglebone-black-add-usb-thumb-drive-as-extra-storage-in-ubuntu-server/
8. Plug the USB into the powered USB hub. Note: the songs cannot be in a folder, but have to be flat on the USB for the program to function correctly. 
9. Power on the PocketBeagle.
10. Use the selector buttons (green) to select between songs. The left moves the indicator up and the right moves the indicator down.
11. Press the black button to play the selected song.
12. Press the blue button to pause the selected song.



More detailed instructions found here: https://www.hackster.io/432580/usb-music-player-with-the-pocketbeagle-0b1624
