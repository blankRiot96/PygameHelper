# Button

#### [creator](https://github.com/Emc2356)
#### [source code](https://github.com/Emc2356/PygameHelper)

#### this is a class made for creating button with the [pygame](https://www.pygame.org)
> these are the mandatory arguments

| Argument | Description | Default Value |
|:----------:|:-------------:|:---------------:|
| `WIN` | the surface that the button is going to be drawn in | - |
| `x` | the x position of the button | - |
| `y` | the x position of the button | - |
| `w` | the width of the button | - |
| `h` | the height of the button | - |
| `inactive_color` | the color of the button when the button is inactive | - |
| `hover_inactive_color` | the color of the button when the button is inactive and the mouse is over it | - |
| `active_color` | the color of the button when the button is active | - |
| `hover_active_color` | the color of the button when the button is active and the mouse is over it | - |
> these are the optional arguments

| Argument | Description | Default Value |
|:----------:|:-------------:|:---------------:|
| `border_radius` | how much will the corners will be rounded | 0 |
| `anchor` | the alignment of the x, y positions | topleft | 
| `inactive_sprite` | the sprite that is used when the button is inactive | None |
| `inactive_hover_sprite` | the sprite that is used when the button is inactive and the mouse is over the button | None |
| `active_sprite` | the sprite that is used when the button is active | None |
| `active_hover_sprite` | the sprite that is used when the button is active and the mouse is over the button | None |
| `on_click` | the function that is called when the button is clicked | None |
| `on_click_args` | the positional arguments of the function that is called when the button is clicked | None |
| `on_click_kwargs` | the key-word arguments of the function that is called when the button is clicked | None |
| `on_release` | the function that is called when the button is released | None |
| `on_release_args` | the positional arguments of the function that is called when the button is released | None |
| `on_release_kwargs` | the key-word arguments of the function that is called when the button is released | None |
| `text` | the text that is going to be rendered | "" |
| `antialias` | if the text is going to be antialiased | True |
| `text_color` | the color of the text | (0, 0, 0) |
| `font_type` | the font that is going to be used | "comicsans" |
| `font_size` | the size of the font that is going to be used | 60 |

# Example code
```python
# the imports
import pygame
from PygameHelper import Button
from PygameHelper.constants import *


pygame.init()
pygame.font.init()

WIN = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Button")


button = Button(
        WIN,                                                                                    # WIN
        250,                                                                                    # x
        250,                                                                                    # y
        200,                                                                                    # w
        200,                                                                                    # h
        (255, 0, 0),                                                                            # inactive_color
        (200, 0, 0),                                                                            # hover_inactive_color
        (0, 255, 0),                                                                            # active_color
        (0, 200, 0),                                                                            # hover_active_color
        anchor=CENTER,                                                                          # anchor
        text=f"\nHELLO\nWORLD\n",                                                               # text
        on_click=lambda name, age=20: print(f"""hello my name is {name} and i am {age}"""),     # what is going to be called when the button is clicked
        on_click_args=("George", ),                                                             # the positional argument that it can accept
        on_click_kwargs={"age": 20}                                                             # the key-word argument that the function can accept
)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit(-1)
        button.event_handler(event)

    WIN.fill((30, 30, 30))
    button.draw()
    pygame.display.update()
```

# contributions:
---
> Pull requests are welcome!
> Feel free to create a fork of this repository and use the code for any noncommercial purposes.
