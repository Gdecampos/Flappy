import pygame
import os
import random

# configuração da tela de jogo
screen_width = 500
screen_height = 800

# pygame.transform.scale2x() aumenta a imagem por 2x // pygame.image.load('filename') carrega imagens // os.path.join('foldername', 'filename') trás im,agens de outra pasta
pipe_skin = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png'))) 
ground_skin = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
background_skin = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
bird_poses = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]
# bird_poses precisa ser lista pois são varias imagens que constituem a personagem

pygame.font.init()
score_font = pygame.font.SysFont('georgia', 50) #pygame.font.SysFont('fontname', size) utiliza uma lista prórpia de fontes para fontes personalizadas salvar o arquivo da fonte como .ttf e utilizar o comando pygame.font.Font('Filepath", size)

class bird:
    imgs = bird_poses
    
    # animações da rotação
    max_rotation = 25
    rotation_speed = 20
    animation_time = 5
    
    # definindo parametros iniciais do passaro
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.heigt = self.y
        self.time = 0
        self.image_serial = 0
        self.image = imgs[0]
        
    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.heigt = self.y
        
    def move(self):
        # calculo do deslocamento
        self.time += 1
        movement = 1.5 * (self.time**2) + self.speed * self.time # S=Si+V*T+(AT²)/2  // fórmula do sorvetão
        
        # restringir o deslocamento
        if movement > 16:
            movement = 16
        # dá uma vantagem no pulo devido a velocidade de queda
        elif movement < 0:
            movement -=2
        
        # movimentando o passaro
        self.y += movement
        
        #angulo do passaro
        if movement < 0 or self.y < (self.heigt + 50):
            
        
    pass

class pipe:
    pass

class ground:
    pass