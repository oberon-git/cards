import pygame


class Event:
    def __init__(self, events):
        self.quit = self.click = self.escape = self.e = self.d = self.p = self.enter = self.left = self.right = False
        self.down = self.up = False
        self.num = -1

        for event in events:
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        self.escape = True
                    case pygame.K_e:
                        self.e = True
                    case pygame.K_d:
                        self.d = True
                    case pygame.K_p:
                        self.p = True
                    case pygame.K_LEFT:
                        self.left = True
                    case pygame.K_RIGHT:
                        self.right = True
                    case pygame.K_DOWN:
                        self.down = True
                    case pygame.K_UP:
                        self.up = True
                    case pygame.K_RETURN:
                        self.enter = True
                    case pygame.K_1 | pygame.K_2 | pygame.K_3 | pygame.K_4 | pygame.K_5 | pygame.K_6 | pygame.K_7 | pygame.K_8 | pygame.K_9:
                        self.num = event.key - pygame.K_1
        self.mouse_pos = pygame.mouse.get_pos()
