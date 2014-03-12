# Switcharoo

Switcharoo is a simple word game where you have three minutes to make as many four-letter words as you can. You can score extra bonuses by changing the same letter repeatedly, making colours, or matching the chosen word of your mentor, Melody.
  

##  Running it

Switcharoo uses Gloss, an OpenGL-based Python library. Gloss is in turn based on PyGame, so you should install the following to make sure it works: Python, PyGame, Python OpenGL, Numpy, SDL, SDL Mixer, SDL TTF.

Once those are installed, just run "python switcharoo.py" to begin.


## Known issues

* I've had reports from some users that the game may lock up on some Linux distros. If this happens to you, look for this line of code near the end of switcharoo.py:
	
 #os.environ['SDL_AUDIODRIVER'] = 'pulseaudio' # silly Ubuntu workaround - hangs without this line!
		
 Remove the # at the beginning of the line, then save the file and try running it again. If that still doesn't work, try changing "pulseaudio" to "esd" - again, some people have reported that as a solution.
	
* On some graphics cards, the spotlights in the menu screen have a square edge around them. Hurray for standards!
	
* The high scores don't actually work - I've made them unrealistically high in the hope that no one actually notices! (NB: the whole Game Over sequence and High Score section is lame and ought to be redone)


##  Version history

v0.5 - September 16th 2010
	- First release.


##  Reading the source
 
Switcharoo is licensed under the GPLv3, so the source code is there for you to read, modify, share and enjoy. That said, it was also written in a few days as part of a "make a game" competition for a  podcast, so don't expect any wizardry - patches to make the code cleaner are most welcome!


##  Contributing

If you'd like to contribute to Switcharoo, great! Get in touch with me at paul.hudson@gmail.com and we'll talk. Code, graphics, sound effects, music, etc are all welcome. If you spot any bugs, drop me a line with some sort of helpful error message - ie, what I have to do to reproduce the error - and I'll get on the case.


##  SDL
    
The Simple DirectMedia Layer (SDL for short) is a cross-platfrom library designed to make it easy to write multi-media software, such as games and emulators.

The Simple DirectMedia Layer library source code is available from: http://www.libsdl.org/

This library is distributed under the terms of the GNU LGPL license: http://www.gnu.org/copyleft/lesser.html
