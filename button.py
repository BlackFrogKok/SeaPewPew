import pygame

pygame.init()
font = pygame.font.SysFont('Corbel', 35)


class Button:
    def __init__(self, x, y, width, height, buttonText='', onclickFunction=None, onePress=False,
                 color_text=(20, 20, 20), icon=None):
        self.x = x
        self.y = y
        self.icon = icon
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.color_text = color_text
        self.fillColors = {
            'normal': '#20B2AA',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, color_text)

        self.alreadyPressed = False

    def process(self, screen):

        mouse_pos = pygame.mouse.get_pos()

        if self.icon is None:
            self.buttonSurface.fill(self.fillColors['normal'])
        else:
            self.buttonSurface.blit(self.icon, (0, 0))
        if self.buttonRect.collidepoint(mouse_pos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)
