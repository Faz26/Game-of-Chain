import pygame
import time
import random
from pygame.locals import *    


SIZE = 50
BACKGROUND_COLOR = (252,107,3)

class Person:
    def __init__(self, parent_screen,):
        
        self.parent_screen = parent_screen
        self.block = pygame.image.load("pygame project/resources/person.png").convert()
        self.x = SIZE*(5)
        self.y = 40

    def draw(self):
        self.parent_screen.blit(self.block,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,9)*SIZE
        self.y = random.randint(1,9)*SIZE


        
class Chain:

    def __init__(self, parent_screen, LENGTH):
        self.LENGTH = LENGTH
        self.parent_screen = parent_screen
        self.block = pygame.image.load("pygame project/resources/person.png").convert()
        self.x = [0]*LENGTH
        self.y = [0]*LENGTH
        self.direction = 'down'
    
    def increase_length(self):
        self.LENGTH += 1
        self.x.append(-1)
        self.y.append(-1)

    

    def draw(self):
        

        for i in range(self.LENGTH):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
            pygame.display.flip()

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_right(self):
        self.direction = 'right'

    def move_left(self):
        self.direction = 'left'

    def walk(self):
        
        # if self.x[0]>500 :
        #     self.x[0] = 0
        # elif self.x[0]<0:
        #     self.x[0] = 500
        # elif self.y[0]>500 :
        #     self.y[0] = 0
        # elif self.y[0]<0:
        #     self.y[0] = 500

        for i in range(self.LENGTH-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        
        
        
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((500,500))
        self.surface.fill((252,107,3))
        self.chain = Chain(self.surface, 1)
        self.chain.draw()
        self.person = Person(self.surface)
        self.person.draw()

    # x1,y1 for chain, x2,y2 for person   
    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

    '''def out_of_bounds(self,x1,y1):
        if x1 > 500 and x1 < 0:
            self.chain.displace_x(x1)
        if y1 > 500 and y1 < 0:
            self.chain.displace_y(y1)
    '''    
    
    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f"pygame project/resources/{sound}.wav")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg1 = pygame.image.load("pygame project/resources/bg1.jpg")
        self.surface.blit(bg1,(0,0))

    def play(self):
        
        self.render_background()
        self.chain.walk()
        self.person.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.chain.x[0], self.chain.y[0], self.person.x, self.person.y):
            self.play_sound("meet")
            self.chain.increase_length()
            self.person.move()

        if self.chain.x[0]>500 or self.chain.x[0]<0 or self.chain.y[0]>500 or self.chain.y[0]<0:
            self.play_sound("game_over")
            raise "Game Over"
        else:
            for i in range(3,self.chain.LENGTH):
                if self.is_collision(self.chain.x[0], self.chain.y[0], self.chain.x[i], self.chain.y[i]):
                    self.play_sound("meet")
                    self.play_sound("game_over")
                    raise "Game Over"
                
                
    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 20)
        line1 = font.render(f"Score: {self.chain.LENGTH}", True, (255,255,255))
        self.surface.blit(line1, (0,250))
        line2 = font.render("To play again press Enter. To exit press Escape", True, (255,255,255))
        self.surface.blit(line2, (0,280))
        pygame.display.flip()
            

    def display_score(self):
        font = pygame.font.SysFont('arial',20)
        score = font.render(f"Score: {self.chain.LENGTH}", True, (255,255,255))
        self.surface.blit(score, (400,10))

    def reset(self):
        self.chain = Chain(self.surface, 1)
        self.person = Person(self.surface)
    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running =False
                    
                    if event.key == K_RETURN:
                        pause = False

                    if not pause:

                        if event.key == K_UP:
                            self.chain.move_up()
                        if event.key == K_DOWN:
                            self.chain.move_down()
                        if event.key == K_RIGHT:
                            self.chain.move_right()
                        if event.key == K_LEFT:
                            self.chain.move_left()


                elif event.type == QUIT:
                    running = False
            
            try:
                if not pause:
                    self.play()
                
            except Exception as e:
                print(e)
                self.show_game_over()
                pause = True
                self.reset()


            time.sleep(0.15)


        
if __name__ == "__main__":
    game = Game()
    game.run()

    

    