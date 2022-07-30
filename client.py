import socket

import pygame
from resources import Resources
from network import Network


def waiting(win, x):
    win.fill((255, 255, 255))
    font = pygame.font.SysFont(None, 30)
    rect = font.render("Waiting For Opponent", True, (0, 0, 0)).get_rect()
    rect.center = (win.get_width() // 2, win.get_height() // 2)
    text = font.render("Waiting For Opponent" + "." * x, True, (0, 0, 0))
    win.blit(text, rect)


def draw(win, game, resources, p, pos, clicked):
    game.draw(win, resources, p, pos, clicked)


def main():
    n = Network()
    p, card_list = n.connect()
    game = n.send(None)
    resources = Resources(card_list)

    pygame.init()
    pygame.font.init()
    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    count = 0
    active = True
    while active:
        try:
            clicked = False
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    win = win = pygame.display.set_mode((750, 750))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True
                    pos = pygame.mouse.get_pos()
            if game.connected():
                draw(win, game, resources, p, pos, clicked)
            else:
                waiting(win, (count // 16) % 4)
            game = n.send(game)
            count += 1
            clock.tick(60)
            pygame.display.update()
            if game is None:
                active = False
                pygame.quit()
        except pygame.error or socket.error:
            active = False
            pygame.quit()


main()
