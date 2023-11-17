import math
import random

import pygame
import sys

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

POINTS = 0
def hit():
    #Шарик попал в цель.
    global POINTS
    POINTS += 1

    
#Для счёта очков.
def SCORE():
    font = pygame.font.SysFont('comicsansms',32)
    score_table=font.render('SCORE '+str(POINTS), 1 ,BLACK ,(255, 255, 255))
    screen.blit(score_table,(20,20))

class Ball:
    def __init__(self, screen: pygame.Surface, x, y=550):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        #Меняю "self.color = choice(GAME_COLORS)" на "self.color = choice(BLUE)" в следующей строке.
        self.color = BLUE
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
#====================================================================================================
        # FIXME
        #Как я считаю нужным.
        
        #Если мяч "отжил", то он отправляется в точку за экраном и сидит там вечно.
        if self.live<=0:
            self.x = 9000
            self.vx=0
            self.vy=0
            self.y=9000
        gravity = 2

        #Условия на отскок от стены
        if (self.x + self.vx + self.r >= 800) or (self.x +self.vx+ self.r <= 0):
            self.live -= 1
            self.vx *= (-0.6)

        #Условие на отскок от потолка и пола, с учётом, что есть "сила трения" для горизонтальной скорости.
        if (self.y + self.vy + self.r >= 600) or (self.y +self.vy + self.r <= 0):
            self.vy *= (-0.3)
            self.vx *= (0.8)
            self.live -= 1
        
        self.x += self.vx
        self.y += (self.vy)
        self.vy += gravity
#======================================================================================================
    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        # Как я считаю нужным.
        if (self.x-obj.x)**2 + (self.y-obj.y)**2 < (self.r+obj.r)**2:
            return True
        else:
            return False
        
        


class Gun:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x=10
        self.y=550
        self.points=0

        #Для движения танка
        self.vx = 0

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x+50)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        #В следующей строке убрал минус, так как была проблема с направлением вертикальной компоненты скорости в начальный момент времени.
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # FIXIT don't know how to do it
        #Как я понимаю
        #Пушка
        dlina_pushki = self.f2_power
        x = self.x + dlina_pushki*math.cos(self.an)
        y = self.y + dlina_pushki*math.sin(self.an)

        pygame.draw.line(surface= self.screen, color=self.color, start_pos=[self.x+50, self.y],
                         end_pos=[x+50, y], width=10)
        #Корпус
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 50, 50))
        
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY
    #Движение танка.
    def move_tank_right(self):
        self.x += 5
    def move_tank_left(self):
        self.x -= 5

class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def __init__(self, c):
        self.x=random.randint(600, 780)
        self.y=random.randint(300, 550)
        self.color = c
        self.r = random.randint(5, 50)
        self.live=1
        self.points=0

        #Для скоростей мишеней
        self.vx = 0
        self.vy = 0
        
        self.new_target()

    def new_target(self):
        #Создание новой мишени.
        a = random.randint(600, 780)
        self.x = a
        b = random.randint(300, 550)
        self.y = b
        self.r = random.randint(2, 50)
        self.color = RED
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points+=points

    def draw(self):
        #Как я понимаю
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        
    #Движение мишеней: скорости и перемещения + столкновения
    def speed_target(self):
        if POINTS<=4:
            self.vx = 0
            self.vy = 0
        else:
            self.vx=random.randint(-10, 10)
            self.vy=random.randint(-10, 10)
        
    def moving_target(self):
        #Условия на отскок от стен.
        if (self.x + self.vx + self.r >= 800) or (self.x +self.vx+ self.r <= 0):
            self.vx *= (-1)
        #Условие на отскок от потолка и пола.
        if (self.y + self.vy + self.r >= 600) or (self.y +self.vy + self.r <= 0):
            self.vy *= (-1)
        self.x += self.vx
        self.y += self.vy

#Класс бомб
class Bombs:
    def __init__(self):
        self.x=random.randint(10, 790)
        self.y=random.randint(0, 200)
        self.color = BLACK
        self.r = 8
        self.live=1
        self.points=0
        self.vx = 0
        self.vy = 2

    def new_bomb(self):
        #Создание новой мишени.
        a = random.randint(10, 790)
        self.x = a
        b = random.randint(0, 200)
        self.y = b
        self.r = 8
        self.color = BLACK
        self.live = 1

    def draw(self):
        #Как я понимаю
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        
    #Движение ,бомб: скорости и перемещения + столкновения
    def speed_bomb(self):
        if POINTS<=6:
            self.vx = 0
            self.vy = 0
        else:
            self.vy+=20
        
    def moving_bomb(self):
        #Условие на детонацию от пола.
        if (self.y + self.vy + self.r >= 600):
            self.vy *= (-1)
        self.y += self.vy

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target(random.choice(GAME_COLORS))
target2 = Target(random.choice(GAME_COLORS))
bomba = Bombs()
finished = False
k=0
POWERATACK = 0
while not finished:
    screen.fill(WHITE)
    gun.draw()
    target1.draw()
    if POINTS>=2:
        target2.draw()
    if POINTS>=5 and target1.vx == 0 and target1.vy == 0:
        target1.speed_target()
    if POINTS>=5 and target2.vx == 0 and target2.vy == 0:
        target2.speed_target()
    if POINTS>=8:
        bomba.draw()
    SCORE()
    for b in balls:
        b.draw()
    pygame.display.update()
    clock.tick(FPS)
    #Для клавиш движения танка
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
            
        #Мощная атака
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            POINTS -= 3
            POWERATACK = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
            if POWERATACK==1 and b.x<=700 and b.y<=500:
                b.vx *= 10
                b.vy *= 10
                b.live += 20
                POWERATACK = 0
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        #Движение влево и вправо
        if keys[pygame.K_a]:
            gun.move_tank_left()
        if keys[pygame.K_d]:
            gun.move_tank_right()

            
    target1.moving_target()
    target2.moving_target()
    bomba.moving_bomb()
    for b in balls:
        if POWERATACK==1 and b.x<=700 and b.y<=500:
            b.vx *= 10
            b.vy *= 10
            b.live += 20
            POWERATACK = 0
        b.move()
        if b.hittest(target1) and target1.live:
            target1.live = 0
            hit()
            target1.new_target()
        if b.hittest(target2) and target2.live:
            target2.live = 0
            hit()
            target2.new_target()
        if b.hittest(bomba):
            bomba.live = 0
            hit()
            bomba.new_bomb()
        if bomba.y >=590:
            POINTS -= 1
            bomba.live = 0
            bomba.new_bomb()
    gun.power_up()

pygame.quit()

