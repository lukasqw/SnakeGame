import pygame, random2
from pygame.locals import *

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
SCREEN_WITH = 800
SCREEN_HEIGHT = 800
SIZE_SNAKE = 40
GAME_TYPE = 'last_col' # firt_col | last_col 
POWER_UP_TIME = 30

pygame.init()
pygame.display.set_caption('Snake')
screen = pygame.display.set_mode((SCREEN_WITH, SCREEN_HEIGHT))

class Game:
    def __init__(self):
        self.type = GAME_TYPE
        self.running = False
        self.game_over = False

    def setRunning(self, state):
        self.running = state
    
    def setGameOver(self, state):
        self.game_over = state

class Snake:
    def __init__(self):
        self.name = 'snake'
        self.powerUp = False
        self.powerUpTime = 0
        self.skin = pygame.Surface((SIZE_SNAKE, SIZE_SNAKE))
        self.color = (255,255,255)
        self.body = []
        self.bodyLength = 3
        self.generete_body_length(200)
        self.score = 0
        self.score_position = (SCREEN_HEIGHT - 100, 10)
        self.skin.fill(self.color)
        self.controls = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
        self.direction = LEFT

    def init(self,color, bodyLength, controls, name, x):
        self.name = name
        self.color = color
        self.skin.fill(self.color)
        self.bodyLength = bodyLength
        self.generete_body_length(x)
        self.controls = controls

    def generete_body_length(self, x):
        self.body = []
        for i in range(self.bodyLength):
            self.body.insert(i, (x + (SIZE_SNAKE * i), 200))

    def collision(self, snakes):
        if self.body[0][0] == SCREEN_WITH or self.body[0][1] == SCREEN_HEIGHT or self.body[0][0] < 0 or self.body[0][1] < 0:
            return True

        if GAME_TYPE == 'firt_col':
            for i in range(1, len(self.body) -1):
                if self.body[0][0] == self.body[i][0] and self.body[0][1] == self.body[i][1]:
                    return True

        if GAME_TYPE == 'last_col':
            for i in range(snakes.__len__()):
                currentSnake = snakes[i]
                for x in range(1, len(currentSnake.body) -1):
                    if currentSnake.powerUp == True and self.name != currentSnake.name:
               
                        if self.body[0][0] == currentSnake.body[x][0] and self.body[0][1] == currentSnake.body[x][1]:
                            return True

            if self.powerUp == False:
                for i in range(1, len(self.body) -1):
                    if self.body[0][0] == self.body[i][0] and self.body[0][1] == self.body[i][1]:
                        return True

        return False
    
    def collisionApple(self,c1, c2):
        return (c1[0] == c2[0]) and (c1[1] == c2[1])
    
    def collisionStar(self,c1, c2):
        return (c1[0] == c2[0]) and (c1[1] == c2[1])

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = (self.body[i - 1][0], self.body[i - 1][1])

        if self.direction == UP:
            self.body[0] = (self.body[0][0], self.body[0][1] - SIZE_SNAKE) 
        if self.direction == DOWN:
            self.body[0] = (self.body[0][0], self.body[0][1] + SIZE_SNAKE)
        if self.direction == RIGHT:
            self.body[0] = (self.body[0][0] + SIZE_SNAKE, self.body[0][1])
        if self.direction == LEFT:
            self.body[0] = (self.body[0][0] - SIZE_SNAKE, self.body[0][1])

    def render_body(self):
        for pos in self.body:
            #RandomColor
            if self.powerUp:
                self.skin.fill((random2.randint(0,255),random2.randint(0,255),random2.randint(0,255)))
            screen.blit(self.skin, pos)

        if self.powerUp:
            self.powerUpTime = self.powerUpTime + 1

            if self.powerUpTime > POWER_UP_TIME:
                self.powerUp = False
                self.powerUpTime = 0
                self.skin.fill(self.color)

    def addScore(self):
        self.score = self.score + 1
        self.render_score()

    def render_score(self):
        font = pygame.font.Font('freesansbold.ttf', 18)
        score_font = font.render('Score: %s' % (self.score), True, (255,255,255, 0.5))
        score_rect = score_font.get_rect()
        score_rect.topleft = self.score_position
        screen.blit(score_font, score_rect)

