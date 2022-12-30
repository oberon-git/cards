import pygame
import socket
from shared.shared_data import *
from client.menu import Menu
from client.resources import Resources
from client.network import Network
from client.user_settings import UserSettings

pygame.init()


def waiting(win, x):
    font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
    win.fill(WHITE)
    rect = font.render("Waiting For Opponent.", True, BLACK).get_rect()
    rect.center = CENTER
    text = font.render("Waiting For Opponent." + "." * x, True, BLACK)
    win.blit(text, rect)


def event_loop():
    active = True
    clicked = escaped = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                escaped = True
    return active, clicked, escaped, pygame.mouse.get_pos()


def main(win, resources, usersettings):
    clock = pygame.time.Clock()

    n = Network()
    menu = None

    count = 0
    active = True
    while active:
        active, clicked, escaped, mouse_pos = event_loop()
        if n.connected:
            if n.game is None:
                n.start_game()
                menu = Menu(usersettings, True)
            if escaped:
                menu.escape()
            if not menu.active:
                n.update(win, resources, usersettings, mouse_pos, clicked, count)
                if n.game.reset:
                    n.kill_all_threads = True
                    main(win, resources, usersettings)
            menu.draw(win, resources, clicked, mouse_pos)
        else:
            waiting(win, ((count // BLINK_SPEED) % 3))

        count += 1
        clock.tick(FPS)
        pygame.display.update()
    n.kill_all_threads = True


def draw_menu(win, resources, usersettings):
    clock = pygame.time.Clock()
    menu = Menu(usersettings)

    active = True
    while active:
        active, clicked, escaped, pos = event_loop()
        if active:
            active = menu.escape(escaped)
        menu.draw(win, resources, clicked, pos)
        if menu.start:
            return main(win, resources, usersettings)
        clock.tick(FPS)
        pygame.display.update()


def setup_win(settings, resources):
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(settings.get_game_name())
    pygame.display.set_icon(resources.icon)
    return win


def setup_dir():
    if not os.path.exists(ASSET_DIR):
        os.mkdir(ASSET_DIR)
    if not os.path.exists(CARDS_DIR):
        os.mkdir(CARDS_DIR)
    if not os.path.exists(BACKGROUND_DIR):
        os.mkdir(BACKGROUND_DIR)
    if not os.path.exists(UI_DIR):
        os.mkdir(UI_DIR)
    if not os.path.exists(USER_SETTINGS_PATH):
        default_settings = {"background": 1, "shared": 1}
        with open(USER_SETTINGS_PATH, 'w') as user_file:
            yaml.dump(default_settings, user_file)


def startup():
    setup_dir()
    resources = Resources()
    usersettings = UserSettings()
    win = setup_win(usersettings, resources)
    draw_menu(win, resources, usersettings)


if __name__ == "__main__":
    startup()
    pygame.quit()
