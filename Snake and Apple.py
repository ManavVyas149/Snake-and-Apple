import random
import pygame

pygame.mixer.init()
pygame.init()


#Color
white = (255, 0, 139)
red = (255, 0, 0)
black = (0, 225, 139)
Black = (0, 0, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
green = (0, 200, 0)
Red = (200, 0, 0)
cyan = (0, 255, 255)



#Creating window
screen_width = 1280
screen_height = 720
gameWindow = pygame.display.set_mode((screen_width, screen_height))


#Background Image
intro = pygame.image.load("welcome.png")
intro = pygame.transform.scale(intro, (screen_width, screen_height)).convert_alpha()
mid = pygame.image.load("gamescreen.jpg")
mid = pygame.transform.scale(mid, (screen_width, screen_height)).convert_alpha()
outro = pygame.image.load("endgame.png")
outro = pygame.transform.scale(outro, (screen_width, screen_height)).convert_alpha()
food = pygame.image.load("apple.png")
food = pygame.transform.scale(food, (30, 30)).convert_alpha()


#Game Title
pygame.display.set_caption("Draco Incursion")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_objects(text, font):
   textSurface = font.render(text, True, cyan)
   return textSurface, textSurface.get_rect()

def button(msg, x, y, w, h, ic, ac, action=None):
   mouse = pygame.mouse.get_pos()
   click = pygame.mouse.get_pressed()

   if x + w > mouse[0] > x and y + h > mouse[1] > y:
       pygame.draw.rect(gameWindow, ac, (x, y, w, h))
       if click[0] == 1 and action != None:
           action()
   else:
       pygame.draw.rect(gameWindow, ic, (x, y, w, h))
   smallText = pygame.font.SysFont("lucidabright", 20)
   textSurf, textRect = text_objects(msg, smallText)
   textRect.center = ((x + (w / 2)), (y + (h / 2)))
   gameWindow.blit(textSurf, textRect)

def quitgame():
   pygame.quit()
   quit()


def unpause():
   global pause
   pygame.mixer.music.unpause()
   pause = False

def text_screen(text, color, x, y):
   screen_text = font.render(text, True, color)
   gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snake_list, snake_size):
   for x,y in snake_list:
       pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def paused():
   pygame.mixer.music.pause()
   largeText = pygame.font.SysFont("lucidabright", 115)
   TextSurf, TextRect = text_objects("Paused", largeText)
   TextRect.center = ((640), (300))
   gameWindow.blit(TextSurf, TextRect)

   while pause:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               quit()

       button("Continue", 380, 500, 200, 50, green, bright_green, unpause)
       button("Quit", 700, 500, 200, 50, Red, bright_red, quitgame)

       pygame.display.update()
       clock.tick(60)

def welcome():
   exit_game = False
   while not exit_game:
       gameWindow.fill((233,210,0))
       gameWindow.blit(intro, (0, 0))
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               exit_game = True
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE:
                   pygame.mixer.music.load('Back.mp3')
                   pygame.mixer.music.play()
                   pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.7)
                   gameloop()
       pygame.display.update()
       clock.tick(60)


#Game Loop
def gameloop():
   # Game specific variables
   global pause
   pygame.mixer.music.load('Back.mp3')
   pygame.mixer.music.play(-1)
   x = (screen_width * 0.5)
   y = (screen_height * 1)
   x_change = 0
   exit_game = False
   game_over = False
   snake_x = 55
   snake_y = 69
   velocity_x = 0
   velocity_y = 0
   snake_list = []
   snake_length = 1
   with open("highscore.txt", "r") as f:
           highscore = f.read()
   food_x = random.randint(75, screen_width / 2)
   food_y = random.randint(75, screen_height / 2)
   score = 0
   init_velocity = 5
   snake_size = 30
   fps = 60
   while not exit_game:
       if game_over:
           with open("highscore.txt", "w") as f:
               f.write(str(highscore))
           gameWindow.fill(white)
           gameWindow.blit(outro, (0, 0))
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   exit_game = True

               if event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_RETURN:
                       gameloop()
       else:
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   exit_game = True

               if event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                       velocity_x = init_velocity
                       velocity_y = 0
                   if event.key == pygame.K_p:
                       pause = True
                       paused()

                   if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                       velocity_x = -init_velocity
                       velocity_y = 0

                   if event.key == pygame.K_UP or event.key == pygame.K_w:
                       velocity_y = -init_velocity
                       velocity_x = 0

                   if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                       velocity_y = init_velocity
                       velocity_x = 0

                   if event.key == pygame.K_q:
                       score += 10

           snake_x = snake_x + velocity_x
           snake_y = snake_y + velocity_y

           if abs(snake_x-food_x)<12 and abs(snake_y-food_y)<12:
               score += 10
               pygame.mixer.music.load('Effect.mp3')
               pygame.mixer.music.play()

               food_x = random.randint(170, screen_width)
               food_y = random.randint(170, screen_height)
               snake_length += 5
               if score > int(highscore):
                   highscore = score

           gameWindow.fill(white)
           gameWindow.blit(mid, (0, 0))
           gameWindow.blit(food, (food_x, food_y))
           text_screen("Score: " + str(score) + "  Highscore: " + str(highscore), red, 5, 5)

           head = []
           head.append(snake_x)
           head.append(snake_y)
           snake_list.append(head)

           if len(snake_list)>snake_length:
               del snake_list[0]

           if head in snake_list[:-1]:
               game_over = True
               pygame.mixer.music.load('gover.mp3')
               pygame.mixer.music.play()

           if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_width:
               game_over = True
               pygame.mixer.music.load('gover.mp3')
               pygame.mixer.music.play()
               pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.6)
           pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
           plot_snake(gameWindow, black, snake_list, snake_size)
       pygame.display.update()
       clock.tick(fps)


   pygame.quit()
   quit()
welcome()
