#!/usr/bin/env python3

	"""See the license below.
    	
    	OneLoneCoder.com - Command Line First Person Shooter (FPS) Engine
	"Why were games not done like this is 1990?" - @Javidx9
    	"Weren't you coding in '90? You tell me." - nuclearfall
	
	As Javidx9's website name implies, I am not affiliated with onelonecoder
	in any way. - nf

	License
	~~~~~~~
	Copyright (C) 2018  Javidx9
	This program comes with ABSOLUTELY NO WARRANTY.
	This is free software, and you are welcome to redistribute it
	under certain conditions; See license for details.
	Original works located at:
	https://www.github.com/onelonecoder
	https://www.onelonecoder.com
	https://www.youtube.com/javidx9

	GNU GPLv3
	https://github.com/OneLoneCoder/videos/blob/master/LICENSE
    

	From Javidx9 :)
	~~~~~~~~~~~~~~~
	Hello! Ultimately I don't care what you use this for. It's intended to be
	educational, and perhaps to the oddly minded - a little bit of fun.
	Please hack this, change it and use it in any way you see fit. You acknowledge
	that I am not responsible for anything bad that happens as a result of
	your actions. However this code is protected by GNU GPLv3, see the license in the
	github repo. This means you must attribute me if you use it. You can view this
	license here: https://github.com/OneLoneCoder/videos/blob/master/LICENSE
	Cheers!
    
    From nuclearfall (.cpp to .py)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    This is pretty much a straight up copy of Javidx9's CLFPS logic from C++/Windows 
    to Python/*Nix. I utilize the curses library for display. Anything that makes
    it look worse is probably my fault, but I'm unlikely to play with this much, as
    it was a learning excercise. 
    
    If you want a better documented file, explaining exact goings on of the code,
    you should download Javidx9's .cpp code. It has extensive documentation and
    made it a lot easier for me to understand how ray tracing and shading works
    in concept. Huge thanks go to Javidx9 for all of his work on video tutorials.

	Background
	~~~~~~~~~~
	Whilst waiting for TheMexicanRunner to start the finale of his NesMania project,
	his Twitch stream had a counter counting down for a couple of hours until it started.
	With some time on my hands, I thought it might be fun to see what the graphical
	capabilities of the console are. Turns out, not very much, but hey, it's nice to think
	Wolfenstein could have existed a few years earlier, and in just ~200 lines of code.

	IMPORTANT!!!!
	~~~~~~~~~~~~~
	READ ME BEFORE RUNNING!!! This program expects the console dimensions to be set to
	120 Columns by 40 Rows. I recommend a small font "Consolas" at size 16. You can do this
	by running the program, and right clicking on the console title bar, and specifying
	the properties. You can also choose to default to them in the future.

	Controls: A = Turn Left, D = Turn Right, W = Walk Forwards, S = Walk Backwards

	Future Modifications
	~~~~~~~~~~~~~~~~~~~~
	1) Shade block segments based on angle from player, i.e. less light reflected off
	walls at side of player. Walls straight on are brightest.
	2) Find an interesting and optimised ray-tracing method. I'm sure one must exist
	to more optimally search the map space.
	3) Add bullets!
	4) Add bad guys!

	Author
	~~~~~~
	Twitter: @javidx9
    
	Blog: www.onelonecoder.com

	Video:
	~~~~~~
	https://youtu.be/xW8skO7MFYw

	Updated: 27/02/2017
    Updated: 14/09/2019 (nuclear fall)"""


from curses import wrapper
import curses
import time
import math

