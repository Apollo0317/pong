```python
#screen
pygame.display.setmode(Tuple[int,int]): # init a screen with a given size

#load and scale
player = pygame.transform.scale(
    pygame.image.load('player.png').convert(),
    (SPRITE_WIDTH, SPRITE_HEIGHT)   
)

#move an image
Surface.blit(source, dest, area=None, special_flags=0) -> Rect

#clock
clock = pygame.time.Clock() #get a pygame clock object
```