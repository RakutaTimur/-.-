#Создай собственный Шутер!

from pygame import *
from random import randint
import time as tm
from time import sleep

cur_time = tm.time()
window = display.set_mode((700, 500))
display.set_caption('99.9% не могут пройти эту игру')
background = transform.scale(image.load('galaxy.jpg'), (700,500))

clock = time.Clock()

mixer.init()
mixer.music.load('space.ogg')
babax = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_hight, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_hight))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

bullets = sprite.Group()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= 10
        
        if keys_pressed[K_DOWN] and self.rect.y < 400:
            self.rect.y += 10
        
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= 10

        if keys_pressed[K_RIGHT] and self.rect.x < 620:
            self.rect.x += 10

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
        babax.play()     
        
lost = 0

sprite_maksim = Player('rocket.png', 200, 400, 80, 100, 4)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            global lost
            self.rect.y = -80
            self.rect.x = randint(0, 630)
            self.speed = randint(1, 3)
            lost += 1

class Asteroidi(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            global lost
            self.rect.y = -80
            self.rect.x = randint(0, 630)
            self.speed = randint(1, 3)

font.init()
font1 = font.SysFont('Arial', 25)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
sc = 0
monsters = sprite.Group()
meteors = sprite.Group()
for i in range(5):
    meteor = Asteroidi('asteroid.png', randint(0, 630), -100, 80, 50, randint(1, 3))
    meteors.add(meteor)

for i in range(5):
    monster = Enemy('ufo.png', randint(0, 630), -80, 80, 50, randint(1, 3))
    monsters.add(monster)

reload_time = 5
health = 2

game = True 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
            
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                sprite_maksim.fire()

    window.blit(background, (0,0))
    sprite_maksim.reset()
    sprite_maksim.update()
    monsters.draw(window)
    monsters.update()
    bullets.draw(window) 
    bullets.update()
    meteors.draw(window)
    meteors.update() 

    if sprite.spritecollide(sprite_maksim, monsters, False) or sprite.spritecollide(sprite_maksim, meteors, False):
        health -= 1
    
    if health ==  0:
        lose = font1.render('YOU LOSE', 1, (200, 100, 5))
        window.blit(lose, (300, 250))
        game = False

    hp = font1.render('Жизней: ' + str(health), 1, (70,80,90))
    window.blit(hp, (570, 10)) 

    if sprite.groupcollide(monsters, bullets, True, True):
        ms = Enemy('ufo.png', randint(0, 630), -80, 80, 50, randint(1, 3))
        monsters.add(ms)
        sc += 1    
    
    score1 = font1.render('Счёт: ' + str(sc), True, (200, 100, 5))
    window.blit(score1, (10, 30))

    if sc == 10:
        win = font1.render('YOU WIN', 1, (200, 100, 5))
        window.blit(win, (300, 250))
        game = False

    score = font1.render('Пропущено: ' + str(lost), True, (255, 255, 255))
    window.blit(score, (10, 60))
    if lost == 3:
        lose = font1.render('YOU LOSE', 1, (200, 100, 5))
        window.blit(lose, (300, 250))
        game = False
    
    display.update()
    clock.tick(60)