import pygame
import random

pygame.init()

SKÄRMENS_BREDD = 1000
SKÄRMENS_HÖJD = 700

skärm = pygame.display.set_mode((SKÄRMENS_BREDD, SKÄRMENS_HÖJD))
pygame.display.set_caption("Straightouttaspace")

pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.load("assets/music/bird.mp3")
pygame.mixer.music.play(-1)

bullet_sound = pygame.mixer.Sound("assets/sounds/yeah.wav")
bullet_sound.set_volume(0.5)

explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.mp3")
explosion_sound.set_volume(0.5)

wahwahwah_sound = pygame.mixer.Sound("assets/sounds/wahwahwah.mp3")
wahwahwah_sound.set_volume(0.5)

critical_sound = pygame.mixer.Sound("assets/sounds/lets_go.mp3")
critical_sound.set_volume(0.5)

# Add transformation music
transformation_music = "assets/music/fullpower.mp3"

sprite_spelare = pygame.image.load("assets/sprites/dababy.png")
sprite_spelare = pygame.transform.scale(sprite_spelare, (sprite_spelare.get_width() // 2, sprite_spelare.get_height() // 2))

sprite_explosion = pygame.image.load("assets/sprites/explosion.jpg")
sprite_explosion = pygame.transform.scale(sprite_explosion, (sprite_spelare.get_width(), sprite_spelare.get_height()))

sprite_critical = pygame.image.load("assets/sprites/bonus_time.png")
sprite_critical = pygame.transform.scale(sprite_critical, (50, 50))

boss_sprite = pygame.image.load("assets/sprites/kingvon.jpg")
boss_sprite = pygame.transform.scale(boss_sprite, (400, 300))

# Add final boss sprite
final_boss_sprite = pygame.image.load("assets/sprites/finalvon.png")
final_boss_sprite = pygame.transform.scale(final_boss_sprite, (400, 300))

spelare_x = SKÄRMENS_BREDD // 2 - 120
spelare_y = SKÄRMENS_HÖJD - 200
spelarens_hastighet = 6

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
player_dead = False

critical_rect = None
critical_active = False
critical_timer = 0

boss_active = False
boss_music_played = False
boss_health = 100
boss_x = SKÄRMENS_BREDD // 2 - boss_sprite.get_width() // 2
boss_y = -300
boss_speed_x = 3
boss_visible = False
boss_can_take_damage = False

boss_awoken_text_timer = 0
boss_awoken_text_displayed = False

# Add transformation variables
final_boss_active = False
transformation_timer = 0
final_boss_health = 200  # Double health for the final form

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

def spawn_critical():
    global critical_rect
    if random.random() < 0.01:
        x = random.randint(0, SKÄRMENS_BREDD - sprite_critical.get_width())
        y = random.randint(-300, -50)
        critical_rect = pygame.Rect(x, y, sprite_critical.get_width(), sprite_critical.get_height())

def activate_critical():
    global critical_active, critical_timer
    critical_active = True
    critical_timer = pygame.time.get_ticks()
    critical_sound.play()

def activate_boss_mode():
    global boss_active, objekt_lista, boss_music_played, boss_health, boss_y, boss_visible, boss_can_take_damage
    boss_active = True
    objekt_lista.clear()
    boss_health = 100
    boss_y = -300
    boss_visible = False
    boss_can_take_damage = False
    if not boss_music_played:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/music/entrance.mp3")
        pygame.mixer.music.play(-1)
        boss_music_played = True

def draw_score(score):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    skärm.blit(score_text, (10, 10))

def draw_boss_health(health, max_health, y_offset=0):
    """Draws a health bar for the boss."""
    bar_width = 300
    bar_height = 20
    bar_x = SKÄRMENS_BREDD // 2 - bar_width // 2
    bar_y = boss_y - 30 + y_offset
    health_ratio = health / max_health
    pygame.draw.rect(skärm, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))  # Red background
    pygame.draw.rect(skärm, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))  # Green foreground

