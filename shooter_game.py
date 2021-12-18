#Создай собственный Шутер!
win_height = 500
from pygame import *
from random import randint
from time import time as timer
#делаем экран
window = display.set_mode((700, 500))
display.set_caption("шутер(ура!!! стрелялка)")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
#делаем музыку
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
#класс для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
#класс игрока
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
        mixer.music.load("fire.ogg")
        mixer.music.play()
#класс врага
lost = 0
schet = 0
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost = lost + 1
#класс астероидов
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
#класс пули
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
#объекты в игре
ship = Player("rocket.png", 5, 400, 80, 100, 10)
monsters = sprite.Group()
for a in range(1, 6):
    monster = Enemy("ufo.png", randint(80, 620), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
asteroids = sprite.Group()
asteroid = Asteroid("asteroid.png", randint(80, 620), -40, 80, 50, 5)
asteroids.add(asteroid)
bullets = sprite.Group()
font.init()
font1 = font.SysFont('Times New Roman', 36)
font2 = font.SysFont('Times New Roman', 36)
font3 = font.SysFont('Times New Roman', 36)
font4 = font.SysFont('Times New Roman', 36)
font5 = font.SysFont('Times New Roman', 36)
font6 = font.SysFont('Times New Roman', 36)
num_fire = 0
rel_time = False
hp = 3
#игровой цикл
run = True
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    ship.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        window.blit(background, (0, 0))
        text_lost = font1.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        text_schet = font2.render("Счёт:" + str(schet), 1, (255, 255, 255))
        text_win = font3.render("YOU WIN!!!", True,  (255, 215, 0))
        text_lose = font4.render("YOU LOSE, you are a noob!", True,  (255, 215, 0))
        text_hp = font6.render(str(hp), 1, (0, 150, 0))

        if schet >= 100:
            window.blit(text_win, (200, 200))
            finish = True
        if lost >= 3 or sprite.spritecollide(ship, monsters, True) or sprite.spritecollide(ship, asteroids, True):
            #window.blit(text_lose, (200, 200))
            hp -= 1

        if hp == 0:
            finish = True
            window.blit(text_lose, (200, 200))
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font5.render("Wait, reload...", 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        window.blit(text_lost, (10, 50))
        window.blit(text_schet, (10, 20))
        window.blit(text_hp, (650, 10))
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window) 
        collide = sprite.groupcollide(monsters, bullets, True, True)
        for c in collide:
            schet = schet + 1
            monster = Enemy("ufo.png", randint(80, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        #if hp == 0:
            #finish = True
        display.update()
    else:
        finish = False
        schet = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        #for e in event.get():
            #if e.type == K_R:
        for i in range(1, 6):
            monster = Enemy("ufo.png", randint(80, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1, 2):
            asteroid = Asteroid("asteroid.png", randint(80, 620), -40, 80, 50, 5)
            asteroids.add(asteroid)
        hp = 3
    time.delay(50)