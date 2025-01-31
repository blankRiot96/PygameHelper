# MIT License
#
# Copyright (c) 2021 Emc2356
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
some useful functions for pygame
and general use
"""

from typing import List, Tuple, Iterable, Generator, Union, Dict, Sequence, Set, TypeVar, Any, overload as TpOverload
from functools import lru_cache

import pygame
import json
import math

from PygameHelper.constants import *
from PygameHelper.exceptions import *
from PygameHelper.types import *

Number = Union[int, float]
NeighborOutputType = TypeVar("NeighborOutputType")


@lru_cache()
def load_image(path: str) -> pygame.surface.Surface:
    """
    it loads an image from a given path and it performs a .convert
    :param path: str
    :return: pygame.surface.Surface
    """
    return pygame.image.load(path).convert()


@lru_cache()
def load_alpha_image(path: str) -> pygame.surface.Surface:
    """
    it loads an image from a given path and it performs a .convert_alpha
    :param path: str
    :return: pygame.surface.Surface
    """
    return pygame.image.load(path).convert_alpha()


def resize_smooth_image(
        image: pygame.surface.Surface, new_size: Union[List[int], Tuple[int, int]]
) -> pygame.surface.Surface:
    """
    wrapper for pygame.transform.smoothscale
    :param image: pygame.surface.Surface
    :param new_size: Union[List[int], Tuple[int, int, int]]
    :return:
    """
    return pygame.transform.smoothscale(image, new_size)


def resize_image(image: pygame.surface.Surface, new_size: Union[List[int], Tuple[int, int]]) -> pygame.surface.Surface:
    """
    wrapper for pygame.transform.scale
    :param image: pygame.surface.Surface
    :param new_size: Union[List[int], Tuple[int, int, int]]
    :return: pygame.surface.Surface
    """
    return pygame.transform.scale(image, new_size)


def resize_image_ratio(image: pygame.surface.Surface, new_size: Tuple[int, int]) -> pygame.surface.Surface:
    ratio = new_size[0] / image.get_width()
    return pygame.transform.scale(image,
                                  (math.floor(image.get_width() * ratio), math.floor(image.get_height() * ratio)))


def resizex(image: pygame.surface.Surface, amount: Number) -> pygame.surface.Surface:
    """
    it resizes a image in both axis by the same amount
    :param image: pygame.surface.Surface
    :param amount: Union[int, float]
    :return: pygame.surface.Surface
    """
    return pygame.transform.scale(image,
                                  (math.floor(image.get_width() * amount), math.floor(image.get_height() * amount)))


def left_click(event: pygame.event.Event) -> bool:
    """
    checks if the user has left-clicked the screen
    :param event: pygame.event.Event
    :return: bool
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            return True
    return False


def middle_click(event: pygame.event.Event) -> bool:
    """
    checks if the user has middle-clicked the screen
    :param event: pygame.event.Event
    :return: bool
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 2:
            return True
    return False


def right_click(event: pygame.event.Event) -> bool:
    """
    checks if the user has right-clicked the screen
    :param event: pygame.event.Event
    :return: bool
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 3:
            return True
    return False


@lru_cache()
def get_font(size, type_of_font="comicsans") -> pygame.font.Font:
    """
    it returns a font
    :param size: int
    :param type_of_font: str
    :return: pygame.font.Font
    """
    if type_of_font.endswith(".tff"):
        font = pygame.font.Font(
            type_of_font, size
        )
        return font

    font = pygame.font.SysFont(
        type_of_font, size
    )
    return font


@lru_cache()
def wrap_multi_lines(
        text: str, font: pygame.font.Font, max_width: int, max_height: int=0, antialias: bool=True
) -> List[str]:
    """
    it returns a list of strings
    :param text: str
    :param font: pygame.font.Font
    :param max_width: int
    :param max_height: int=0
    :param antialias: bool=True
    :return: List[str]
    """
    finished_lines = [""]

    for word in text.split(" "):
        w = font.render(word, antialias, BLACK).get_width()
        # check if one word is too long to fit in one line
        if w > max_width:
            raise WordTooLong(
                f"""the word: "{word}" is too long to fit in a width of: {max_width}, out of bounds by: {w - max_width}pxls""")

        if font.render(finished_lines[-1] + word, antialias, BLACK).get_width() > max_width:
            finished_lines.append(f"""{word}""")
        else:
            finished_lines[-1] += f""" {word}"""
    finished_lines[0] = finished_lines[0][1:]
    if max_height > 0:
        h = 0
        for line in finished_lines:
            h += font.render(line, antialias, BLACK).get_height()

        if h > max_height:
            raise TextOfOutBounds(
                f"""the lines: {finished_lines} are too long in the y axis by: {h - max_height}pxls""")

    return finished_lines


