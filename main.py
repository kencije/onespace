import pygame

pygame.init()

SKÄRMENS_BREDD = 1000
SKÄRMENS_HÖJD = 1000

skärm = pygame.display.set_mode((SKÄRMENS_BREDD, SKÄRMENS_HÖJD))

pygame.display.set_caption("Onespace")

original_bild = pygame.image.load("assets/sprites/dababy.png")
sprite_spelare = pygame.transform.scale(original_bild, (original_bild.get_width() // 2, original_bild.get_height() // 2))

spelare_x = SKÄRMENS_BREDD // 2 - 120
spelare_y = SKÄRMENS_HÖJD - 200
spelarens_hastighet = 5

sprite_skott = pygame.image.load("assets/sprites/bullet.png")
skott_lista = []

spelet_körs = True
while spelet_körs:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spelet_körs = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                skott_rect = sprite_skott.get_rect(center=(spelare_x + sprite_spelare.get_width() // 2, spelare_y))
                skott_lista.append(skott_rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spelare_x > 0:
        spelare_x -= spelarens_hastighet
    if keys[pygame.K_RIGHT] and spelare_x < SKÄRMENS_BREDD - sprite_spelare.get_width():
        spelare_x += spelarens_hastighet
    if keys[pygame.K_UP] and spelare_y > 0:
        spelare_y -= spelarens_hastighet
    if keys[pygame.K_DOWN] and spelare_y < SKÄRMENS_HÖJD - sprite_spelare.get_height():
        spelare_y += spelarens_hastighet

    skärm.fill((0, 0, 30))
    skärm.blit(sprite_spelare, (spelare_x, spelare_y))

    for skott in skott_lista:
        skott.y -= 10
        skärm.blit(sprite_skott, skott)
        if skott.y < 0:
            skott_lista.remove(skott)

    pygame.display.update()







    pygame.mixer.init()

    pygame.mixer.music.load("assets/music/Nami_Theme.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

pygame.quit()