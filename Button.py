import pygame as pg

class Button:
    
    def __init__(self, color, highlight_color, origin, width, height, text):
        
        self.color = color
        self.base_color = color
        self.highlight_color = highlight_color
        self.x = origin[0]
        self.y = origin[1]
        self.width = width
        self.height = height
        self.text = text
        
    def render(self, surface):
        pg.draw.rect(surface, (0,0,0), (self.x-2, self.y-2, self.width+4, self.height+4))
        pg.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        font = pg.font.SysFont("Arial", 18)
        text_obj = font.render(self.text, True, (0,0,0))
        surface.blit(text_obj, (self.x+6, self.y+4))
        
    def mouse_above_button(self, mouse_pos):
        if (
            mouse_pos[0] >= self.x and mouse_pos[0] <= self.x + self.width
            and mouse_pos[1] >= self.y and mouse_pos[1] <= self.y + self.height
            ):
            self.color = self.highlight_color
            return True
        else:
            self.color = self.base_color
            return False
            