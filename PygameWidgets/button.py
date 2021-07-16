from typing import Tuple

import pygame

from PygameWidgets.constants import *
from PygameWidgets.exceptions import *


class Button:
    def __init__(self,
                 WIN: pygame.surface.Surface,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 inactive_color: Tuple[int, int, int],
                 hover_inactive_color: Tuple[int, int, int],
                 active_color: Tuple[int, int, int],
                 hover_active_color: Tuple[int, int, int],
                 **kwargs):

        # get the screen to draw the button
        self.WIN = WIN

        # get the positions/dimensions of the button
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.pressed = False
        self.anchor = kwargs.get("anchor", TOPLEFT)
        self.button_rect = pygame.Rect(1, 1, 1, 1)
        self.update_button_rect(self.x, self.y, self.w, self.h)

        # get the colors
        self.inactive_color = inactive_color
        self.hover_inactive_color = hover_inactive_color
        self.active_color = active_color
        self.hover_active_color = hover_active_color
        self.color = self.active_color if self.pressed else self.inactive_color

        # get the images if there is any
        inactive_sprite = kwargs.get("inactive_sprite", None)  # the sprite that is used when the button is deactivated
        if inactive_sprite:
            transform_scale_image = kwargs.get("transform_scale_image", True)
            if inactive_sprite:
                if isinstance(inactive_sprite, pygame.surface.Surface):
                    if transform_scale_image:
                        self.inactive_sprite = pygame.transform.scale(inactive_sprite.convert_alpha(), (self.w, self.h))
                    else:
                        self.inactive_sprite = inactive_sprite.convert_alpha()
                elif isinstance(inactive_sprite, str):
                    if transform_scale_image:
                        self.inactive_sprite = pygame.transform.scale(
                            pygame.image.load(inactive_sprite).convert_alpha(), (self.w, self.h))
                    else:
                        self.inactive_sprite = pygame.image.load(inactive_sprite).convert_alpha()
        else:
            self.inactive_sprite = None

        inactive_hover_sprite = kwargs.get("inactive_hover_sprite",
                                           None)  # the sprite that is used when the button is deactivated
        if inactive_hover_sprite:
            transform_scale_image = kwargs.get("transform_scale_image", True)
            if inactive_hover_sprite:
                if isinstance(inactive_hover_sprite, pygame.surface.Surface):
                    if transform_scale_image:
                        self.inactive_hover_sprite = pygame.transform.scale(inactive_hover_sprite.convert_alpha(),
                                                                            (self.w, self.h))
                    else:
                        self.inactive_hover_sprite = inactive_hover_sprite.convert_alpha()
                elif isinstance(inactive_hover_sprite, str):
                    if transform_scale_image:
                        self.inactive_hover_sprite = pygame.transform.scale(
                            pygame.image.load(inactive_hover_sprite).convert_alpha(), (self.w, self.h))
                    else:
                        self.inactive_hover_sprite = pygame.image.load(inactive_hover_sprite).convert_alpha()
        else:
            self.inactive_hover_sprite = self.inactive_sprite

        active_sprite = kwargs.get("active_sprite", None)  # the sprite that is used when the button is activated
        if active_sprite:
            transform_scale_image = kwargs.get("transform_scale_image", True)
            if active_sprite:
                if isinstance(active_sprite, pygame.surface.Surface):
                    if transform_scale_image:
                        self.active_sprite = pygame.transform.scale(active_sprite.convert_alpha(), (self.w, self.h))
                    else:
                        self.active_sprite = active_sprite.convert_alpha()
                elif isinstance(active_sprite, str):
                    if transform_scale_image:
                        self.active_sprite = pygame.transform.scale(pygame.image.load(active_sprite).convert_alpha(),
                                                                    (self.w, self.h))
                    else:
                        self.active_sprite = pygame.image.load(active_sprite).convert_alpha()
        else:
            self.active_sprite = self.inactive_sprite

        active_hover_sprite = kwargs.get("active_hover_sprite",
                                         None)  # the sprite that is used when the button is activated
        if active_hover_sprite:
            transform_scale_image = kwargs.get("transform_scale_image", True)
            if active_hover_sprite:
                if isinstance(active_hover_sprite, pygame.surface.Surface):
                    if transform_scale_image:
                        self.active_hover_sprite = pygame.transform.scale(active_hover_sprite.convert_alpha(),
                                                                          (self.w, self.h))
                    else:
                        self.active_hover_sprite = active_hover_sprite.convert_alpha()
                elif isinstance(active_hover_sprite, str):
                    if transform_scale_image:
                        self.active_hover_sprite = pygame.transform.scale(
                            pygame.image.load(active_hover_sprite).convert_alpha(), (self.w, self.h))
                    else:
                        self.active_hover_sprite = pygame.image.load(active_hover_sprite).convert_alpha()
        else:
            self.active_hover_sprite = self.active_sprite

        # get the functions if the user has set any
        self.on_click = kwargs.get("on_click", None)  # the function that is called when the button is activated
        self.on_click_args = kwargs.get("on_click_args", None)  # the positional arguments of the function that is called when the button is activated
        self.on_click_kwargs = kwargs.get("on_click_kwargs", None)  # the key-word arguments of the function that is called when the button is activated
        self.on_release = kwargs.get("on_release", None)  # the function that is called when the button is deactivated
        self.on_release_args = kwargs.get("on_release_args", None)  # the positional arguments of the function that is called when the button is deactivated
        self.on_release_kwargs = kwargs.get("on_release_kwargs", None)  # the key-word arguments of the function that is called when the button is deactivated

        # get the text info
        self.text = kwargs.get("text",
                               f"jdhfroiewnvowijfvnoi")  # for multiple lines use PygameWidgets.constants.LINE_SPLITTER
        if self.text != "":
            self.antialias = kwargs.get("antialias", True)
            self.text_color = kwargs.get("text_color", (0, 0, 0))
            self.font_name = kwargs.get("font_name", "camicsans")
            self.font_size = kwargs.get("font_size", 60)
            self.font = pygame.font.SysFont(self.font_name, self.font_size)

            self.update_text()

        self.kwargs = kwargs

    def update_text(self):
        if LINE_SPLITTER in self.text:
            self.text_rects = []
            self.rendered_texts = []
            self.text_lines = self.text.split(LINE_SPLITTER)
            final_h = 0

            for text in self.text_lines:
                label = self.font.render(
                    text, self.antialias, self.text_color
                )
                self.rendered_texts.append(
                    label
                )
                final_h += label.get_height() + 5

            if final_h > self.h:
                raise TextOutOfButton("the given string: '{0}' is {1}pxls out of bounds in the y axis".format(
                    self.text.replace(LINE_SPLITTER, " "), final_h - self.h))

            self.text_rects.reverse()
            self.rendered_texts.reverse()

            for i in range(len(self.rendered_texts)):
                self.text_rects.append(
                    self.rendered_texts[i].get_rect()
                )

                self.text_rects[i].center = (
                    self.button_rect.center[0],  # x
                    (self.button_rect.center[1] + final_h / 2) - self.text_rects[i][3]
                )
                final_h -= self.text_rects[i][3] + 25

            for rendered_text in self.rendered_texts:
                if rendered_text.get_width() > self.w:
                    raise TextOutOfButton("the given string: '{0}' is {1}pxl out of bounds in the x axis".format(self.text.split(LINE_SPLITTER)[self.rendered_texts.index(rendered_text)],rendered_text.get_width() - self.h))

        else:
            if self.font.render(self.text.replace(LINE_SPLITTER, " "), self.antialias,
                                self.text_color).get_width() > self.w:
                raise TextOutOfButton("the given string: '{0}' is {1}pxl out of bounds in the x axis".format(
                    self.text.replace(LINE_SPLITTER, " "), self.font.render(self.text.replace(LINE_SPLITTER, " "), self.antialias, self.text_color).get_width() - self.h))

            self.rendered_text = self.font.render(str(self.text), self.antialias, self.text_color)
            self.text_rect = self.rendered_text.get_rect()
            self.text_rect.center = self.button_rect.center

    def update_button_rect(self, x: int, y: int, w: int, h: int):
        if self.anchor == CENTER:
            self.button_rect = pygame.Rect(x, y, w, h)
            self.button_rect.center = (x, y)
        elif self.anchor == TOPLEFT:
            self.button_rect = pygame.Rect(x, y, w, h)
            self.button_rect.topleft = (x, y)
        elif self.anchor == BOTTOMLEFT:
            self.button_rect = pygame.Rect(x, y, w, h)
            self.button_rect.bottomleft = (x, y)
        elif self.anchor == TOPRIGHT:
            self.button_rect = pygame.Rect(x, y, w, h)
            self.button_rect.topright = (x, y)
        elif self.anchor == BOTTOMRIGHT:
            self.button_rect = pygame.Rect(x, y, w, h)
            self.button_rect.bottomright = (x, y)
        elif self.anchor == MIDTOP:
            self.button_rect = pygame.Rect(x, y, w, h)
            self.button_rect.midtop = (x, y)
        elif self.anchor == MIDLEFT:
            self.button_rect = pygame.Rect(x, y, w, h)
            self.button_rect.midleft = (x, y)
        elif self.anchor == MIDBOTTOM:
            self.button_rect = pygame.Rect(x, y, w, h)
            self.button_rect.midbottom = (x, y)
        elif self.anchor == MIDRIGHT:
            self.button_rect = pygame.Rect(x, y, w, h)
            self.button_rect.midright = (x, y)

    def draw(self):
        if self.pressed:
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                self.color = self.hover_active_color
                sprite = self.active_hover_sprite
            else:
                self.color = self.active_color
                sprite = self.active_sprite
        else:
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                self.color = self.hover_inactive_color
                sprite = self.inactive_hover_sprite
            else:
                self.color = self.inactive_color
                sprite = self.inactive_sprite

        pygame.draw.rect(self.WIN, self.color, self.button_rect)
        if sprite:
            self.WIN.blit(sprite, self.button_rect)

        if self.text != "":
            if LINE_SPLITTER in self.text:
                for rendered_text in self.rendered_texts:
                    self.WIN.blit(rendered_text, self.text_rects[self.rendered_texts.index(rendered_text)])

            else:
                self.WIN.blit(self.rendered_text, self.text_rect)

    def event_handler(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.button_rect.collidepoint(event.pos):
                    if self.pressed:
                        self.pressed = False

                        # call the function that is given if there is any
                        if self.on_release:
                            if self.on_release_kwargs and self.on_release_args:
                                self.on_release(*self.on_release_args, **self.on_release_kwargs)

                            elif self.on_release_args:
                                self.on_release(*self.on_release_args)

                            elif self.on_release_kwargs:
                                self.on_release(**self.on_release_kwargs)

                            else:
                                self.on_release()

                    elif not self.pressed:
                        self.pressed = True

                        # call the function that is given if there is any
                        if self.on_click:
                            if self.on_click_kwargs and self.on_click_args:
                                self.on_click(*self.on_click_args, **self.on_click_kwargs)

                            elif self.on_click_args:
                                self.on_click(*self.on_click_args)

                            elif self.on_click_kwargs:
                                self.on_click(**self.on_click_kwargs)

                            else:
                                self.on_click()