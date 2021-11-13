"""
--------------------------------------------------------------------------
MP3 Player
--------------------------------------------------------------------------
License:   
Copyright 2021 <Kevin Sun>

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Use an SPI screen with buttons and a USB speaker to create an MP3 player

Requirements:
  - play a song when a button is pressed
  - play and pause a song
  - display what song is being played and what song is selected

"""
import time
import busio
import board
import digitalio
import os 
import vlc

from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import color565
import adafruit_rgb_display.ili9341 as ili9341

import Adafruit_BBIO.GPIO as GPIO
# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class MP3Player():
    """ People Counter """
    #buttons
    button_up = None
    button_down = None
    button_play = None
    button_pause = None
    #screen
    spi = None
    display = None
    reset_pin = None
    dc_pin = None
    cs_pin = None
    song_list = None
    
    def __init__(self, reset_time=2.0, button_up="P2_4", button_down="P2_2", 
    button_play="P2_6", button_pause="P2_8", sclock = board.SCLK, MISO = board.MISO, 
    MOSI = board.MOSI, BAUDRATE = 24000000, reset = board.P1_2, dc = board.P1_4, cs= board.P1_6):
        """ Initialize variables and set up display """
        self.button_up = button_up
        self.button_down = button_down
        self.button_play = button_play
        self.button_pause= button_pause
        
        self.reset_pin = digitalio.DigitalInOut(reset)
        self.dc_pin = digitalio.DigitalInOut(dc)
        self.cs_pin = digitalio.DigitalInOut(cs)
        self.spi = busio.SPI(clock=sclock, MISO=MISO, MOSI=MOSI)
        self.display = ili9341.ILI9341(spi = self.spi, cs = self.cs_pin, dc = self.dc_pin, rst = self.reset_pin, baudrate=BAUDRATE)
        self.song_list = []
        self._setup()
    # End def
    
    
    def _setup(self):
        """Setup the hardware components."""
        # Initialize Display - display Hello to show that program has been started and the screen has been initialized
        width    = self.display.width
        height   = self.display.height
        BORDER   = 20
        FONTSIZE = 24
        image = Image.new("RGB", (width, height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a white filled box as the background
        draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
        self.display.image(image)

        # Load a TTF Font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

        # Draw Some Text
        text = "Hello!"
        (font_width, font_height) = font.getsize(text)
        draw.text((width // 2 - font_width // 2, height // 2 - font_height // 2),text, font=font, fill=(0, 0, 0),)

        # Display image.
        self.display.image(image)
        
        # Initialize Buttons
        GPIO.setup(self.button_up,GPIO.IN)
        GPIO.setup(self.button_down,GPIO.IN)
        GPIO.setup(self.button_play,GPIO.IN)
        GPIO.setup(self.button_pause,GPIO.IN)

    # End def
    
    def display_songs(self, song_list, button_count):
        width = self.display.width
        height = self.display.height

	#adjust font size based on the number of songs present
        if len(song_list) > 7:
            FONTSIZE = int(160/len(song_list))
        else:
            FONTSIZE = int(60/len(song_list))
        image = Image.new("RGB", (width, height))
    
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        
        # Draw a white filled box as the background
        draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
        self.display.image(image)

        # Load a TTF Font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)
        
        # Draw the song files on the USB
        text = song_list
        for x in range(len(song_list)):
            (font_width, font_height) = font.getsize(song_list[x])
            draw.text((width // 2 - font_width // 2, x*1.5*font_height), song_list[x], font=font, fill=(0, 0, 0),)
        
	#draw an indicator to show which song is being selected
        draw.rectangle((5, button_count*1.5*font_height, font_width//5, button_count*1.5*font_height+font_height), fill=(0, 0, 255))

        # Display image.
        self.display.image(image)
    # End def
    
    def get_songs(self):
        self.song_list = os.listdir("/var/lib/cloud9/media/USB") #use OS command to read the songs in this file
    # End def

    def run(self):
        """Execute the main program."""
        button_count                 = 0        # Number of times the button has been pressed
        self.get_songs()			# retrieve the song list
        self.display_songs(self.song_list, button_count)	#display the songs
        song_selected_2 = 'holder'		#holder variable to compare to when deciding to either continue playing the song that was previously playing or start a new one
        
        while(True):
            # Wait for any button press
            while(GPIO.input(self.button_up) + GPIO.input(self.button_down) + GPIO.input(self.button_play) + GPIO.input(self.button_pause) == 4):
                time.sleep(0.1)
            
		    #if the up button is pressed, increase the button count and update the screen to move the indicator
            if GPIO.input(self.button_up) == 0:
                button_count += 1
                self.display_songs(self.song_list, button_count)
            
            #if the down button is pressed, increase the button count and update the screen to move the indicator
            if GPIO.input(self.button_down) == 0:
                button_count -= 1
                self.display_songs(self.song_list, button_count)
            
            #if the play button is pressed, play the selected song
            if GPIO.input(self.button_play) == 0:
                song_selected_1 = self.song_list[button_count] #extract highlighted song
                if song_selected_1 != song_selected_2: #if the song is different from the holder variable, play the new song from the beginning
                    song_loc = "/var/lib/cloud9/media/USB/" + song_selected_1
                    print(song_loc)
                    p = vlc.MediaPlayer(song_loc)
                    p.stop()
                    p.play()
                else: #if the song is not different from the holder variable, continue playing the old song from where it was paused
                    p.play()
                    
                
            #if the pause button is pressed, pause the selected song    
            if GPIO.input(self.button_pause) == 0:
                p.pause()
                song_selected_2 = song_selected_1 #update the holder variable for the next time the play button is pressed
        
    # End def

# End class

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    print("Program Start")
    # Create instantiation of project1
    project1 = MP3Player()
    # run project1
    project1.run()
    print("Program Complete")