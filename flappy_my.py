import pygame
import os
import random

#configuração da tela de jogo
screen_width = 500
screen_height = 800

#pygame.transform.scale2x() aumenta a imagem por 2x // pygame.image.load('filename') carrega imagens // os.path.join('foldername', 'filename') trás im,agens de outra pasta
pipe = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png'))) 
ground = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
background = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
bird_poses = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]
#bird_poses precisa ser lista pois são varias imagens que constituem a personagem

pygame.font.init()
score_font = pygame.font.SysFont('georgia', 50) #pygame.font.SysFont('fontname', size) utiliza uma lista prórpia de fontes para fontes personalizadas salvar o arquivo da fonte como .ttf e utilizar o comando pygame.font.Font('Filepath", size)
