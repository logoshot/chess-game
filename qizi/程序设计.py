import pygame
import sys
import math
import random
from pygame.locals import *
#指定图像文件名称 
pygame.init()
#初始化pygame,为使用硬件做准备
screen = pygame.display.set_mode((1500, 720), 0, 32)
#设置窗口标题
# pygame 初始化
pygame.init()

# 设置背景颜色和线条颜色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)


# 设置直线的坐标
points = [(200, 75), (300, 25), (400, 75)]

# 设置背景框大小
size = width, height = 1500, 720
# position = width // 2, height // 2

# 设置帧率，返回clock 类
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("国际数棋")
background=pygame.image.load("qipan5.jpg")
while True:
    for event in pygame.event.get():
        # 查找关闭窗口事件
        if event.type == QUIT:
            sys.exit()

    # 填充背景色
    #screen.fill(BLACK)
    #画棋盘
    pygame.draw.polygon(screen, BLUE, [(75, 360), (300, 225), (300, 495)], 0)
    pygame.draw.polygon(screen, RED, [(1125, 360), (900, 225), (900, 495)], 0)
    for i in range(0, 8):
        pygame.draw.line(screen,WHITE,(75+i * 75, 360 + i * 45),(600 + i * 75,45+ i * 45), 2)
    for i in range(0, 8):
        pygame.draw.line(screen,WHITE,(75+i * 75, 360 - i * 45),(600 + i * 75,675 - i * 45),2)
    for i in range(0, 7):
        pygame.draw.line(screen,WHITE,(150 + i * 75, 315 - i * 45), (150 + i * 75, 405 + i * 45),2)
    for i in range(0, 6):
        pygame.draw.line(screen,WHITE,(675 + i * 75, 90 + i * 45), (675 + i * 75, 630 - i * 45),2)
    #pygame.draw.rect(screen, RED, (), 0)
    for i in range(0,8):
        for j in range(0,8):
            pygame.draw.circle(screen,WHITE , (75+i*75+j*75,360-i*45+j*45), 25, 0)

    #载入棋子

    x0=pygame.image.load('heiqizi10.png')
    x0=pygame.transform.scale(x0,(50,50))
    screen.blit(x0, (50, 335))
    x1 = pygame.image.load('heiqizi1.png')
    x1 = pygame.transform.scale(x1, (50, 50))
    screen.blit(x1, (275, 200))
    x2 = pygame.image.load('heiqizi2.png')
    x2 = pygame.transform.scale(x2, (50, 50))
    screen.blit(x2, (275, 290))
    x3 = pygame.image.load('heiqizi3.png')
    x3 = pygame.transform.scale(x3, (50, 50))
    screen.blit(x3, (275, 380))
    x4 = pygame.image.load('heiqizi4.png')
    x4 = pygame.transform.scale(x4, (50, 50))
    screen.blit(x4, (275, 470))
    x5 = pygame.image.load('heiqizi5.png')
    x5 = pygame.transform.scale(x5, (50, 50))
    screen.blit(x5, (200, 425))
    x6 = pygame.image.load('heiqizi6.png')
    x6 = pygame.transform.scale(x6, (50, 50))
    screen.blit(x6, (200, 335))
    x7 = pygame.image.load('heiqizi7.png')
    x7 = pygame.transform.scale(x7, (50, 50))
    screen.blit(x7, (200, 245))
    x8 = pygame.image.load('heiqizi8.png')
    x8 = pygame.transform.scale(x8, (50, 50))
    screen.blit(x8, (125, 290))
    x9 = pygame.image.load('heiqizi9.png')
    x9 = pygame.transform.scale(x9, (50, 50))
    screen.blit(x9, (125, 380))
    #红方
    y0 = pygame.image.load('hongqizi10.png')
    y0 = pygame.transform.scale(y0, (50, 50))
    screen.blit(y0, (1100, 335))
    y1 = pygame.image.load('hongqizi1.png')
    y1 = pygame.transform.scale(y1, (50, 50))
    screen.blit(y1, (875, 200))
    y2 = pygame.image.load('hongqizi2.png')
    y2 = pygame.transform.scale(y2, (50, 50))
    screen.blit(y2, (875, 290))
    y3 = pygame.image.load('hongqizi3.png')
    y3 = pygame.transform.scale(y3, (50, 50))
    screen.blit(y3, (875, 380))
    y4 = pygame.image.load('hongqizi4.png')
    y4 = pygame.transform.scale(y4, (50, 50))
    screen.blit(y4, (875, 470))
    y5 = pygame.image.load('hongqizi5.png')
    y5 = pygame.transform.scale(y5, (50, 50))
    screen.blit(y5, (950, 425))
    y6 = pygame.image.load('hongqizi6.png')
    y6 = pygame.transform.scale(y6, (50, 50))
    screen.blit(y6, (950, 335))
    y7 = pygame.image.load('hongqizi7.png')
    y7 = pygame.transform.scale(y7, (50, 50))
    screen.blit(y7, (950, 245))
    y8 = pygame.image.load('hongqizi8.png')
    y8 = pygame.transform.scale(y8, (50, 50))
    screen.blit(y8, (1025, 290))
    y9 = pygame.image.load('hongqizi9.png')
    y9 = pygame.transform.scale(y9, (50, 50))
    screen.blit(y9, (1025, 380))
    # 刷新图s
    pygame.display.update()

    clock.tick(60)
