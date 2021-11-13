USB Music Player with the PocketBeagle

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
