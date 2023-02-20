import pygame as Pygame

WIDTH = 1200
HEIGHT = 600
OFFSET_MAX = 250

class Game:
    player_1_lives = 5

    player_2_lives = 5

    def __init__(self):

        self.running = False

        self.screen = Pygame.display.set_mode((WIDTH, HEIGHT))

        self.clock = Pygame.time.Clock()

        self.balls = Pygame.sprite.Group()

        self.player_group = Pygame.sprite.Group()
  
        self.player1 = Player(20, HEIGHT // 2, 1)

        self.player2 = Player(WIDTH - 20, HEIGHT // 2, 2)

    
    def run(self):
        self.add_players()
        self.add_ball()

        while self.running:
            events = Pygame.event.get()
            
            if Game.player_1_lives == 0 or Game.player_2_lives == 0:
                self.running = False

            for event in events:
                if event.type == Pygame.QUIT:
                    self.running = False
                    Pygame.quit()
                    exit()
                if event.type == Pygame.KEYDOWN:
                    if event.key == Pygame.K_UP:
                        self.player2.move_up()
                    if event.key == Pygame.K_DOWN:
                        self.player2.move_down()
                    if event.key == Pygame.K_LEFT:
                        self.player2.move_left()
                    if event.key == Pygame.K_RIGHT:
                        self.player2.move_right()

                    if event.key == Pygame.K_w:
                        self.player1.move_up()
                    if event.key == Pygame.K_s:
                        self.player1.move_down()
                    if event.key == Pygame.K_a:
                        self.player1.move_left()
                    if event.key == Pygame.K_d:
                        self.player1.move_right()
            
            self.balls.update()

            self.screen.fill((255, 255, 255))
            self.player_group.draw(self.screen)
            self.balls.draw(self.screen)
            self.show_info()
            Pygame.display.flip()
            self.clock.tick(60)

    def set_running(self, value):
        self.running = value

    def add_players(self):
        self.player_group.add( self.player1 )
        self.player_group.add( self.player2 )

    def add_ball(self):
        self.balls.add(Ball())


    def get_player(self):
        return self.player_group

    def get_balls(self):
        return self.balls

    def show_info(self):
        Pygame.font.init()
        font = Pygame.font.SysFont('arial.ttf', 26)
        player1text = font.render('Player 1 Lives: '+str(Game.player_1_lives), True, (0, 0, 0))
        position = player1text.get_rect()
        position.x = 0
        position.y = 0

        self.screen.blit(player1text, position)

        player2text = font.render('Player 2 Lives: '+str(Game.player_2_lives), True, (0, 0, 0))
        position = player2text.get_rect()
        position.x = WIDTH - 200
        position.y = 0
        self.screen.blit(player2text, position)


class Player(Pygame.sprite.Sprite):

    def __init__(self, x, y, p):
        super().__init__()

        self.speed = 50
        self.p = p
        self.offset = 0

        self.image = Pygame.Surface((10, 100))
        self.image.fill((0,0,0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def move_right(self):
        if self.p == 1:
            if self.offset == OFFSET_MAX:
                pass
            else:
                self.rect.x += 10
                self.offset += 10
        else:
            if self.offset == 0:
                pass
            else:
                self.rect.x += 10
                self.offset -= 10
    
    def move_left(self):
        if self.p == 1:
            if self.offset == 0:
                pass
            else:
                self.rect.x -= 10
                self.offset -= 10
        else:
            if self.offset == OFFSET_MAX:
                pass
            else:
                self.rect.x -= 10
                self.offset += 10

    def move_down(self):
        if self.rect.y <= HEIGHT  and self.rect.y >= 0:
            self.rect.y += self.speed
        
        if self.rect.y > HEIGHT - 100:
            self.rect.y = HEIGHT - 100
            

    def move_up(self):

        if self.rect.y <= HEIGHT and self.rect.y >= 0:
            self.rect.y -= self.speed

        if self.rect.y < 0:
            self.rect.y = 0


class Ball(Pygame.sprite.Sprite):

    player = None

    def __init__(self):
        super().__init__()
        self.velocity = [-3, -3]
        self.image = Pygame.Surface((10,10))
        self.image.fill((255, 255, 255))
        Pygame.draw.circle(self.image, (0, 0, 0), (5, 5), 5)

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT // 2
    
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if self.rect.y <= 0 or self.rect.y >= HEIGHT - 5:
            self.velocity[1] = -self.velocity[1]
        
        if self.rect.x <= 0 or self.rect.x >= WIDTH - 5:
            if self.rect.x >= WIDTH - 5:
                Game.player_2_lives -= 1
                self.velocity[0] = 3
            if self.rect.x <= 0:
                Game.player_1_lives -= 1
                self.velocity[0] = -3
            
            self.rect.x = WIDTH // 2
            self.rect.y = HEIGHT // 2
            
            
        
        collisions = Pygame.sprite.spritecollide(self, Ball.player, False)
        if collisions:
            self.velocity[1] = self.velocity[1]
            self.velocity[0] = -self.velocity[0]
            if self.velocity[0] > 0:
                self.velocity[0] += 1
            else:
                self.velocity[0] -= 1
        

def main():
    game = Game()
    game.set_running(True)
    Ball.player = game.get_player()
    game.run()

if __name__ == '__main__':
    main()