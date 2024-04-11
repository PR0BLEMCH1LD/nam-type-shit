import pygame

class Button:
    def __init__(self, disabled, font, text, pos, color, text_color=(0, 0, 0), inner_pad_x=10, inner_pad_y=7, border_width=1, border_color=(0, 0, 0), border_radius=4):
        self.disabled = disabled
        self.font = font
        self.text = text
        self.pos = pos
        self.color = color
        self.text_color = text_color
        self.inner_pad_x = inner_pad_x
        self.inner_pad_y = inner_pad_y
        self.border_width = border_width
        self.border_color = border_color
        self.border_radius = border_radius
        
        self.pressed = False
        self.cursor_in_area = False
    
    def render(self, screen, events):
        if self.pressed:
            self.pressed = False

        text_width = self.font.size(self.text)[0]
        text_height = self.font.get_height()

        if self.disabled:
            color = (233, 236, 239)
            text_color = (173, 181, 189)
        else:
            color = self.color
            text_color = self.text_color

        pygame.draw.rect(screen, color, (self.pos[0] - self.inner_pad_x, self.pos[1] - self.inner_pad_y, text_width + 2 * self.inner_pad_x, text_height + 2 * self.inner_pad_y), border_radius=self.border_radius)
        pygame.draw.rect(screen, self.border_color, (self.pos[0] - self.inner_pad_x, self.pos[1] - self.inner_pad_y, text_width + 2 * self.inner_pad_x, text_height + 2 * self.inner_pad_y), self.border_width, self.border_radius)
        screen.blit(self.font.render(self.text, False, text_color), self.pos)

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mpos = pygame.mouse.get_pos()

                if mpos[0] >= self.pos[0] - self.inner_pad_x and mpos[0] <= self.pos[0] + text_width + self.inner_pad_x and mpos[1] >= self.pos[1] - self.inner_pad_y and mpos[1] <= self.pos[1] + text_height + self.inner_pad_y:
                    self.cursor_in_area = True
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    self.cursor_in_area = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.cursor_in_area and not self.disabled:
                    self.pressed = True