def main(stdscr):
    screenwidth = 120			# Console Screen Size X (columns)
    screenheight = 40;			# Console Screen Size Y (rows)
    mapwidth = 16;				# World Dimensions
    mapheight = 16;
    playerx = 14.4      		# Player Start Position 
    playery = 15.4              # *nf- I changed the map a bit so the player starts at an entrance.
    playera = 3.14159 		    # Player Start Rotation *nf - changed so character is facing west.*
    fov = 3.14159 / 4.0	        # Field of View
    depth = 16.0			    # Maximum rendering distance
    speed = 5.0			        # Walking Speed *nf - You may need to adjust this*
    turn_speed = 8.0            # *nf - I found turn speeds to be too slow at walking speed.*

    screen = ' ' * screenwidth * screenheight
    map = ''
    map += '###########....#'
    map += '#..............#'
    map += '#.......########'
    map += '#..............#'
    map += '#......##......#'
    map += '#......##......#'
    map += '#.......#..#...#'
    map += '###............#'
    map += '##.............#'
    map += '#......####..###'
    map += '#......#.......#'
    map += '#......#.......#'
    map += '#..............#'
    map += '#..........#####'
    map += '#...............'
    map += '################'
    curses.resize_term(40, 120)
    stdscr.refresh()
    stdscr.nodelay(True)
    stdscr.leaveok(True)
    curses.curs_set(0)
    start = time.time()
    elapsed = time.time()

    # javidx9 - We'll need time differential per frame to calculate modification to movement speeds, 
    # to ensure consistant movement, as ray-tracing is non-deterministic. 
    # *^nf - This may be an issue with my movement speeds. I may not be properly timing things.*

    while True:  
        # prevents initial division by zero
        if elapsed is 0.0:
            elasped = .001
        start = time.time()
        key = stdscr.getch()
        if key is ord('a'):
            playera -= turn_speed * elapsed
        if key is ord('d'):
            playera += turn_speed * elapsed
        if key is ord('w'):
            playerx += math.sin(playera) * speed * elapsed
            playery += math.cos(playera) * speed * elapsed
            if map[int(playerx) * mapwidth + int(playery)] == '#':
                playerx -= math.sin(playera) * speed * elapsed
                playery -= math.cos(playera) * speed * elapsed
        if key is ord('s'):
            playerx -= math.sin(playera) * speed * elapsed
            playery -= math.cos(playera) * speed * elapsed
            if map[int(playerx) * mapwidth + int(playery)] == '#':
                playerx += math.sin(playera) * speed * elapsed
                playery += math.cos(playera) * speed * elapsed
        if key is ord('q'):
            quit()

        for x in range(screenwidth):
            rayangle = (playera - fov / 2.0) + (x / screenwidth) * fov
            stepsize = 0.1
            towall = 0.0
            has_hitwall = False
            boundary = False

            eyesx = math.sin(rayangle)
            eyesy = math.cos(rayangle)

            while not has_hitwall and towall < depth:
                towall += stepsize
                testx = int(playerx + eyesx * towall)
                testy = int(playery + eyesy * towall)

                if testx < 0 or testx >= mapwidth or testy < 0 or testy >= mapheight:
                    has_hitwall = True
                    towall = depth
                else:
                    if map[int(testx * mapwidth + testy)] is '#':
                        has_hitwall = True
                        # *nf - A CPP vector is basically equivalent to a top level python list*
                        p = []
                        for tx in range(2):
                            for ty in range(2):
                                vy = testy + ty - playery
                                vx = testx + tx - playerx
                                d = math.sqrt(vx*vx + vy*vy)
                                dot = (eyesx * vx / d) + (eyesy * vy / d)
                                p.append([d, dot])
                        p.sort()

                        bound = 0.001
                        if math.acos(p[0][1]) < bound:
                            boundary = True
                        if math.acos(p[1][1]) < bound:
                            boundary = True
                        if math.acos(p[2][1]) < bound:
                            boundary = True

            ceiling = round((screenheight / 2.0) - screenheight / towall)
            floor = round(screenheight - ceiling)
            
            shade = ' '
            if towall <= depth / 4:
                shade = chr(0x2588)
            elif towall < depth / 3:
                shade = chr(0x2593)
            elif towall < depth / 2:
                shade = chr(0x2592)
            elif towall < depth / 1:
                shade = chr(0x2591)
            else:
                shade = ' '

            if boundary:
                shade = ' '
            for y in range(screenheight):
                index = y * screenwidth + x
                if y <= ceiling:
                    screen = screen[:index] + ' ' + screen[index+1:]
                elif y > ceiling and y <= floor:
                    screen = screen[:index] + shade + screen[index+1:]
                else:
                    b = 1 - (float(y - screenheight / 2.0)) / (float(screenheight /2))
                    if b < 0.25:
                        shade = '#'
                    elif b < 0.5:
                        shade = 'x'
                    elif b < 0.75:
                        shade = '-'
                    elif b < 0.9:
                        shade = '.'
                    else:
                        shade = ' '
                    screen = screen[:index] + shade + screen[index+1:]

        # Place statistics in upper left corner
        stat_str = str(round(playerx,1)) + ", " + str(round(playery,1)) + ", " + str(round(playera,1)) + (str(round(1.0 / elapsed, 1)))
        lenstat = len(stat_str) +1
        screen = screen[:screenwidth-lenstat] + stat_str + screen[screenwidth-2:]

        # Place map in upper right left corner
        for x in range(mapwidth):
            for y in range(mapwidth):
                sindex = (y) * screenwidth + x
                mindex = y * mapwidth + x
                screen = screen[:sindex] + map[mindex] + screen[sindex+1:]
        index = int(playerx) * screenwidth + int(playery)
        # *nf - It's easy to get lost without an indicator on the map of where you are.*
        screen = screen[:index] + 'P' + screen[index+1:]

        index = screenwidth * screenheight -1
        screen = screen[:index] + ''
        stdscr.addstr(0, 0, screen)
        stdscr.refresh()
        elapsed = time.time() - start


wrapper(main)
