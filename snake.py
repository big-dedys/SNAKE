from pygame import *
import random

class GameSprite(sprite.Sprite):
    def __init__(self, color, size, speed, x, y):
        super().__init__()
        self.image = Surface(size)
        self.image.fill(color)
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Snake(GameSprite):
    def __init__(self, color, size, speed, x, y):
        super().__init__(color, size, speed, x, y)
        self.direction = "right"
        self.body = []
        self.speed_increase = 1

    def update(self):
        keys = key.get_pressed()

        if keys[K_UP] and self.rect.y > 5 and self.direction != "down":
            self.direction = "up"
        elif keys[K_DOWN] and self.rect.y < 425 and self.direction != "up":
            self.direction = "down"
        elif keys[K_LEFT] and self.rect.x > 5 and self.direction != "right":
            self.direction = "left"
        elif keys[K_RIGHT] and self.rect.x < 630 and self.direction != "left":
            self.direction = "right"

        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

            self.check_collision()

        if sprite.collide_rect(self, apple):
            apple.respawn()
            self.speed += self.speed_increase

    def check_collision(self):
        self.rect.x <= 0 or self.rect.x >= 680 or self.rect.y <= 0 or self.rect.y >= 380

class Apple(GameSprite):
    def init(self, color, size, x, y):
        super().init(color, size, 0, x, y)

    def respawn(self):
        self.rect.x = random.randint(20, 680)
        self.rect.y = random.randint(20, 380)

blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

window_size = (600, 400)

FPS = 60
clock = time.Clock()

window = display.set_mode((700, 500))
display.set_caption('Змейка')
background = Surface((800, 500))
background.fill((0, 0, 0))

snake_color = green
snake_size = (20, 20)

apple_color = red
apple_size = (20, 20)

snake = Snake(snake_color, snake_size, 1, 300, 200)
apple = Apple(apple_color, apple_size, 1, 100, 100)

font.init()

lose = font.Font(None, 80)
score_font = font.Font(None, 36)

game = True
game_over = False

score = 0

while not game_over:
    window.blit(background, (0, 0))

    for e in event.get():
        if e.type == QUIT:
            game_over = True

    if snake.check_collision():
        text = lose.render("You lose", True, red)
        text_rect = text.get_rect(center=(250, 250))
        window.blit(text, text_rect)
        game_over = True
    else:
        snake.update()
        snake.reset()
        apple.reset()

        if sprite.collide_rect(snake, apple):
            apple.respawn()
            snake.speed += snake.speed_increase
            score += 1

            score_text = score_font.render("Score: " + str(score), True, (255, 255, 255))
            score_rect = score_text.get_rect()
            score_rect.topleft = (10, 10)
            window.blit(score_text, score_rect)

    clock.tick(FPS)
display.update()



