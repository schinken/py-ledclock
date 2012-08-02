import random
import time
import math
import bitmapfont
import pygame, sys,os
from pygame.locals import * 


DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 400

DOT_SPEED_X = float(DISPLAY_WIDTH)/4.0
DOT_SPEED_Y = float(DISPLAY_HEIGHT)/4.0

DOT_PADDING = 10

class Dot(object):

    def __init__(self, color=(100,100,100)):
        self.screen = pygame.display.get_surface()
        self.set_color( color )

    def set_color(self, color):
        self.color = color

    def draw(self):
        x, y = self.get_pos()
        pygame.draw.circle( self.screen, self.color, (x,y), 3)

    def update(self, speed):
        pass    

    def set_pos(self, x, y ):
        self.x, self.y = x, y

    def get_pos(self):
        return int(round(self.x)), int(round(self.y))

class AnimatedDot(Dot):
 
    def __init__(self, color):
        super(AnimatedDot,self).__init__(color)

        self.mv_x = random.random()*DOT_SPEED_X-(DOT_SPEED_X/2.0)
        self.mv_y = random.random()*DOT_SPEED_Y-(DOT_SPEED_Y/2.0)

    def update(self, speed):
        self.mv_y += 2.0
        self.x += self.mv_x * speed
        self.y += self.mv_y * speed

class AnimationPool(object):

    def __init__(self):
        self.items = []

    def add_object(self, obj):
        self.items.append(obj)

    def update(self,speed):
        for item in self.items:
            item.update(speed)

    def draw(self):
        for item in self.items:
            item.draw()

class Digit(object):

    def __init__(self, number, x, y):

        self.animated = []
        self.dots = []
        self.current_mask = None

        print x, y

        for h in xrange(bitmapfont.height):
            for w in xrange(bitmapfont.width):

                cur_x = (w+1) * DOT_PADDING + x
                cur_y = (h+1) * DOT_PADDING + y

                dot = Dot()
                dot.set_pos( cur_x, cur_y )

                self.dots.append( dot )

        self.x = x
        self.y = y
        self.set_number(number)

    def set_number(self, number):
    
        self.number = number
        mask = bitmapfont.digits[number]

        self.animate_diff(mask)
        self.current_mask = mask

        for index, val in enumerate(mask):
            if val:
                self.set_digitcolor(index, (200, 200, 200))
            else:
                self.set_digitcolor(index, (60, 60, 60))

    def animate_diff(self, new_mask):
        
        if self.current_mask is None:
            return

        for index, new_value in enumerate(new_mask):
            old_value = self.current_mask[index]

            if old_value == 1 and new_value == 0:
                x, y = self.dots[index].get_pos()

                anim_dot = AnimatedDot((200,0,0))
                anim_dot.set_pos(x,y)

                self.animated.append(anim_dot)

    def set_digitcolor(self, index, color):
        self.dots[index].set_color(color)

    def draw(self):

        for dot in self.animated:
            dot.draw()

        for dot in self.dots:
            dot.draw()

    def update(self,speed):

        for index, dot in enumerate(self.animated):
            x,y = dot.get_pos()

            if x >= DISPLAY_WIDTH or y >= DISPLAY_HEIGHT:
                del self.animated[index]

            dot.update(speed)

class Clock(object):

    def __init__(self, offset_x, offset_y):
        
        self.last_time = None
        self.digits = []

        for digit in '00:00:00':
            if digit == '0':
                dig = Digit(0, offset_x, offset_y)
                self.digits.append(dig)
                offset_x += 50
            else:
                offset_x += 20

    def update_clock(self):

        clock = self.get_clock()
        if self.last_time != clock:
            for index,digit in enumerate(clock):
                self.digits[index].set_number( int(digit) )

            self.last_time = clock

    def update(self,speed):
        for digit in self.digits:
            digit.update(speed)

    def draw(self):
        for digit in self.digits:
            digit.draw()

    def get_clock(self):
        return time.strftime("%H%M%S")

def main():

    pygame.init() 
    
    window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT)) 
    pygame.display.set_caption('Jumping dots') 
    screen = pygame.display.get_surface() 

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))


    dot_clock = Clock(100, 50)

    pygame.display.flip()
    clock = pygame.time.Clock()
    pygame.time.set_timer(USEREVENT+1, 200)

    while True:
        ticks = clock.tick(60)
        speed = 1 / float(ticks)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == USEREVENT+1:
                dot_clock.update_clock()
        
        screen.blit(background, (0, 0))

        dot_clock.update(speed)
        dot_clock.draw()
            
        #Draw Everything
        pygame.display.flip()

if __name__ == '__main__':
    main()

