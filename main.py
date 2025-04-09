import pygame
import random
import time

pygame.init()

SKÄRMENS_BREDD = 1000
SKÄRMENS_HÖJD = 1000

skärm = pygame.display.set_mode((SKÄRMENS_BREDD, SKÄRMENS_HÖJD))
pygame.display.set_caption("Onespace")

pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.load("assets/music/bird.mp3")
pygame.mixer.music.play(-1)

bullet_sound = pygame.mixer.Sound("assets/sounds/yeah.wav")
bullet_sound.set_volume(0.5)

explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.mp3")
explosion_sound.set_volume(0.5)

sprite_spelare = pygame.image.load("assets/sprites/dababy.png")
sprite_spelare = pygame.transform.scale(sprite_spelare, (sprite_spelare.get_width() // 2, sprite_spelare.get_height() // 2))

sprite_explosion = pygame.image.load("assets/sprites/explosion.jpg")
sprite_explosion = pygame.transform.scale(sprite_explosion, (sprite_spelare.get_width(), sprite_spelare.get_height()))

spelare_x = SKÄRMENS_BREDD // 2 - 120
spelare_y = SKÄRMENS_HÖJD - 200
spelarens_hastighet = 4

sprite_skott = pygame.image.load("assets/sprites/bullet.png")
sprite_skott = pygame.transform.scale(sprite_skott, (sprite_skott.get_width() // 2, sprite_skott.get_height() // 2))
skott_lista = []

sprite_medium = pygame.image.load("assets/sprites/biggie.png")
sprite_medium = pygame.transform.scale(sprite_medium, (sprite_medium.get_width() // 2, sprite_medium.get_height() // 2))

sprite_small = pygame.image.load("assets/sprites/tupac.png")
sprite_small = pygame.transform.scale(sprite_small, (sprite_small.get_width() // 4, sprite_small.get_height() // 4))

background_mörkblå = pygame.image.load("assets/backgrounds/bg.png")
background_stjärnor = pygame.image.load("assets/backgrounds/stars-A.png")

background_y = 0

objekt_lista = []
player_score = 0
game_over = False


def spawn_enemy():
    if random.random() < 0.6: 
        x = random.randint(0, SKÄRMENS_BREDD - sprite_medium.get_width())
        y = random.randint(-300, -50)
        new_rect = pygame.Rect(x, y, sprite_medium.get_width(), sprite_medium.get_height())
        objekt_lista.append({"rect": new_rect, "type": "medium", "speed_x": random.choice([-2, 2]), "speed_y": random.randint(2, 4)})
    else: 
        x = random.randint(0, SKÄRMENS_BREDD - sprite_small.get_width())
        y = random.randint(-300, -50) 
        new_rect = pygame.Rect(x, y, sprite_small.get_width(), sprite_small.get_height())
        objekt_lista.append({"rect": new_rect, "type": "small", "speed_x": random.choice([-2, 2]), "speed_y": random.randint(2, 4)})

def draw_score(score):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    skärm.blit(score_text, (10, 10))

def game_over_screen():
    font = pygame.font.SysFont(None, 72)
    text = font.render("you suck lol. /n Press 'R' to Restart", True, (255, 0, 0))
    skärm.blit(text, (SKÄRMENS_BREDD // 2 - text.get_width() // 2, SKÄRMENS_HÖJD // 2 - text.get_height() // 2))
    pygame.display.update()

def restart_game():
    global objekt_lista, player_score, spelare_x, spelare_y, game_over
    objekt_lista = []
    player_score = 0
    spelare_x = SKÄRMENS_BREDD // 2 - 120
    spelare_y = SKÄRMENS_HÖJD - 200
    game_over = False
    for _ in range(3):
        spawn_enemy()

spelet_körs = True
enemy_spawn_timer = 0

while spelet_körs:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spelet_körs = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                skott_rect = pygame.Rect(
                    spelare_x + sprite_spelare.get_width() // 2,
                    spelare_y,
                    sprite_skott.get_width(),
                    sprite_skott.get_height(),
                )
                skott_lista.append(skott_rect)
                bullet_sound.play()
            if event.key == pygame.K_r:
                restart_game()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and spelare_x > 0:
            spelare_x -= spelarens_hastighet
        if keys[pygame.K_RIGHT] and spelare_x < SKÄRMENS_BREDD - sprite_spelare.get_width():
            spelare_x += spelarens_hastighet
        if keys[pygame.K_UP] and spelare_y > 0:
            spelare_y -= spelarens_hastighet
        if keys[pygame.K_DOWN] and spelare_y < SKÄRMENS_HÖJD - sprite_spelare.get_height():
            spelare_y += spelarens_hastighet

    background_y += 2
    if background_y >= SKÄRMENS_HÖJD:
        background_y = 0

    skärm.blit(background_mörkblå, (0, 0))
    skärm.blit(background_stjärnor, (0, background_y))
    skärm.blit(background_stjärnor, (0, background_y - SKÄRMENS_HÖJD))

    if game_over:
        skärm.blit(sprite_explosion, (spelare_x, spelare_y))
        game_over_screen()
        continue
    else:
        skärm.blit(sprite_spelare, (spelare_x, spelare_y))

    if pygame.time.get_ticks() - enemy_spawn_timer > 2000:
        spawn_enemy()
        enemy_spawn_timer = pygame.time.get_ticks()

    for obj in objekt_lista[:]:
        obj["rect"].x += obj["speed_x"]
        obj["rect"].y += obj["speed_y"]

        if obj["rect"].left < 0 or obj["rect"].right > SKÄRMENS_BREDD:
            obj["speed_x"] *= -1
        if obj["rect"].top > SKÄRMENS_HÖJD:
            objekt_lista.remove(obj)

        if sprite_spelare.get_rect(topleft=(spelare_x, spelare_y)).colliderect(obj["rect"]):
            explosion_sound.play()
            game_over = True

        if obj["type"] == "medium":
            skärm.blit(sprite_medium, obj["rect"].topleft)
        elif obj["type"] == "small":
            skärm.blit(sprite_small, obj["rect"].topleft)

    for skott in skott_lista[:]:
        skott.y -= 10
        skärm.blit(sprite_skott, skott)
        for obj in objekt_lista[:]:
            if skott.colliderect(obj["rect"]):
                skott_lista.remove(skott)
                if obj["type"] == "medium":
                    player_score += 2
                    objekt_lista.remove(obj)
                    for _ in range(2):
                        x = obj["rect"].x + random.randint(-10, 10)
                        y = obj["rect"].y + random.randint(-10, 10)
                        objekt_lista.append({"rect": pygame.Rect(x, y, sprite_small.get_width(), sprite_small.get_height()), "type": "small", "speed_x": random.choice([-2, 2]), "speed_y": random.choice([2, 3])})
                elif obj["type"] == "small":
                    player_score += 1
                    objekt_lista.remove(obj)
                break
        if skott.y < 0:
            skott_lista.remove(skott)

    draw_score(player_score)

    pygame.display.update()

pygame.quit()