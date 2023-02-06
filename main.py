import os

from random import choice
import json

from field import Field
from shipChoice import ShipChoice
from button import Button
from bot import Bot
from const import *

creators = False
game_stat = gameStatus.ship_setup


def start_screen():
    res = width, height = (640, 512)
    fps = 60
    fps_clock = pygame.time.Clock()
    largeFont = pygame.font.SysFont('comicsans', 28)

    sc = pygame.display.set_mode((width, height))
    screen = pygame.display.set_mode(res)
    dog_surf = pygame.image.load('data/sprites/mor.gif')
    dog_rect = dog_surf.get_rect(
        bottomright=(width, height))
    sc.blit(dog_surf, dog_rect)
    dog_surf_nad = pygame.image.load('data/sprites/mrboi2.png')
    dog_rect_nad = dog_surf_nad.get_rect(
        bottomright=(120, 100))
    sc.blit(dog_surf_nad, dog_rect)

    pygame.mixer.music.load("data/music/noize.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    buttons = [Button(175, 150, 300, 100, 'Играть!', onclickFunction=new_game),
               Button(175, 270, 300, 100, 'Об авторах', onclickFunction=creators_change), ]

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()

        sc.blit(dog_surf, dog_rect)
        if creators:
            table_creators_surf = pygame.image.load('data/sprites/table2.png')
            table_creators_rect = table_creators_surf.get_rect(
                bottomright=(500, 500))
            sc.blit(table_creators_surf, (120, 0))

            about_a = largeFont.render('Биба, Боба и Абоба', 1, (255, 255, 255))
            screen.blit(about_a, (table_creators_rect.centerx - about_a.get_width() // 2.4, 200))

        else:
            for button in buttons:
                button.process(screen)
            sc.blit(dog_surf_nad, dog_rect)

        pygame.display.flip()
        fps_clock.tick(fps)


def creators_change():
    global creators
    creators = True


def main():
    pygame.init()
    pygame.font.init()
    start_screen()


def end_screen(vic_or_def, score):
    width, height = (640, 512)
    fps = 60
    fps_clock = pygame.time.Clock()
    largeFont = pygame.font.SysFont('comicsans', 40)  # creates a font object
    screen = pygame.display.set_mode((width, height))
    dog_surf = pygame.image.load('data/sprites/background.png')
    dog_rect = dog_surf.get_rect(
        bottomright=(width, height))
    screen.blit(dog_surf, dog_rect)
    if vic_or_def:
        pygame.mixer.music.load(choice(["data/music/victory1.mp3", "data/music/victory2.mp3"]))
        dog_surf_nad = pygame.image.load('data/sprites/Victory.png')
        dog_rect_nad = dog_surf_nad.get_rect(
            bottomright=(600, 250))
        screen.blit(dog_surf_nad, (20, 50))

        lastScore = largeFont.render('Лучший результат: ' + str(get_last_res(score)), 1,
                                     (255, 255, 255))  # We will create the function updateFile later
        currentScore = largeFont.render('Результат: ' + str(score), 1, (255, 255, 255))
        screen.blit(lastScore, (width // 2 - lastScore.get_width() // 2, dog_rect_nad.bottom + 10))
        screen.blit(currentScore, (width // 2 - currentScore.get_width() // 2, dog_rect_nad.bottom
                                   + 10 + lastScore.get_height() + 20))
    else:
        dog_surf_nad = pygame.image.load('data/sprites/Defeat.png')
        pygame.mixer.music.load(choice(["data/music/defeat1.mp3", "data/music/defeat2.mp3"]))
        dog_rect_nad = dog_surf_nad.get_rect(
            bottomright=(600, 250))
        screen.blit(dog_surf_nad, (20, 50))
        currentScore = largeFont.render('Результат: ' + str(score), 1, (255, 255, 255))
        screen.blit(currentScore, (width // 2 - currentScore.get_width() // 2, dog_rect_nad.bottom + 10))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
        pygame.display.flip()
        fps_clock.tick(fps)
        pygame.display.update()


def get_last_res(score):
    file_name = 'Statistics.json'
    with open(file_name, 'r+') as file:
        if os.stat(file_name).st_size == 0:
            json.dump({"score": score}, file)
            return score
        else:
            last_score = json.load(file)["score"]
            print(last_score)
            if score > last_score:
                file.seek(0)
                json.dump({"score": score}, file)
                file.truncate()
                return score
            else:
                return last_score


def change_stat():
    global game_stat
    game_stat = gameStatus.player


def new_game():
    global game_stat

    pygame.mixer.music.stop()
    fps_clock = pygame.time.Clock()

    fps = 60
    score = 0
    strikes = 0
    bot_delay = False

    bg = pygame.image.load("data/sprites/background.png")
    all_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    font = pygame.font.SysFont('notosans', FONT_SIZE)
    board1 = Field(50, (screen.get_width() - 1000 - INTERVAL_BOARD) // 2, 0, 'Ваше поле')
    game_stat = gameStatus.ship_setup
    pygame.mixer.music.stop()
    fps_clock = pygame.time.Clock()

    fps = 60
    score = 0
    strikes = 0
    bg = pygame.image.load("data/sprites/background.png")
    all_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    font = pygame.font.SysFont('notosans', FONT_SIZE)

    board1 = Field(50, (screen.get_width() - 1000 - INTERVAL_BOARD) // 2, 0, 'Ваше поле')
    board2 = Field(50, board1.get_field_width() + INTERVAL_BOARD, 11.3, 'Поле противника')
    bot = Bot(board2.check_collision_ship, board2.set_ship)
    bot.auto_set_ships()

    ship_choice_bar = ShipChoice((screen.get_width() - 1150) // 2, board1.get_field_height(), all_sprites, change_stat)

    button_close = Button(screen.get_width() - 60, 10, 50, 50,
                          icon=pygame.image.load('data/sprites/img3.png'), onclickFunction=pygame.quit)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                sp = event.pos
                if game_stat == gameStatus.ship_setup:
                    ship_choice_bar.start_motion(sp, board1.del_ship)
                elif game_stat == gameStatus.player:
                    bot_delay = False
                    x, y = event.pos
                    if board2.check_click_corr(x, y):
                        hod_res = board2.check_strike(x, y)
                        if hod_res is None:
                            continue
                        elif hod_res != BoardStat.MISS_SHOT:
                            strikes += 1
                            score += 100 * strikes
                        else:
                            strikes = 0
                            game_stat = gameStatus.bot
                            bot_delay = True
            if event.type == pygame.MOUSEMOTION and ship_choice_bar.get_motion_flag():
                pos = event.rel
                ship_choice_bar.motion(pos)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and ship_choice_bar.get_motion_flag():
                sp = event.pos
                ship_choice_bar.stop_motion(sp, board1.check_click_corr,
                                            board1.set_ship, board1.check_collision_ship)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c \
                    and ship_choice_bar.current_ship is not None:
                ship_choice_bar.rotate_ship()

        screen.blit(bg, (0, 0))
        board1.render_board(screen)
        board2.render_board(screen)
        all_sprites.draw(screen)
        board1.render_cell_stat(screen)
        board2.render_cell_stat(screen)
        if game_stat != gameStatus.ship_setup:
            score_render = font.render(f'Очки: {score}', True, WHITE)
            screen.blit(score_render,
                        (board1.get_field_width() + (INTERVAL_BOARD // 2 - score_render.get_width() // 2),
                         board1.get_field_height()))
            screen.blit(arrow_player if game_stat == gameStatus.player else arrow_bot,
                        (board1.get_field_width() + INTERVAL_BOARD // 2 - arrow_bot.get_width() // 2,
                         board1.get_field_height() // 2))
        button_close.process(screen)
        ship_choice_bar.render(screen)
        pygame.display.flip()
        fps_clock.tick(fps)

        if bot_delay:
            pygame.time.delay(600)
        if game_stat == gameStatus.bot:
            move_res = bot.make_shot(board1.check_strike, board1.ships)
            if move_res == BoardStat.MISS_SHOT:
                bot_delay = False
                game_stat = gameStatus.player
        if board1.get_ships_count() == 0 and game_stat != gameStatus.ship_setup:
            game_stat = gameStatus.game_over
            end_screen(False, score)
            return
        if board2.get_ships_count() == 0 and game_stat != gameStatus.ship_setup:
            game_stat = gameStatus.game_over
            score += 100 * board2.get_ships_count()
            end_screen(True, score)
            return


if __name__ == '__main__':
    main()
