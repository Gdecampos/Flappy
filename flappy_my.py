import pygame
import os
import random

# configuração da tela de jogo
screen_width = 550
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

class Bird:
    imgs = bird_poses
    
    # animações da rotação
    max_rotation = 25
    rotation_speed = 20
    animation_time = 5
    y = 0
    
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
        self.speed = -8 
        self.time = 0
        self.heigt = self.y
        
    def move(self):
        # calculo do deslocamento de queda
        self.time += 1
        movement = 1.3 * (self.time**2) + self.speed * self.time # S=Si+V*T+(AT²)/2  // fórmula do sorvetão
        
        # restringir velocidade de queda
        if movement > 15:
            movement = 15
        # dá uma vantagem no pulo devido a velocidade de queda
        elif movement < 0:
            movement -= 2
        
        # movimentando o passaro para baixo
        self.y += movement
        
        # angulo do passaro
        if movement < 0 or self.y < (self.heigt + 50):
            if self.angle < self.max_rotation:
                self.angle = self.max_rotation
        
        else:
            if self.angle > -90:
                self.angle -= self.rotation_speed
        
    def sketch(self, screen):
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
        return pygame.mask.from_surface(self.image) # pega a mascara do passaro

class Pipe:
    distance = 200 # Define a distancia entre o cano superior e inferior
    speed = 5 # Define velocidade do cano
    
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
        
    def move(self):
        self.x -= self.speed # Movimenta os canos da direita para esquerda (movimento negativo)
        
    def sketch(self, screen):
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

class Ground:
    speed = 5
    ground_width = ground_skin.get_width()
    image = ground_skin
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.ground_width
        
    def move(self):
        # Movimenta o chão da direita para esquerda
        self.x1 -= self.speed
        self.x2 -= self.speed
        
        # Caso um dos chãos chegue ao fim da tela o envia para trás do próximo chão (cria um efeito carrocel)
        if self.x1 + self.ground_width < 0:
            self.x1 = self.x2 + self.ground_width
            
        if self.x2 + self.ground_width < 0:
            self.x2 = self.x1 + self.ground_width
            
    def sketch(self, screen):
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))
        
def screen_sketch(screen, bird, pipes, ground, score):
    screen.blit(background_skin, (0, 0))
    # As funções estão no plural para serem usadas em diversos objetos na tela ao mesmo tempo
    bird.sketch(screen)
        
    for pipe in pipes:
        pipe.sketch(screen)
        
    text = score_font.render(f"{score}", 1, (50,50,50)) 
    screen.blit(text, (screen_width/2  - text.get_width()/2, 10))
    ground.sketch(screen)
    pygame.display.update()
    
def main():
    bird = Bird(200, 350)
    ground = Ground(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((screen_width, screen_height))
    score = 0
    clock = pygame.time.Clock()
    lost = False
    runing = True
    
    while runing:
        clock.tick(30) # .tick define o frame rate 
        # Movimenta os objetos em tela
        if not lost:
            bird.move()
        ground.move()
        
        # Interações com o usuário
        for event in pygame.event.get(): # Verifica se o botão de fechar foi clicado
            if event.type == pygame.QUIT:
                runing = False
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN: # Acionado quando uma tecla for pressionada
                if event.key == pygame.K_SPACE: # Verifica se a tecla pressionada foi o espaço
                    bird.jump()
        
        pipe_add = False
        pipe_remove = []
        for pipe in pipes:           
            pipe.move()  
            
            if pipe.collision(bird):  # Verifica se houve colisão entre o cano e o passaro
                Pipe.speed = 0
                Ground.speed = 0
                Bird.animation_time = 0
                lost = True
                
            if not pipe.trespass and bird.x > pipe.x: # Analisa se o passaro passou do cano
                pipe.trespass = True
                pipe_add = True 
            
            if pipe.x + pipe.upper_pipe.get_width() < 0: # Verifica se o cano já saiu por completo da tela
                pipe_remove.append(pipe) # Adiciona o cano em uma lista para remoção
                
        if pipe_add: # Função para adicionar mais canos
            pipes.append(Pipe(650))     # Adiciona mais uma dupla de canos ao fim da tela     
            if score % 10 == 0 and score != 0: # A cada 10 pontos aumenta a velocidade em 1
                Pipe.speed += 1 
                Ground.speed += 1
            score += 1
            
        for pipe in pipe_remove: # Remove os canos ao chegar ao fim da tela
            pipes.remove(pipe)
        
        if (bird.y + bird.image.get_height()) > ground.y or bird.y < 0:
            Pipe.speed = 0
            Ground.speed = 0
            Bird.animation_time = 0
            lost = True
    
        screen_sketch(screen, bird, pipes, ground, score)
        
if __name__ == '__main__':
    main()