class Apple:
    def __init__(self):
        self.pos = self.on_grid_random()
        self.apple = pygame.Surface((SIZE_SNAKE, SIZE_SNAKE))
        self.apple.fill((255,0,0))

    def on_grid_random(self):
        x = (random2.randint(0,(SCREEN_WITH - SIZE_SNAKE)))
        y = (random2.randint(0,(SCREEN_HEIGHT - SIZE_SNAKE)))
        return (x//SIZE_SNAKE * SIZE_SNAKE, y//SIZE_SNAKE * SIZE_SNAKE)
    
    def render_screen(self):
        screen.blit(self.apple, self.pos)

class Star:
    def __init__(self):
        self.pos = self.on_grid_random()
        self.star = pygame.Surface((SIZE_SNAKE, SIZE_SNAKE))
        self.star.fill((0,255,0))

    def on_grid_random(self):
        x = (random2.randint(0,(SCREEN_WITH - SIZE_SNAKE)))
        y = (random2.randint(0,(SCREEN_HEIGHT - SIZE_SNAKE)))
        return (x//SIZE_SNAKE * SIZE_SNAKE, y//SIZE_SNAKE * SIZE_SNAKE)
    
    def render_screen(self):
        screen.blit(self.star, self.pos)

class Screen_grid:
    def generete_grid(self):
        for x in range(0, SCREEN_WITH, SIZE_SNAKE):
            pygame.draw.line(screen, (80,80,80), (x, 0), (x, SCREEN_HEIGHT))
            for Y in range(0, SCREEN_HEIGHT, SIZE_SNAKE):
                pygame.draw.line(screen, (80,80,80), (0, Y), (SCREEN_WITH, Y))

def snakes_move(snakes, key):
    for i in range(snakes.__len__()):
        currentSnake = snakes[i]

        if key == currentSnake.controls[0] and not currentSnake.direction == DOWN:
            currentSnake.direction = UP
        if key == currentSnake.controls[1] and not currentSnake.direction == UP:
            currentSnake.direction = DOWN
        if key == currentSnake.controls[2] and not currentSnake.direction == RIGHT:
            currentSnake.direction = LEFT
        if key == currentSnake.controls[3] and not currentSnake.direction == RIGHT:
            currentSnake.direction = RIGHT

def render_apples(apples):
    for x in range(apples.__len__()):
        apples[x].render_screen()

def render_stars(stars):
    for x in range(stars.__len__()):
        stars[x].render_screen()

def show_game_over(winner, game):
    while True:
        #Font Game Over
        game_over_font = pygame.font.Font('freesansbold.ttf', 60)
        game_over_screen = game_over_font.render('Game Over', True, (255,255,255))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (SCREEN_WITH / 2, SCREEN_HEIGHT / 3)
        screen.blit(game_over_screen, game_over_rect)

        #Font Winner
        game_over_font = pygame.font.Font('freesansbold.ttf', 15)
        game_over_screen = game_over_font.render('Winner ' + str(winner.name) + " | Score: " + str(winner.score), True, (255,255,255))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (SCREEN_WITH / 2, (SCREEN_HEIGHT / 3) + 65)
        screen.blit(game_over_screen, game_over_rect)

        #Font Restart
        game_over_font = pygame.font.Font('freesansbold.ttf', 15)
        game_over_screen = game_over_font.render('Press to Enter to Restart', True, (255,255,255))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (SCREEN_WITH / 2, (SCREEN_HEIGHT / 3) + 85)
        screen.blit(game_over_screen, game_over_rect)

        pygame.display.update()
        pygame.time.wait(500)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

                if event.type == KEYDOWN:
                    if event.key == 13:
                        game.setGameOver(False)
                        main(game)

def show_game_start(game):
    while True:
        #Font Snake
        game_over_font = pygame.font.Font('freesansbold.ttf', 60)
        game_over_screen = game_over_font.render('Snake Game', True, (255,255,255))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (SCREEN_WITH / 2,( SCREEN_HEIGHT / 3) + 20)
        screen.blit(game_over_screen, game_over_rect)

        #Font Start
        game_over_font = pygame.font.Font('freesansbold.ttf', 15)
        game_over_screen = game_over_font.render('Press to Enter to Start', True, (255,255,255))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (SCREEN_WITH / 2, (SCREEN_HEIGHT / 3) + 85)
        screen.blit(game_over_screen, game_over_rect)

        pygame.display.update()
        pygame.time.wait(500)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

                if event.type == KEYDOWN:
                    if event.key == 13:
                        game.setRunning(True)
                        main(game)

def main(game):
    #grid
    screen_grid = Screen_grid()
    if game.running:
        # INIT
        clock = pygame.time.Clock()
        snakes = []
        apples = []
        stars  = []
        
        #snake 1
        snake1 = Snake()
        snake1.init((0,255,0), 3, [K_UP, K_DOWN, K_LEFT, K_RIGHT], 'Snake1', 200)
        snake1.score_position = (0, 0)
        snakes.append(snake1)

        #apple1
        apple1 = Apple()
        apples.append(apple1)

    if not game.running:
        show_game_start(game)


    while not game.game_over and game.running:
        clock.tick(9)
        
        screen.fill((0,0,0))
        screen_grid.generete_grid()

        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                
                if event.type == KEYDOWN:
                    snakes_move(snakes, event.key)
                    
        
        for i in range(snakes.__len__()):
            currentSnake = snakes[i]
            
            for x in range(apples.__len__()):
                currentApple = apples[x]
                if currentSnake.collisionApple(currentSnake.body[0], currentApple.pos):
                    currentApple.pos = currentApple.on_grid_random()
                    currentSnake.body.append((0,0))
                    currentSnake.addScore()
            
            for x in range(stars.__len__()):
                currentStar = stars[x]
                if currentSnake.collisionStar(currentSnake.body[0], currentStar.pos):
                    currentStar.pos = currentStar.on_grid_random()
                    currentSnake.powerUp = True

            if currentSnake.collision(snakes):
                if game.type == 'firt_col':
                    winner = None
                    for x in range(snakes.__len__()):
                        currSnake = snakes[x]
                        if winner is None:
                            winner = currSnake
                        if winner is not None and winner.score < currSnake.score:
                            winner = currSnake
                        
                    show_game_over(winner, game)

                if game.type == 'last_col':
                    if snakes.__len__() > 1:
                        snakes.remove(currentSnake)

                    else:
                        show_game_over(currentSnake, game)
                    
                break

            currentSnake.move()

            render_apples(apples)
            render_stars(stars)

            currentSnake.render_body()
            currentSnake.render_score()

        pygame.display.update()

game = Game()
main(game)



                    