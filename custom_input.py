import pygame, pygame_textinput

class CustomInput:
    def __init__(self, font, text, pos, inner_pad_x=8, inner_pad_y=4, border_width=1, border_color=(0, 0, 0)):
        self.font = font
        self.pos = pos
        self.inner_pad_x = inner_pad_x
        self.inner_pad_x = inner_pad_x
        self.inner_pad_y = inner_pad_y
        self.border_width = border_width
        self.border_color = border_color

        self.manager = pygame_textinput.TextInputManager(text)
        self.text_input = pygame_textinput.TextInputVisualizer(manager=self.manager, font_object=font, antialias=False)
        self.manager.cursor_pos = len(self.manager.value)

        self.active = False
        self.value = self.text_input.value
        self.cursor_in_area = False

    def render(self, screen, events):
        if self.active:
            self.text_input.update(events)
            self.value = self.text_input.value
            screen.blit(self.text_input.surface, self.pos)
        else:
            screen.blit(self.font.render(self.value, False, self.text_input.font_color), self.pos)

        text_width = self.font.size(self.value)[0]
        text_height = self.font.get_height()

        pygame.draw.rect(screen, self.border_color, (self.pos[0] - self.inner_pad_x, self.pos[1] - self.inner_pad_y, text_width + 2 * self.inner_pad_x, text_height + 2 * self.inner_pad_y), self.border_width)

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mpos = pygame.mouse.get_pos()
                
                if mpos[1] >= self.pos[1] and mpos[1] <= self.pos[1] + text_height and mpos[0] >= self.pos[0] - self.inner_pad_x and mpos[0] <= self.pos[0] + text_width + self.inner_pad_x:
                    self.cursor_in_area = True
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                else:
                    self.cursor_in_area = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                
                if self.cursor_in_area:
                    self.active = True

                    if self.value == "":
                        break

                    font_width = text_width // len(self.value)
                    self.manager.cursor_pos = (int((mpos[0] - self.pos[0]) / (font_width / 2)) + 1) // 2
                else:
                    self.active = False