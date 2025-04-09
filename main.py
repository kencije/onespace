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

critical_sound = pygame.mixer.Sound("assets/sounds/lets_go2.mp3")
critical_sound.set_volume(0.5)

intro_sound = pygame.mixer.Sound("assets/sounds/intro_dababy.mp3")
intro_sound.set_volume(0.5)

original_bild = pygame.image.load("assets/sprites/dababy.png")
sprite_spelare = pygame.transform.scale(original_bild, (original_bild.get_width() // 2, original_bild.get_height() // 2))

spelare_x = SKÄRMENS_BREDD // 2 - 120
spelare_y = SKÄRMENS_HÖJD - 200
spelarens_hastighet = 4

sprite_skott = pygame.image.load("assets/sprites/bullet.png")
sprite_skott = pygame.transform.scale(sprite_skott, (sprite_skott.get_width() // 2, sprite_skott.get_height() // 2))
skott_lista = []

sprite_bonus = pygame.image.load("assets/sprites/bonus_time.png")
bonus_rect = sprite_bonus.get_rect(center=(random.randint(0, SKÄRMENS_BREDD), random.randint(0, SKÄRMENS_HÖJD)))
bonus_speed_x = random.choice([-2, 2])
bonus_speed_y = random.choice([-2, 2])
bonus_cooldown = 0

sprite_medium = pygame.image.load("assets/sprites/biggie.png")
sprite_medium = pygame.transform.scale(sprite_medium, (sprite_medium.get_width() // 2, sprite_medium.get_height() // 2))

sprite_small = pygame.image.load("assets/sprites/tupac.png")
sprite_small = pygame.transform.scale(sprite_small, (sprite_small.get_width() // 4, sprite_small.get_height() // 4))

background_mörkblå = pygame.image.load("assets/backgrounds/bg.png")
background_stjärnor = pygame.image.load("assets/backgrounds/stars-A.png")

background_y = 0

objekt_lista = []
respawn_queue = []
player_health = 100
player_score = 0

for _ in range(5):
    while True:
        x = random.randint(0, SKÄRMENS_BREDD - sprite_medium.get_width())
        y = random.randint(0, SKÄRMENS_HÖJD - sprite_medium.get_height())
        new_rect = pygame.Rect(x, y, sprite_medium.get_width(), sprite_medium.get_height())
        if not new_rect.colliderect(bonus_rect):
            objekt_lista.append({"rect": new_rect, "type": "medium", "speed_x": random.choice([-2, 2]), "speed_y": random.choice([-2, 2])})
            break

for _ in range(3):
    while True:
        x = random.randint(0, SKÄRMENS_BREDD - sprite_small.get_width())
        y = random.randint(0, SKÄRMENS_HÖJD - sprite_small.get_height())
        new_rect = pygame.Rect(x, y, sprite_small.get_width(), sprite_small.get_height())
        if not new_rect.colliderect(bonus_rect):
            objekt_lista.append({"rect": new_rect, "type": "small", "speed_x": random.choice([-2, 2]), "speed_y": random.choice([-2, 2])})
            break

har_kritisk_träff = False
kritisk_träff_tid = 0

def aktivera_kritisk_träff():
    global har_kritisk_träff, kritisk_träff_tid, bonus_cooldown
    har_kritisk_träff = True
    kritisk_träff_tid = time.time()
    intro_sound.play()
    bonus_cooldown = time.time() + 5

def respawn_asteroids():
    current_time = time.time()
    for asteroid in respawn_queue[:]:
        if current_time >= asteroid["respawn_time"]:
            x = random.randint(0, SKÄRMENS_BREDD - sprite_medium.get_width())
            y = random.randint(0, SKÄRMENS_HÖJD - sprite_medium.get_height())
            new_rect = pygame.Rect(x, y, sprite_medium.get_width(), sprite_medium.get_height())
            if asteroid["type"] == "medium":
                objekt_lista.append({"rect": new_rect, "type": "medium", "speed_x": random.choice([-2, 2]), "speed_y": random.choice([-2, 2])})
            elif asteroid["type"] == "small":
                objekt_lista.append({"rect": new_rect, "type": "small", "speed_x": random.choice([-2, 2]), "speed_y": random.choice([-2, 2])})
            respawn_queue.remove(asteroid)

def draw_health_bar(health):
    pygame.draw.rect(skärm, (255, 0, 0), (10, 10, 200, 20))
    pygame.draw.rect(skärm, (0, 255, 0), (10, 10, max(0, 200 * (health / 100)), 20))

def draw_score(score):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    skärm.blit(score_text, (10, 40))

def game_over_screen():
    font = pygame.font.SysFont(None, 72)
    text = font.render("Game Over! Press 'R' to Restart", True, (255, 0, 0))
    skärm.blit(text, (SKÄRMENS_BREDD // 2 - text.get_width() // 2, SKÄRMENS_HÖJD // 2 - text.get_height() // 2))
    pygame.display.update()

def restart_game():
    global objekt_lista, respawn_queue, player_health, player_score, spelare_x, spelare_y
    objekt_lista = []
    respawn_queue = []
    player_health = 100
    player_score = 0
    spelare_x = SKÄRMENS_BREDD // 2 - 120
    spelare_y = SKÄRMENS_HÖJD - 200
    for _ in range(5):
        while True:
            x = random.randint(0, SKÄRMENS_BREDD - sprite_medium.get_width())
            y = random.randint(0, SKÄRMENS_HÖJD - sprite_medium.get_height())
            new_rect = pygame.Rect(x, y, sprite_medium.get_width(), sprite_medium.get_height())
            if not new_rect.colliderect(bonus_rect):
                objekt_lista.append({"rect": new_rect, "type": "medium", "speed_x": random.choice([-2, 2]), "speed_y": random.choice([-2, 2])})
                break
    for _ in range(3):
        while True:
            x = random.randint(0, SKÄRMENS_BREDD - sprite_small.get_width())
            y = random.randint(0, SKÄRMENS_HÖJD - sprite_small.get_height())
            new_rect = pygame.Rect(x, y, sprite_small.get_width(), sprite_small.get_height())
            if not new_rect.colliderect(bonus_rect):
                objekt_lista.append({"rect": new_rect, "type": "small", "speed_x": random.choice([-2, 2]), "speed_y": random.choice([-2, 2])})
                break

spelet_körs = True
while spelet_körs:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spelet_körs = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if har_kritisk_träff and time.time() - kritisk_träff_tid < 10:
                    for i in range(-2, 3):
                        skott_rect = pygame.Rect(
                            spelare_x + sprite_spelare.get_width() // 2 + i * 15,
                            spelare_y,
                            sprite_skott.get_width(),
                            sprite_skott.get_height(),
                        )
                        skott_lista.append(skott_rect)
                    critical_sound.play()
                else:
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

    if player_health <= 0:
        game_over_screen()
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spelare_x > 0:
        spelare_x -= spelarens_hastighet
    if keys[pygame.K_RIGHT] and spelare_x < SKÄRMENS_BREDD - sprite_spelare.get_width():
        spelare_x += spelarens_hastighet
    if keys[pygame.K_UP] and spelare_y > 0:
        spelare_y -= spelarens_hastighet
    if keys[pygame.K_DOWN] and spelare_y < SKÄRMENS_HÖJD - sprite_spelare.get_height():
        spelare_y += spelarens_hastighet

    if sprite_spelare.get_rect(topleft=(spelare_x, spelare_y)).colliderect(bonus_rect):
        aktivera_kritisk_träff()
        bonus_rect.topleft = (-100, -100)

    if time.time() > bonus_cooldown and bonus_rect.topleft == (-100, -100):
        bonus_rect.topleft = (random.randint(0, SKÄRMENS_BREDD), random.randint(0, SKÄRMENS_HÖJD))
        bonus_speed_x = random.choice([-2, 2])
        bonus_speed_y = random.choice([-2, 2])

    bonus_rect.x += bonus_speed_x
    bonus_rect.y += bonus_speed_y

    if bonus_rect.left < 0 or bonus_rect.right > SKÄRMENS_BREDD:
        bonus_speed_x *= -1
    if bonus_rect.top < 0 or bonus_rect.bottom > SKÄRMENS_HÖJD:
        bonus_speed_y *= -1

    background_y += 2
    if background_y >= SKÄRMENS_HÖJD:
        background_y = 0

    skärm.blit(background_mörkblå, (0, 0))
    skärm.blit(background_stjärnor, (0, background_y))
    skärm.blit(background_stjärnor, (0, background_y - SKÄRMENS_HÖJD))

    skärm.blit(sprite_spelare, (spelare_x, spelare_y))
    if bonus_rect.topleft != (-100, -100):
        skärm.blit(sprite_bonus, bonus_rect.topleft)

    for obj in objekt_lista[:]:
        obj["rect"].x += obj["speed_x"]
        obj["rect"].y += obj["speed_y"]

        if obj["rect"].left < 0 or obj["rect"].right > SKÄRMENS_BREDD:
            obj["speed_x"] *= -1
        if obj["rect"].top < 0 or obj["rect"].bottom > SKÄRMENS_HÖJD:
            obj["speed_y"] *= -1

        if sprite_spelare.get_rect(topleft=(spelare_x, spelare_y)).colliderect(obj["rect"]):
            player_health -= 10
            objekt_lista.remove(obj)

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
                player_score += 10
                if obj["type"] == "medium":
                    respawn_queue.append({"type": "medium", "respawn_time": time.time() + 3})
                    objekt_lista.remove(obj)
                    for _ in range(2):
                        x = obj["rect"].x + random.randint(-10, 10)
                        y = obj["rect"].y + random.randint(-10, 10)
                        objekt_lista.append({"rect": pygame.Rect(x, y, sprite_small.get_width(), sprite_small.get_height()), "type": "small", "speed_x": random.choice([-2, 2]), "speed_y": random.choice([-2, 2])})
                elif obj["type"] == "small":
                    respawn_queue.append({"type": "small", "respawn_time": time.time() + 3})
                    objekt_lista.remove(obj)
                break
        if skott.y < 0:
            skott_lista.remove(skott)

    respawn_asteroids()

    draw_health_bar(player_health)
    draw_score(player_score)

    pygame.display.update()

pygame.quit()