def game_over_screen(win):
    font = pygame.font.SysFont(None, 72)
    if win:
        text = font.render("How did you beat him...?", True, (0, 255, 0))
    else:
        text = font.render("lol you suck", True, (255, 0, 0))
    restart_text = font.render("Press 'R' to Restart", True, (255, 255, 255))
    skärm.blit(text, (SKÄRMENS_BREDD // 2 - text.get_width() // 2, SKÄRMENS_HÖJD // 2 - text.get_height() // 2 - 50))
    skärm.blit(restart_text, (SKÄRMENS_BREDD // 2 - restart_text.get_width() // 2, SKÄRMENS_HÖJD // 2 - restart_text.get_height() // 2 + 50))
    pygame.display.update()

def restart_game():
    global objekt_lista, player_score, spelare_x, spelare_y, game_over, player_dead, critical_rect, critical_active, boss_active, boss_music_played, boss_health, boss_y, boss_visible, boss_can_take_damage, final_boss_active, final_boss_health, boss_sprite
    objekt_lista.clear()
    player_score = 0
    spelare_x = SKÄRMENS_BREDD // 2 - 120
    spelare_y = SKÄRMENS_HÖJD - 200
    game_over = False
    player_dead = False
    critical_rect = None
    critical_active = False
    boss_active = False
    boss_music_played = False
    boss_health = 100
    boss_y = -300
    boss_visible = False
    boss_can_take_damage = False
    final_boss_active = False
    final_boss_health = 200

    # Reset King Von's sprite
    boss_sprite = pygame.image.load("assets/sprites/kingvon.jpg")
    boss_sprite = pygame.transform.scale(boss_sprite, (400, 300))

    pygame.mixer.music.load("assets/music/bird.mp3")
    pygame.mixer.music.play(-1)

spelet_körs = True
enemy_spawn_timer = 0

while spelet_körs:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spelet_körs = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                restart_game()
            if event.key == pygame.K_SPACE and not game_over and not player_dead:
                if critical_active:
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

    keys = pygame.key.get_pressed()
    if not game_over and not player_dead:
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
        if player_dead:
            skärm.blit(sprite_explosion, (spelare_x, spelare_y))
        game_over_screen(win=(not player_dead))
        continue

    skärm.blit(sprite_spelare, (spelare_x, spelare_y))

    if boss_active:
        if not boss_awoken_text_displayed:
            boss_awoken_text_timer = pygame.time.get_ticks()
            boss_awoken_text_displayed = True

        if pygame.time.get_ticks() - boss_awoken_text_timer < 2000:
            font = pygame.font.SysFont(None, 72)
            awoken_text = font.render("You have awoken him....", True, (255, 0, 0))
            skärm.blit(awoken_text, (SKÄRMENS_BREDD // 2 - awoken_text.get_width() // 2, SKÄRMENS_HÖJD // 2 - awoken_text.get_height() // 2))
    
        if boss_y < 50:
            boss_y += 1
        else:
            boss_visible = True
            boss_can_take_damage = True

        if boss_visible:
            boss_x += boss_speed_x
            if boss_x <= 0 or boss_x + boss_sprite.get_width() >= SKÄRMENS_BREDD:
                boss_speed_x *= -1

        boss_rect = pygame.Rect(boss_x, boss_y, boss_sprite.get_width(), boss_sprite.get_height())
        skärm.blit(boss_sprite, (boss_x, boss_y))

        player_rect = pygame.Rect(spelare_x, spelare_y, sprite_spelare.get_width(), sprite_spelare.get_height())
        if player_rect.colliderect(boss_rect):
            explosion_sound.play()
            wahwahwah_sound.play()
            pygame.mixer.music.stop()
            game_over = True
            player_dead = True

        if boss_visible:
            draw_boss_health(boss_health, 100)

        for skott in skott_lista[:]:
            skott.y -= 10
            skärm.blit(sprite_skott, skott)
            if boss_can_take_damage and skott.colliderect(boss_rect):
                skott_lista.remove(skott)
                boss_health -= 1
                if boss_health <= 0 and not final_boss_active:
                    boss_speed_x = 0
                    boss_x = SKÄRMENS_BREDD // 2 - boss_sprite.get_width() // 2
                    boss_visible = False
                    boss_can_take_damage = False

                    transformation_timer = pygame.time.get_ticks()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(transformation_music)
                    pygame.mixer.music.play(-1)
                    final_boss_active = True

            if skott.y < 0:
                skott_lista.remove(skott)

    if final_boss_active:
        current_time = pygame.time.get_ticks()
        if current_time - transformation_timer < 2000:
            font = pygame.font.SysFont(None, 72)
            transformation_text = font.render("You have made him mad...", True, (255, 0, 0))
            skärm.blit(transformation_text, (SKÄRMENS_BREDD // 2 - transformation_text.get_width() // 2, SKÄRMENS_HÖJD // 2 - transformation_text.get_height() // 2))
        elif current_time - transformation_timer >= 15000:
            boss_sprite = final_boss_sprite
            boss_visible = True
            boss_can_take_damage = True
            boss_health = final_boss_health
            boss_speed_x = 3 
            draw_boss_health(boss_health, final_boss_health, y_offset=20)
            final_boss_active = False

    if boss_visible and not final_boss_active and boss_health <= 0:
        # Trigger the win screen only when finalvon.png is defeated
        game_over = True
        game_over_screen(win=True)

    spawn_critical()

    if critical_rect:
        critical_rect.y += 3
        skärm.blit(sprite_critical, critical_rect.topleft)
        if critical_rect.top > SKÄRMENS_HÖJD:
            critical_rect = None
            
        player_rect = pygame.Rect(spelare_x, spelare_y, sprite_spelare.get_width(), sprite_spelare.get_height())

        if critical_rect and player_rect.colliderect(critical_rect):
            activate_critical()
            critical_rect = None

    if critical_active and pygame.time.get_ticks() - critical_timer > 3000:
        critical_active = False

    if not boss_active and pygame.time.get_ticks() - enemy_spawn_timer > 2000:
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
            wahwahwah_sound.play()
            pygame.mixer.music.stop()
            game_over = True
            player_dead = True

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
                    player_score += 20
                    objekt_lista.remove(obj)
                    for _ in range(2):
                        x = obj["rect"].x + random.randint(-10, 10)
                        y = obj["rect"].y + random.randint(-10, 10)
                        objekt_lista.append({"rect": pygame.Rect(x, y, sprite_small.get_width(), sprite_small.get_height()), "type": "small", "speed_x": random.choice([-2, 2]), "speed_y": random.choice([2, 3])})
                elif obj["type"] == "small":
                    player_score += 10
                    objekt_lista.remove(obj)
                break
        if skott.y < 0:
            skott_lista.remove(skott)

    if player_score >= 100 and not boss_active:
        activate_boss_mode()

    draw_score(player_score)

    pygame.display.update()

pygame.quit()