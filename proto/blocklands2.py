# Copyright 2018, Eric Clack, eric@bn7.net
# This program is distributed under the terms of the GNU General
# Public License

"""Blocklands : hidden landscapes

DONE:
- Show blocks immediately around fred

TODO:
- Start in middle and show Fred
- Line of sight
"""

import random, time
from packages import *

BLOCK_SIZE=50
SCREEN_SIZE=16

create_canvas()

block_images = {
    'mud': PhotoImage(file='../examples/images/earth.gif'),
    'boulder': PhotoImage(file='../examples/images/ball.gif'),
    'wall': PhotoImage(file='../examples/images/wall.gif'),
    'gem': PhotoImage(file='../examples/images/gem.gif'),
    'hidden': PhotoImage(file='../examples/images/black.gif'),
}

fred_img = PhotoImage(file='../examples/images/smallface.gif')

class BlockSprite(ImageSprite):
    def __init__(self, what, x=0, y=0):
        self.what = what
        self.falling = False
        self.visible = True
        image = block_images[what]
        hidden = block_images['hidden']
        super(BlockSprite, self).__init__([image, hidden], x, y)

    def is_a(self, what):
        return (self.what == what)

    def show(self):
        self.switch_costume(1)

    def hide(self):
        self.switch_costume(2)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def block_choices():
    """More gems, boulders and walls the higher the level"""
    c1 = ['mud'] * 20
    c2 = ['wall', 'boulder', 'gem'] * world.level
    c1.extend(c2)
    return c1

def make_landscape():
    landscape = []
    for y in range(SCREEN_SIZE):
        landscape.append([])
        for x in range(SCREEN_SIZE):
            if (x, y) == coords(fred):
                what = None
            elif x in (0, (SCREEN_SIZE-1)) or y in (0, (SCREEN_SIZE-1)):
                what = 'wall'
            else:
                what = random.choice(block_choices())

            if what:
                block = BlockSprite(what)
                block.move_to(x*BLOCK_SIZE, y*BLOCK_SIZE)
                block.hide()
            else:
                block = None
            landscape[-1].append(block)
                
    return landscape

def clear_landscape():
    for row in world.landscape:
        for i in row:
            if i: i.delete()
    landscape = []

def show_visible_landscape():
    """Show landscape around fred, that which he can see"""

    # First show the blocks right next to him
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            block = what_is_next_to(fred, dx, dy)
            if block: block.show()

    # Now further out, provided nothing (except earth)
    # is in the way
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            block = what_is_next_to(fred, dx, dy)
            if block and fred_can_see(dx, dy):
                block.show()
    
    
def coords(sprite):
    cx, cy = sprite.pos()
    cx = int(cx/BLOCK_SIZE); cy = int(cy/BLOCK_SIZE)
    return (cx, cy)

def all_blocks_of(what):
    b = []
    for rows in world.landscape:
        for i in rows:
            if i and i.is_a(what):
                b.append(i)
    return b

def all_boulders():
    return all_blocks_of('boulder')

def all_gems():
    return all_blocks_of('gem')

def what_is_next_to(sprite, dx, dy):
    cx, cy = coords(sprite)
    if sprite != fred and (cx+dx, cy+dy) == coords(fred):
        return fred
    try:
        return world.landscape[cy+dy][cx+dx]    
    except IndexError:
        return None

def fred_can_see(dx, dy):
    """No blocks between fred and relative (dx, dy)?"""
    fx, fy = coords(fred)    
    length = max(abs(dx), abs(dy))
    #print("Checking from %s to %s, length %s" % ((fx, fy), (dx, dy), length))
    
    # increments to take us to dx, dy over `length` iterations
    xi = dx / length
    yi = dy / length
    
    for i in range(1, length):
        x = int(xi*i); y = int(yi*i)
        #print(x, y)
        block = what_is_next_to(fred, x, y)
        if block and block.what in ['boulder', 'wall', 'gem']:
            return False
    return True

def can_move(dx, dy):
    sprite = what_is_next_to(fred, dx, dy)
    return sprite is None or sprite.is_a('mud') or sprite.is_a('gem')

def set_landscape(a_pair, what):
    x, y = a_pair
    world.landscape[y][x] = what

def clear_block():
    """Clear the block that fred just landed on"""
    x, y = coords(fred)
    block = world.landscape[y][x]
    if block:
        world.landscape[y][x] = None
        if block.is_a('gem'): world.gems_left -= 1
        block.delete()

def move(dx, dy):
    if world.status != 'play': return

    if can_move(dx, dy):
        fred.move(dx*BLOCK_SIZE, dy*BLOCK_SIZE)
        clear_block()
        if world.gems_left <= 0:
            banner("Well done!")
            world.status = 'next_level'
    elif dy == 0:
        next_block = what_is_next_to(fred, dx, 0)
        next_next_block = what_is_next_to(fred, dx*2, 0)
        if next_block.is_a('boulder') and next_next_block is None:
            # We can move a boulder
            set_landscape(coords(next_block), None)
            next_block.move(dx*BLOCK_SIZE, 0)
            set_landscape(coords(next_block), next_block)
            # Now we can move too
            fred.move(dx*BLOCK_SIZE, 0)
    show_visible_landscape()
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# World set up
#

world = Struct( level=1, status='play', fred=None, 
                landscape=None, gems_left=None )

def move_fred_to_start():
    fred.move_to(SCREEN_SIZE*BLOCK_SIZE/2,SCREEN_SIZE*BLOCK_SIZE/2)

# These require previous world things to be defined
fred = ImageSprite(fred_img)
move_fred_to_start()
world.fred = fred

world.landscape = make_landscape()
world.gems_left = len(all_gems())
show_visible_landscape()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Events and actions
#

def move_left(event):
    move(-1, 0)

def move_right(event):
    move(1, 0)

def move_up(event): 
    move(0, -1)

def move_down(event):
    move(0, 1)

def boulders_fall():
    for b in all_boulders():
        what = what_is_next_to(b, 0, 1)
        if what is None:
            set_landscape(coords(b), None)
            b.move(0, BLOCK_SIZE)
            b.falling = True
            set_landscape(coords(b), b)
        else:
            if what is world.fred and b.falling:
                banner("Ouch!")
                world.status = 'end'
            else:
                b.falling = False

def start_level(event):
    """Start or restart a level"""
    world.status = 'building'
    clear_banner()
    clear_landscape()
    move_fred_to_start()
    world.landscape = make_landscape()
    show_visible_landscape()    
    world.gems_left = len(all_gems())
    world.status = 'play'

def check_status():
    if world.status == 'next_level':
        world.level += 1
        start_level(None)
    if world.status == 'end':
        end_game()
        

when_key_pressed('<Left>', move_left)
when_key_pressed('<Right>', move_right)
when_key_pressed('<Up>', move_up)
when_key_pressed('<Down>', move_down)
when_key_pressed('r', start_level)

forever(boulders_fall, 200)
forever(check_status, 1000)
mainloop()
