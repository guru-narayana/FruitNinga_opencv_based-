import pygame
import cv2
import math
from random import randint
cam = cv2.VideoCapture(0)
palm = cv2.CascadeClassifier('D:\\cubed\\palm.xml')
pygame.init()
a = []
myfont = pygame.font.SysFont("monospace", 24)


win = pygame.display.set_mode((400, 200))
bg = pygame.image.load('bg.jpg')
watermelon = [pygame.image.load('watermelon1.png'), pygame.image.load('watermelon2.png'),
              pygame.image.load('watermelon3.png')]
berry = [pygame.image.load('berry1.png'), pygame.image.load('berry2.png'),
              pygame.image.load('berry3.png')]
orange = [pygame.image.load('orang1.png'), pygame.image.load('orang2.png'),
              pygame.image.load('orange3.png')]
star= pygame.image.load('star1.png')
pygame.display.set_caption("Fruit Ninja")
clock = pygame.time.Clock()
class img(object):
    def __init__(self, x, y, pic, u=12, g=-0.4, t=0):
        self.x = x
        self.y = y
        self.pic = pic
        self.u = u
        self.pos = x
        self.g = g
        self.t = t
    def show(self,angle):
        self.angle = angle
        win.blit(pygame.transform.rotate(self.pic, self.angle), (self.x, self.y))
win.blit(bg, (0, 0))
pygame.display.update()
vx = 0
vy = 0
run = True
angle = 0
x = []
score = 0
while run:
    ret, frame = cam.read()
    correct = cv2.flip(frame, 1)
    gray = cv2.cvtColor(correct, cv2.COLOR_BGR2GRAY)
    palmcord = palm.detectMultiScale(gray, 1.3, 5)
    for (p, q, r, s) in palmcord:
        centery = (2 * q + s) / 2
        centerx = (2 * p + r) / 2
        cv2.rectangle(correct, (p, q), (p + r, q + s), (0, 255, 0), 2)
        vy = int((centery / 480) * 200)
        vx = int((centerx / 640) * 400)
    cv2.imshow("output", correct)
    win.blit(star, (vx, vy))
    number = randint(0, 3)
    maskp = pygame.mask.from_surface(star)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if a == x:
        for i in range(number):
            pos = randint(50, 450)
            ypos = randint(200, 240)
            fruit_type = randint(0, 2)

            if fruit_type == 0:
                fruit = watermelon[0]
            if fruit_type == 1:
                fruit = berry[0]
            if fruit_type == 2:
                fruit = orange[0]
            a.append(img(pos, ypos, fruit))

    for z in a:
        z.y = z.y - (z.u*z.t)
        z.u = z.u + (z.g*z.t)
        z.t = z.t + 0.01
        if z.pos <= 200:
            z.x = z.x + 1.3
        if z.pos > 200:
            z.x = z.x - 1.3
        if z.u == 0:
            z.t = 0
        z.show(angle)
        mask = pygame.mask.from_surface(z.pic)
        if not(mask.overlap(maskp,(int(z.x - vx), int(z.y - vy))) == None):

            if z.pic == berry[0] or z.pic == orange[0] or z.pic == watermelon[0]:
                score +=1
                index_value = a.index(z)
                xposition = z.x
                yposition = z.y
                grav = z.g
                vel = z.u
                tim = z.t
                if z.pic == berry[0]:
                    a.append(img(xposition +9, yposition + 9, berry[1], vel, grav, tim))
                    a[index_value] = img(xposition - 9, yposition - 9, berry[2], vel, grav, tim)
                if z.pic == watermelon[0]:
                    a.append(img(xposition + 9, yposition + 9, watermelon[1], vel, grav, tim))
                    a[index_value] = img(xposition - 9, yposition - 9, watermelon[2], vel, grav, tim)
                if z.pic == orange[0]:
                    a.append(img(xposition +9, yposition + 9, orange[1], vel, grav, tim))
                    a[index_value] = img(xposition - 9, yposition - 9, orange[2], vel, grav, tim)
        scoretext = myfont.render("Score = " + str(score), 1, (0, 0, 0))
        win.blit(scoretext, (5, 10))
        if z.y > 241:
            a = []

    pygame.display.update()
    win.blit(bg, (0, 0))


    angle = angle + 1
    if angle == 259:
        angle = 0
    clock.tick(6000)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
pygame.quit()
cv2.destroyAllWindows()
