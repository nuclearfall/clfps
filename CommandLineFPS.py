#!/usr/bin/env python3

import io
from curses import wrapper
import curses
import time
import locale
import math
import sys

def main(stdscr):
    screenwidth = 120			# Console Screen Size X (columns)
    screenheight = 40;			# Console Screen Size Y (rows)
    mapwidth = 16;				# World Dimensions
    mapheight = 16;
    playerx = 14.4      		# Player Start Position
    playery = 15.4
    playera = 3.14  		# Player Start Rotation
    fov = 3.14159 / 4.0	    # Field of View
    depth = 16.0			# Maximum rendering distance
    speed = 8.0			# Walking Speed
    turn_speed = 10.0

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

# We'll need time differential per frame to calculate modification to movement speeds, to ensure consistant movement, as ray-tracing is non-deterministic

# Handle backwards movement & collision
    while True:  # prevents initial division by zero
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
        screen = screen[:index] + 'P' + screen[index+1:]


        index = screenwidth * screenheight -1
        screen = screen[:index] + ''
        stdscr.addstr(0, 0, screen)
        stdscr.refresh()
        elapsed = time.time() - start




wrapper(main)
