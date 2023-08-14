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
        self.image = self.imgs[0]
        
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
        
        # angulo do passaro
        if movement < 0 or self.y < (self.heigt + 50):
            if self.angle < self.max_rotation:
                self.angle = self.max_rotation
        
        else:
            if self.angle > -90:
                self.angle -= self.rotation_speed
        
    def art(self, screen):
        # definindo a ordem das imagens para animação do bater de asas
        self.image_serial +=1
        
        # asas descendo
        if self.image_serial < self.animation_time:
            self.image = self.imgs[0]
        elif self.image_serial < self.animation_time*2:
            self.image = self.imgs[1]
        elif self.image_serial < self.animation_time*3:
            self.image = self.imgs[2]
            
        # asas subindo
        elif self.image_serial < self.animation_time*4:
            self.image = self.imgs[1]
        elif self.image_serial < self.animation_time*4 + 1:
            self.image = self.imgs[0]
            self.image_serial = 0   # reiniciando a animação para o ponto inicial
        
        # caso pule enquanto cai inicia o bater de asas
        if self.angle <= -80:
            self.image = self.imgs[1]
            self.image_serial = self.animation_time*2 
        
        # exibição do passaro na tela
        rotate_image = pygame.transform.rotate(self.image, self.angle) # faz a imagem girar de acordo com o angulo
        img_center = self.image.get_rect(topleft=(self.x, self.y)).center # define o centro da imagem
        box = rotate_image.get_rect(center=img_center) # get_rect() cria um retangulo 'hit box' em torno da imagem
        screen.blit(rotate_image, box.topleft) # .blit serve para mostrar imagem na tela do pygame

    def get_mask(self):
        pygame.mask.from_surface(self.image) # pega a mascara do passaro

class pipe:
    distance = 200 # Define a distancia entre o cano superior e inferior
    pipe_speed = 5 # Define velocidade do cano
    
    def __init__(self, x):
        self.x = x
        self.height_pipe = 0
        self.upper_position = 0
        self.bottom_position = 0
        self.upper_pipe = pygame.transform.flip(pipe_skin, False, True) # pygame.transform.flip(image_name, X axis[T,F], Y axis[T,F]) gira a imagem 
        self.bottom_pipe = pipe_skin
        self.trespass = False
        self.set_height()
        
    def set_height(self):
        self.height_pipe = random.randrange(50, 450) # random.randrange(min, max) Define um limite no centro da tela para criação dos canos
        self.upper_position = self.height_pipe - self.upper_pipe.get_height() # define o cano para cima a partir do ponto definido no self.height_pipe
        self.bottom_position = self.height_pipe + self.distance # define o cano para baixo a partir do ponto definido no self.height_pipe mais a distancia entre os canos definida na variavel "distance"
        
    def move_pipe(self):
        self.x -= self.pipe_speed # Movimenta os canos da direita para esquerda (movimento negativo)
        
    def draw_pipe(self, screen):
        screen.blit(self.upper_pipe, (self.x, self.upper_position))
        screen.blit(self.bottom_pipe, (self.x, self.bottom_position))
        
    def collision(self, bird):
        bird_mask = bird.get_mask() # Executa a def "get_mask" dentro da class "bird"
        upper_mask = pygame.mask.from_surface(self.upper_pipe) # Pega a mask do cano superior
        bottom_mask = pygame.mask.from_surface(self.bottom_pipe)
        
        # Calculo da distancia entre a mask do passaro e a mask dos canos
        upper_distance = (self.x - bird.x, self.upper_position - round(bird.y)) # Usado round na variavel bird.y pois a posição pode ser de numeros quebrados
        bottom_distance = (self.x - bird.x, self.bottom_position - round(bird.y))
        
        upper_colide = bird_mask.overlap(upper_mask, upper_distance)
        bottom_colide = bird_mask.overlap(bottom_mask, bottom_distance) # A função ".overlap(oobjeto A, objeto B)" averigua se os objetos A e B estão sobrepostos e retorna "True / False"
        
        # Averiguando se ouve colisão com os canos
        if upper_colide or bottom_colide:
            return True
        else:
            return False

class ground:
    pass