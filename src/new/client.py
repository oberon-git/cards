import socket
import threading

import pygame
from client import client_data
from client.resources import Resources
from client.ui.menu_ui import MenuUI
from client.ui.game_ui import GameUI
from client.net.network import Network


def waiting(win, x):
    win.fill((255, 255, 255))
    font = pygame.font.SysFont('Times', 30)
    rect = font.render("Waiting For Opponent", True, (0, 0, 0)).get_rect()
    rect.center = (client_data.WIN_WIDTH // 2, client_data.WIN_HEIGHT // 2)
    text = font.render("Waiting For Opponent" + "." * x, True, (0, 0, 0))
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


def main():
    pygame.init()

    resources = Resources()
    win = pygame.display.set_mode((client_data.WIN_WIDTH, client_data.WIN_HEIGHT))
    pygame.display.set_caption('Cards')
    pygame.display.set_icon(resources.icon)

    clock = pygame.time.Clock()

    active = show_menu = True
    frames = 0
    menu_ui = MenuUI(win, resources)
    game = p = network = None
    while active:
        active, clicked, escaped, mouse_pos = event_loop()

        if show_menu:
            menu_ui.draw(mouse_pos, clicked)
            if menu_ui.start_game:
                show_menu = False
                network = Network()
        else:
            if network.connected:
                if game is None:
                    game, p = network.get_initial_game_data()
                game.draw(win, resources, p, mouse_pos, clicked, frames)
            else:
                waiting(win, (frames // 32) % 4)

        clock.tick(60)
        pygame.display.update()
        frames += 1


if __name__ == '__main__':
    main()
