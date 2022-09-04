import pygame
from sys import exit
from random import randint, choice
from moviepy.editor import *


# pygame imports
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
slide_sound = pygame.mixer.Sound("graphics/music and video/slide.mp3")
slide_sound.set_volume(0.01)
transition_singleplayer = VideoFileClip("graphics/music and video/transition_video.mp4", audio=False)
transition_multiplayer = VideoFileClip("graphics/music and video/video_transition_2.mp4", audio=False)
default_font = pygame.font.Font("graphics/Thintel.ttf", 120)
name_banner_font = pygame.font.Font("graphics/Thintel.ttf", 250)
name_banner_outline_font = pygame.font.Font("graphics/Thintel.ttf", 256)
high_score_outline_font = pygame.font.Font("graphics/Thintel.ttf", 124)
bg_music = pygame.mixer.Sound("graphics/music and video/bg_music.mp3")
bg_music.play(loops=-1)

# background
background = pygame.image.load("graphics/backgrounds/new_grusel_background.png").convert()
lobby_screen = pygame.image.load("graphics/backgrounds/new_grusel_background_hell2.png").convert()

level1_button = default_font.render("Level 1", False, (106, 62, 35))
level1_rect = level1_button.get_rect(center=(590, 760))
level2_button = default_font.render("Level 2", False, (106, 62, 35))
level2_rect = level2_button.get_rect(center=(970, 760))
level3_button = default_font.render("Level 3", False, (106, 62, 35))
level3_rect = level3_button.get_rect(center=(1300, 760))
singleplayer_button = default_font.render("Singleplayer", False, (106, 62, 35))
singleplayer_rect = singleplayer_button.get_rect(center=(680, 760))
multiplayer_button = default_font.render("Multiplayer", False, (106, 62, 35))
multiplayer_rect = multiplayer_button.get_rect(center=(1230, 760))
name_banner = name_banner_font.render("FOREST RUNNER", False, (255, 255, 0))
name_banner_rect = name_banner.get_rect(center=(955, 200))
name_banner_outline = name_banner_outline_font.render("FOREST RUNNER", False, (0, 0, 0))
name_banner_outline_rect = name_banner_outline.get_rect(center=(955, 201))

timer_start = 0
time_played = 0

# bools
game_active = False
multiplayer = None
multiplayer_selected = False
stone2_spawn = False  # aktiviert, wenn level2 oder level3 selected wurde
level_speed = None
transition_singleplayer_play = False
transition_multiplayer_play = False


class Owl:
    x_pos = 963
    y_pos = 370
    speed = 10
    frame1 = pygame.image.load("graphics/charakter/owl_flys_up.png").convert_alpha()
    frame2 = pygame.image.load("graphics/charakter/owl_flys_down.png").convert_alpha()
    death_frame = pygame.image.load("graphics/charakter/owl_death2.png").convert_alpha()
    liste = [frame1, frame2]
    index = 0
    current_frame = liste[index]
    rect = current_frame.get_rect(midbottom=(x_pos, y_pos))
    bahn_1_x, bahn_2_x, bahn_3_x, bahn_4_x, bahn_5_x = 181, 579, 963, 1348, 1742
    bahn_list = [bahn_1_x, bahn_2_x, bahn_3_x, bahn_4_x, bahn_5_x]
    bahn_list_index = 2
    arrow_key_links = False
    arrow_key_rechts = False
    death = False
    jump = False
    animation_count = 0


class Chicken:
    x_pos = 963
    y_pos = 460
    speed = 10
    frame1 = pygame.image.load("graphics/charakter/chicken_frame1.png").convert_alpha()
    frame2 = pygame.image.load("graphics/charakter/chicken_frame2.png").convert_alpha()
    death_frame = pygame.image.load("graphics/charakter/chicken_death.png").convert_alpha()
    frame1 = pygame.transform.rotozoom(frame1, 0, 0.7)
    frame2 = pygame.transform.rotozoom(frame2, 0, 0.7)
    death_frame = pygame.transform.rotozoom(death_frame, 0, 0.7)
    liste = [frame1, frame2]
    index = 0
    current_frame = liste[index]
    rect = current_frame.get_rect(midbottom=(x_pos, y_pos))
    bahn_1_x, bahn_2_x, bahn_3_x, bahn_4_x, bahn_5_x = 181, 579, 963, 1348, 1742
    bahn_list = [bahn_1_x, bahn_2_x, bahn_3_x, bahn_4_x, bahn_5_x]
    bahn_list_index = 2
    arrow_key_links = False
    arrow_key_rechts = False
    death = False
    jump = False
    animation_count = 0


