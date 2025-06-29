from pygame import *
from random import randint 
import time as tm

window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_height, player_weight):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_weight, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite): 
    def update(self):
        #keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 625:
            self.rect.x += self.speed
    def fire(self):
            bul = Bullet('bullet.png', self.rect.centerx, self.rect.top, 3, 30, 20)
            bullets.add(bul)

i = 0
class Enemy(GameSprite):
    def update(self):
        global i
        if self.rect.y > 500:
            self.rect.y = 0
            i = i + 1
            self.rect.x = randint(0, 700)
        else:
            self.rect.y += self.speed

class Bullet(GameSprite):
    def update(self):
        if self.rect.y < 0:
            self.kill()
        else:
            self.rect.y -= self.speed

class Meteorite(GameSprite):
    def update(self):
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 700)
        else:
            self.rect.y += self.speed

clock = time.Clock()
FPS = 60

rocket = Player('rocket.png', 330, 395, 5, 100, 50)
monster_1 = Enemy('ufo.png', randint(0, 700), -10, 3, 40, 65)
monster_2 = Enemy('ufo.png', randint(0, 700), -6, 2, 40, 65)
monster_3 = Enemy('ufo.png', randint(0, 700), 0, 1, 40, 65)
monster_4 = Enemy('ufo.png', randint(0, 700), -4, 2, 40, 65)
monster_5 = Enemy('ufo.png', randint(0, 700), -2, 2, 40, 65)
planetoid_1 = Meteorite('asteroid.png', randint(0, 700), 1, 2, 40, 40)
planetoid_2 = Meteorite('asteroid.png', randint(0, 700), 3, 1, 40, 40)
planetoid_3 = Meteorite('asteroid.png', randint(0, 700), 2, 3, 40, 40)
planetoid_4 = Meteorite('asteroid.png', randint(0, 700), 4, 2, 40, 40)

bullets = sprite.Group()

asteroids = sprite.Group()
asteroids.add(planetoid_1)
asteroids.add(planetoid_2)
asteroids.add(planetoid_3)
asteroids.add(planetoid_4)

monsters = sprite.Group()
monsters.add(monster_1)
monsters.add(monster_2)
monsters.add(monster_3)
monsters.add(monster_4)
monsters.add(monster_5)

font.init()
letter = font.SysFont('Comic Sans MS', 30)
fount = font.SysFont('Comic Sans MS', 20)
win = letter.render('YOU WIN', True, (255, 243, 181))
loss = letter.render('YOU LOSE', True, (255, 82, 97))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.8)
mixer.music.play()
fire = mixer.Sound('fire.ogg')

points = 0

lifes = 3

num_fire = 0

rel_time = False

slug = tm.time()

finish = False
game = True
while game:
    if finish != True:
        window.blit(background, (0, 0))
        collides = sprite.groupcollide(monsters, bullets, True, True)
        colli = sprite.groupcollide(asteroids, bullets, True, True)
        for collide in collides:
            points = points + 1
            monster_1 = Enemy('ufo.png', randint(0, 700), -10, 3, 40, 65)
            monsters.add(monster_1)
        collid = sprite.spritecollide(rocket, monsters, True)
        keys_pressed = key.get_pressed()
        collideses = sprite.spritecollide(rocket, asteroids, True)
        for coll in collideses:
            lifes = lifes - 1
        for encounter in collid:
            lifes = lifes - 1
        if keys_pressed[K_SPACE]:
            if tm.time() - slug >= 0.4:
                slug = tm.time()
                if num_fire < 5 and rel_time == False:
                    rocket.fire()
                    fire.set_volume(0.2)
                    fire.play()
                    num_fire = num_fire + 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    recharge = tm.time()
        if rel_time == True:
            overcharge = tm.time()
            if overcharge - recharge >= 3:
                num_fire = 0
                rel_time = False
            else:
                reloading = fount.render('Подождите, идет перезарядка', True, (239, 0, 0))
                window.blit(reloading, (250, 400))
        rocket.reset()
        rocket.update()
        asteroids.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        asteroids.update()
        monsters.update()
        bullets.update()
        missed = letter.render('Пропущено: ' + str(i), True, (255, 255, 255))
        check = letter.render('Счет: ' + str(points), True, (255, 255, 255))
        life = letter.render('Жизни: ' + str(lifes), True, (255, 255, 255))
        window.blit(check, (0, 15))
        window.blit(missed, (0, 50))
        window.blit(life, (0, 85))
        if lifes <= 0:
            finish = True
            window.blit(loss, (300, 200))
            mixer.music.stop()
        if points == 10:
            finish = True
            window.blit(win, (350, 250))
            mixer.music.stop()
        if i >= 3:
            finish = True
            window.blit(loss, (300, 200))
            mixer.music.stop()

    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_e and finish == True:
                finish = False
                i = 0
                points = 0
                lifes = 3
                for clean in monsters:
                    clean.kill()
                for purification in bullets:
                    purification.kill()
                for purge in asteroids:
                    purge.kill()
                monster_1 = Enemy('ufo.png', randint(0, 700), -10, 3, 40, 65)
                monster_2 = Enemy('ufo.png', randint(0, 700), -6, 2, 40, 65)
                monster_3 = Enemy('ufo.png', randint(0, 700), 0, 1, 40, 65)
                monster_4 = Enemy('ufo.png', randint(0, 700), -4, 2, 40, 65)
                monster_5 = Enemy('ufo.png', randint(0, 700), -2, 2, 40, 65)
                planetoid_1 = Meteorite('asteroid.png', randint(0, 700), 1, 2, 40, 40)
                planetoid_2 = Meteorite('asteroid.png', randint(0, 700), 3, 1, 40, 40)
                planetoid_3 = Meteorite('asteroid.png', randint(0, 700), 2, 3, 40, 40)
                planetoid_4 = Meteorite('asteroid.png', randint(0, 700), 4, 2, 40, 40)
                asteroids = sprite.Group()
                asteroids.add(planetoid_1)
                asteroids.add(planetoid_2)
                asteroids.add(planetoid_3)
                asteroids.add(planetoid_4)
                monsters.add(monster_1)
                monsters.add(monster_2)
                monsters.add(monster_3)
                monsters.add(monster_4)
                monsters.add(monster_5)
                mixer.music.set_volume(0.8)
                mixer.music.play()

        if e.type == QUIT:
            game = False

    clock.tick(FPS)
    display.update()