def blit_multiple_lines(
        x: int, y: int, lines: List[str], WIN: pygame.surface.Surface, font: pygame.font.Font,
        centered_x=False, centered_x_pos: int=None, color: Tuple[int, int, int]=(0, 0, 0)
) -> None:
    """
    it blits in a surface a list of strings
    :param x: int
    :param y: int
    :param lines: list[str]
    :param WIN: pygame.surface.Surface
    :param font: pygame.font.Font
    :param centered_x: if the text is going to be x-centered
    :param centered_x_pos: the rect that is going to be used if centered_x is True
    :param color: Tuple[int, int, int]
    :return: None
    """
    if centered_x and not centered_x_pos:
        raise MissingRequiredArgument("Missing 'centered_x_pos'")
    height = font.get_height()
    for i, text in enumerate(lines):
        rendered_text_surface = font.render(text, True, color)
        if centered_x:
            WIN.blit(rendered_text_surface, (centered_x_pos - rendered_text_surface.get_width() / 2, y + (i * height)))
        else:
            WIN.blit(rendered_text_surface, (x, y + (i * height)))


def pixel_perfect_collision(
        image_1: pygame.surface.Surface, image_1_pos: Tuple[int, int],
        image_2: pygame.surface.Surface, image_2_pos: Tuple[int, int]
) -> bool:
    """
    it is a wrapper for pygame.mask.overlap and it handles the offset
    this function is recommended to be used with rectangle collision as pixel perfect collision is really heavy
    :param image_1: pygame.surface.Surface
    :param image_1_pos: Tuple[int, int]
    :param image_2: pygame.surface.Surface
    :param image_2_pos: Tuple[int, int]
    :return: bool
    """
    offset = [image_1_pos[0] - image_2_pos[0],
              image_1_pos[1] - image_2_pos[1]]
    mask_1 = pygame.mask.from_surface(image_1)
    mask_2 = pygame.mask.from_surface(image_2)

    result = mask_2.overlap(mask_1, offset)
    if result:
        return True
    return False


def flatten(iterable: Iterable) -> Generator:
    """
    it takes a iterable object and it flattens the object
    :param iterable: Iterable
    :return: any
    """
    for item in iterable:
        if isinstance(item, list) or isinstance(item, tuple):
            for subitem in flatten(item):
                yield subitem
        else:
            yield item


def get_cloth(path: str) -> Dict[str, list]:
    """
    it returns the cloth data from a file
    :param path: str
    :return: Dict
    """
    with open(path, "r") as f:
        data = json.loads(f.read())
    return data


def get_neighbors(
        grid: List[List[NeighborOutputType]], target: Union[Tuple[int, int], List[int], Sequence[int]]
) -> Generator:
    """
    it returns the directly adjacent cells (it makes the assumption that it has rows of the same length)
    :param grid: List[List[Any]]
    :param target: Union[Tuple[int, int], List[int, int], Sequence[int]]
    :return: List[Any]
    """
    columns = len(grid) - 1
    rows = len(grid[0]) - 1
    oi, oj = target

    for i, j in [(oi - 1, oj), (oi, oj - 1), (oi, oj + 1), (oi + 1, oj)]:
        if not (i == oi and j == oj) and 0 <= i <= columns and 0 <= j <= rows:
            yield grid[i][j]


def get_neighbors_index(
        grid: List[List[Any]],
        target: Union[Tuple[int, int], List[int], Sequence[int]]
) -> Generator:
    """
    it returns the directly adjacent cells index (it makes the assumption that it has rows of the same length)
    :param grid: List[List[Any]]
    :param target: Union[Tuple[int, int], List[int, int], Sequence[int]]
    :return: List[Any]
    """
    columns = len(grid) - 1
    rows = len(grid[0]) - 1
    oi, oj = target

    for i, j in [(oi - 1, oj), (oi, oj - 1), (oi, oj + 1), (oi + 1, oj)]:
        if not (i == oi and j == oj) and 0 <= i <= columns and 0 <= j <= rows:
            yield i, j


def combine_rects(rects: List[RectType]) -> pygame.Rect:
    """
    it creates the smallest possible rect that contains all of the rects
    :param rects: List[RectType]
    :return: RectType
    """
    x = sorted((pygame.Rect(r).x for r in rects))
    y = sorted((pygame.Rect(r).y for r in rects))
    return pygame.Rect(x[0], y[0], x[~0] - x[0], y[~0] - y[0])


__all__ = [
    "load_image",
    "load_alpha_image",
    "resize_smooth_image",
    "resize_image",
    "resize_image_ratio",
    "resizex",
    "left_click",
    "middle_click",
    "right_click",
    "get_font",
    "wrap_multi_lines",
    "blit_multiple_lines",
    "pixel_perfect_collision",
    "flatten",
    "get_cloth",
    "get_neighbors",
    "get_neighbors_index",
    "combine_rects"
]
