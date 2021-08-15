import pygame
from PygameHelper import MultiLineText
from PygameHelper.constants import *


pygame.init()
pygame.font.init()


WIN = pygame.display.set_mode((500, 500))

pygame.display.set_caption("MultiLineText")


text = MultiLineText(
    WIN,                                    # WIN
    250,                                    # x
    250,                                    # y
    f"Hello Word\nBey World",               # text
    RED,                                    # color
    anchor=CENTER,                          # anchor
    font_size=60,                           # font_size
    font_type="comicsans",                  # font_type
    antialias=True                          # antialias
)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit(-1)

    WIN.fill((30, 30, 30))
    text.draw()
    pygame.display.update()
