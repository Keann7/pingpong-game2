from pygame import *

# ---------- ASSETS ----------
img_back = "bg_dapur.jpg"
img_ball = "egg.png"
img_racket = "racket.png"

mixer.init()
pung_sound = mixer.Sound("pung.mp3")

font.init()
font1 = font.Font(None, 45)
lose1 = font1.render("PLAYER 1 LOSE!", True, (255, 0, 0))
lose2 = font1.render("PLAYER 2 LOSE!", True, (255, 0, 0))

# ---------- GAMESPRITE CLASS ----------
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed_x = player_speed
        self.speed_y = player_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Pantul dari atas dan bawah layar
        if self.rect.top <= 0 or self.rect.bottom >= win_height:
            self.speed_y *= -1

# ---------- PLAYER CLASS ----------
class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed_y
        if keys[K_s] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed_y

    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed_y
        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height - 5:
            self.rect.y += self.speed_y

# ---------- SETTINGS ----------
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Ping-Pong Kartun!")

background = transform.scale(image.load(img_back), (win_width, win_height))

# ---------- OBJECTS ----------
ball = GameSprite(img_ball, 100, 200, 50, 50, 5)
racket_l = Player(img_racket, 20, 180, 80, 90, 5)
racket_r = Player(img_racket, 610, 180, 80, 90, 5)

# ---------- GAME LOOP ----------
clock = time.Clock()
FPS = 60

speed_x = 5
speed_y = 5

finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        window.blit(background, (0, 0))

        ball.rect.x += speed_x
        ball.rect.y += speed_y

        racket_l.update_l()
        racket_r.update_r()

        ball.reset()
        racket_l.reset()
        racket_r.reset()

    # Wall Bounce
    if ball.rect.y > win_height - 50 or ball.rect.y < 0:
        speed_y *= -1
    
    # Racket Bounce
    if sprite.collide_rect(racket_l, ball) or sprite.collide_rect(racket_r, ball):
        speed_x *= -1
        pung_sound.play()

    # Lose Condition
    if ball.rect.x < 0:
        finish = True
        window.blit(lose1, (80, 220))
    
    if ball.rect.x > 700:
        finish = True
        window.blit(lose2, (350, 220))

    display.update()
    clock.tick(FPS)