class Stone:
    spawn_chance1 = 1500
    spawn_chance2 = 5000
    x = x2 = 963
    y = y2 = 1081
    spawn = False
    spawn2 = False
    speed = speed2 = 10
    frame = pygame.image.load("graphics/Stone.png").convert_alpha()
    rect = frame.get_rect(midtop=(x, y))
    rect2 = frame.get_rect(midtop=(x, y))
    bahn_1_x, bahn_2_x, bahn_3_x, bahn_4_x, bahn_5_x = 181, 579, 963, 1348, 1742
    bahn_list = [bahn_1_x, bahn_2_x, bahn_3_x, bahn_4_x, bahn_5_x]


# charakter
character = Owl

# custom events
stone_timer = pygame.USEREVENT + 1
pygame.time.set_timer(stone_timer, randint(Stone.spawn_chance1, Stone.spawn_chance2))

stone_timer2 = pygame.USEREVENT + 2
pygame.time.set_timer(stone_timer2, randint(Stone.spawn_chance1, Stone.spawn_chance2))

while True:
    for event in pygame.event.get():  # anderer quit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:  # esc quit
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        if game_active:
            if event.type == stone_timer:
                Stone.x = choice(Stone.bahn_list)
                Stone.spawn = True

            if event.type == stone_timer2 and stone2_spawn:
                Stone.x2 = choice(Stone.bahn_list)
                Stone.spawn2 = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if Owl.bahn_list_index <= 0:
                        Owl.bahn_list_index = 0
                    else:
                        Owl.x_pos = Owl.bahn_list[Owl.bahn_list_index]
                        Owl.bahn_list_index -= 1
                        Owl.arrow_key_links = True
                        slide_sound.play()

                if event.key == pygame.K_RIGHT:
                    if Owl.bahn_list_index >= 4:
                        Owl.bahn_list_index = 4
                    else:
                        Owl.x_pos = Owl.bahn_list[Owl.bahn_list_index]
                        Owl.bahn_list_index += 1
                        Owl.arrow_key_rechts = True
                        slide_sound.play()

                if event.key == pygame.K_a:
                    if Chicken.bahn_list_index <= 0:
                        Chicken.bahn_list_index = 0
                    else:
                        Chicken.x_pos = Chicken.bahn_list[Chicken.bahn_list_index]
                        Chicken.bahn_list_index -= 1
                        Chicken.arrow_key_links = True
                        slide_sound.play()

                if event.key == pygame.K_d:
                    if Chicken.bahn_list_index >= 4:
                        Chicken.bahn_list_index = 4
                    else:
                        Chicken.x_pos = Chicken.bahn_list[Chicken.bahn_list_index]
                        Chicken.bahn_list_index += 1
                        Chicken.arrow_key_rechts = True
                        slide_sound.play()

                if event.key == pygame.K_w:
                    Chicken.speed = -20
                    Chicken.jump = True

                if event.key == pygame.K_UP:
                    Owl.speed = -20
                    Owl.jump = True

        else:
            screen.blit(lobby_screen, (0, 0))
            screen.blit(name_banner_outline, name_banner_outline_rect)
            screen.blit(name_banner, name_banner_rect)
            mouse_pos = pygame.mouse.get_pos()

            high_score_txt = open("high score.txt", "r")
            read_it = high_score_txt.read()
            if time_played > int(read_it):
                read_it = time_played
            high_score_banner = default_font.render("High Score: " + str(read_it), False, (255, 255, 0))
            high_score_banner_rect = high_score_banner.get_rect(center=(955, 420))
            high_score_banner_outline = high_score_outline_font.render("High Score: " + str(read_it), False, (0, 0, 0))
            high_score_banner_outline_rect = high_score_banner_outline.get_rect(center=(955, 421))
            high_score_txt.close()
            screen.blit(high_score_banner_outline, high_score_banner_outline_rect)
            screen.blit(high_score_banner, high_score_banner_rect)
            high_score_txt = open("high score.txt", "w")
            high_score_txt.write(str(read_it))
            high_score_txt.close()

            if not multiplayer_selected:
                screen.blit(singleplayer_button, singleplayer_rect)
                screen.blit(multiplayer_button, multiplayer_rect)

                if singleplayer_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed() == (True, False, False):
                    multiplayer = False
                    multiplayer_selected = True
                if multiplayer_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed() == (True, False, False):
                    multiplayer = True
                    multiplayer_selected = True

            elif multiplayer_selected:
                screen.blit(level1_button, level1_rect)
                screen.blit(level2_button, level2_rect)
                screen.blit(level3_button, level3_rect)

                if level1_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed() == (True, False, False):
                        game_active = True
                        level_speed = 0.15
                        Stone.spawn_chance = 10
                        Stone.spawn_chance2 = 100
                        stone2_spawn = False
                        score_multiplikator = 0.5
                        if multiplayer:
                            transition_multiplayer_play = True
                        else:
                            transition_singleplayer_play = True

                if level2_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed() == (True, False, False):
                        game_active = True
                        level_speed = 0.3
                        Stone.spawn_chance1 = 0
                        Stone.spawn_chance2 = 0
                        stone2_spawn = True
                        score_multiplikator = 1
                        if multiplayer:
                            transition_multiplayer_play = True
                        else:
                            transition_singleplayer_play = True

                if level3_rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed() == (True, False, False):
                        game_active = True
                        level_speed = 0.7
                        Stone.spawn_chance1 = 0
                        Stone.spawn_chance2 = 0
                        stone2_spawn = True
                        score_multiplikator = 2
                        if multiplayer:
                            transition_multiplayer_play = True
                        else:
                            transition_singleplayer_play = True

    if transition_singleplayer_play:
        transition_singleplayer.preview()
        transition_singleplayer_play = False
        timer_start = pygame.time.get_ticks()

    if transition_multiplayer_play:
        transition_multiplayer.preview()
        transition_multiplayer_play = False
        timer_start = pygame.time.get_ticks()

    # animation:
    Owl.animation_count += 1
    if Owl.animation_count == 8:
        if Owl.index == 0:
            Owl.index = 1
            Owl.y_pos -= 6
        elif Owl.index == 1:
            Owl.index = 0
            Owl.y_pos += 6
        Owl.animation_count = 0
        Owl.current_frame = Owl.liste[Owl.index]

    if multiplayer:
        Chicken.animation_count += 1
        if Chicken.animation_count == 8:
            if Chicken.index == 0:
                Chicken.index = 1
                Chicken.x_pos -= 6
            elif Chicken.index == 1:
                Chicken.index = 0
                Chicken.x_pos += 6
            Chicken.animation_count = 0
            Chicken.current_frame = Chicken.liste[Chicken.index]

    if Owl.death or Chicken.death:
        score_banner = default_font.render("Score: " + str(time_played), False, (106, 62, 35))
        if Owl.death:
            character = Owl
        elif Chicken.death:
            character = Chicken
        character.speed += 1
        character.y_pos += character.speed
        screen.blit(background, (0, 0))
        character.rect = character.death_frame.get_rect(midbottom=(character.x_pos, character.y_pos))
        screen.blit(character.death_frame, character.rect)
        screen.blit(score_banner, (820, 900))
        if character.y_pos > 1400:
            Owl.death = False
            Chicken.death = False
            Owl.y_pos = 370
            Chicken.y_pos = 460
            Chicken.x_pos = 963
            Owl.x_pos = 963
            character.speed = 10
            character.rect = character.current_frame.get_rect(midbottom=(character.x_pos, character.y_pos))
            Chicken.bahn_list_index = 2
            Owl.bahn_list_index = 2
            multiplayer_selected = False

    if game_active:
        screen.blit(background, (0, 0))
        current_time = pygame.time.get_ticks()
        time_played = current_time - timer_start
        time_played /= 10
        time_played *= score_multiplikator
        time_played = int(time_played)
        score_banner = default_font.render("Score: " + str(time_played), False, (106, 62, 35))
        screen.blit(score_banner, (820, 900))
        if Owl.arrow_key_links:
            Owl.speed += 2
            Owl.x_pos -= Owl.speed
            if Owl.x_pos <= Owl.bahn_list[Owl.bahn_list_index]:
                Owl.x_pos = Owl.bahn_list[Owl.bahn_list_index]
                Owl.speed = 10
                Owl.arrow_key_links = False

        if Owl.arrow_key_rechts:
            Owl.speed += 2
            Owl.x_pos += Owl.speed
            if Owl.x_pos >= Owl.bahn_list[Owl.bahn_list_index]:
                Owl.x_pos = Owl.bahn_list[Owl.bahn_list_index]
                Owl.speed = 10
                Owl.arrow_key_rechts = False

        if Chicken.arrow_key_links:
            Chicken.speed += 2
            Chicken.x_pos -= Chicken.speed
            if Chicken.x_pos <= Chicken.bahn_list[Chicken.bahn_list_index]:
                Chicken.x_pos = Chicken.bahn_list[Chicken.bahn_list_index]
                Chicken.speed = 10
                Chicken.arrow_key_links = False

        if Chicken.arrow_key_rechts:
            Chicken.speed += 2
            Chicken.x_pos += Chicken.speed
            if Chicken.x_pos >= Chicken.bahn_list[Chicken.bahn_list_index]:
                Chicken.x_pos = Chicken.bahn_list[Chicken.bahn_list_index]
                Chicken.speed = 10
                Chicken.arrow_key_rechts = False

        if Stone.spawn:
            Stone.speed += level_speed
            Stone.y -= Stone.speed
            Stone.rect = Stone.frame.get_rect(midtop=(Stone.x, Stone.y))
            screen.blit(Stone.frame, Stone.rect)
            if Stone.y < -200:
                Stone.y = 1081
                Stone.rect = Stone.frame.get_rect(midtop=(Stone.x, Stone.y))
                screen.blit(Stone.frame, Stone.rect)
                Stone.speed = 10
                Stone.spawn = False

        if Stone.spawn2:
            Stone.speed2 += level_speed
            Stone.y2 -= Stone.speed2
            Stone.rect2 = Stone.frame.get_rect(midtop=(Stone.x2, Stone.y2))
            screen.blit(Stone.frame, Stone.rect2)
            if Stone.y2 < -200:
                Stone.y2 = 1081
                Stone.rect2 = Stone.frame.get_rect(midtop=(Stone.x, Stone.y2))
                screen.blit(Stone.frame, Stone.rect2)
                Stone.speed2 = 10
                Stone.spawn2 = False

        if Owl.rect.colliderect(Stone.rect) or Owl.rect.colliderect(Stone.rect2):
            Stone.rect = Stone.rect2 = Stone.frame.get_rect(midtop=(Stone.x, 1081))
            Stone.y = Stone.y2 = 1081
            Stone.speed = Stone.speed2 = 10
            Stone.spawn = Stone.spawn2 = game_active = False
            multiplayer = None
            Owl.speed = -20
            Owl.death = True
            multiplayer_selected = False

        if multiplayer:
            if Chicken.rect.colliderect(Stone.rect) or Chicken.rect.colliderect(Stone.rect2):
                Stone.rect = Stone.rect2 = Stone.frame.get_rect(midtop=(Stone.x, 1081))
                Stone.y = Stone.y2 = 1081
                Stone.speed = Stone.speed2 = 10
                Stone.spawn = Stone.spawn2 = game_active = False
                multiplayer = None
                Chicken.speed = -20
                Chicken.death = True
                multiplayer_selected = False

        if Owl.jump:
            Owl.speed += 1
            Owl.y_pos += Owl.speed
            if Owl.y_pos >= 370:
                Owl.y_pos = 370
                Owl.jump = False
                Owl.speed = 10

        if Chicken.jump:
            Chicken.speed += 1
            Chicken.y_pos += Chicken.speed
            if Chicken.y_pos >= 460:
                Chicken.y_pos = 460
                Chicken.jump = False
                Chicken.speed = 10

        Owl.rect = Owl.current_frame.get_rect(midbottom=(Owl.x_pos, Owl.y_pos))
        screen.blit(Owl.current_frame, Owl.rect)
        if multiplayer:
            Chicken.rect = Chicken.current_frame.get_rect(midbottom=(Chicken.x_pos, Chicken.y_pos))
            screen.blit(Chicken.current_frame, Chicken.rect)

        screen.blit(Stone.frame, Stone.rect)
        if stone2_spawn:
            screen.blit(Stone.frame, Stone.rect2)

    pygame.display.update()
    clock.tick(60)
