import sys
import pygame
from shared.shared_data import WIN_WIDTH, WIN_HEIGHT, WIN_NAME, CENTER, FPS, BLINK_SPEED
from shared.shared_data import WHITE, BLACK, FONT_SIZE, FONT_FAMILY
from client.menu import Menu
from client.resources import Resources
from client.network import Network
from client.user_settings import UserSettings
from client.event import Event
from client.client_game_data import ClientGameData


def waiting(win, x):
    font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
    win.fill(WHITE)
    rect = font.render("Waiting For Opponent", True, BLACK).get_rect()
    rect.center = CENTER
    text = font.render("Waiting For Opponent" + "." * x, True, BLACK)
    win.blit(text, rect)


def game_loop(win, resources, menu, usersettings):
    n = Network(usersettings.get_game_name())
    client_data = ClientGameData(usersettings)
    clock = pygame.time.Clock()
    frame_count = 0
    while True:
        event = Event(pygame.event.get())
        if event.quit:
            break
        if n.connected:
            if not n.game_started:
                n.start_game()
            if event.escape and menu.escape():
                break
            if n.game.reset or menu.exit_game:
                n.close()
                return menu_loop(win, resources, usersettings)
            if not menu.active:
                n.update(win, resources, client_data, event, frame_count)
            menu.draw(win, resources, event, frame_count)
        else:
            waiting(win, ((frame_count // BLINK_SPEED) % 4))
        frame_count += 1
        clock.tick(FPS)
        pygame.display.update()
    n.close()


def menu_loop(win, resources, usersettings):
    clock = pygame.time.Clock()
    menu = Menu(usersettings)
    frame_count = 0
    while True:
        event = Event(pygame.event.get())
        if event.quit:
            break
        if event.escape and menu.escape():
            break
        menu.draw(win, resources, event, frame_count)
        if menu.start:
            return game_loop(win, resources, menu, usersettings)
        frame_count += 1
        clock.tick(FPS)
        pygame.display.update()


def main():
    pygame.init()

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    resources = Resources()
    usersettings = UserSettings()

    pygame.display.set_caption(WIN_NAME)
    pygame.display.set_icon(resources.icon)

    menu_loop(win, resources, usersettings)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
