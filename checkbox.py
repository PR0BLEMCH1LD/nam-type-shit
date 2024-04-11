import pygame

class CheckBox:
    def __init__(self, checked, size, pos, color, inner_pad=2, border_width=1, border_color=(0, 0, 0)):
        self.checked = checked
        self.size = size
        self.pos = pos
        self.color = color
        self.inner_pad = inner_pad
        self.border_width = border_width
        self.border_color = border_color

        self.cursor_in_area = False

    def render(self, screen, events):
        pygame.draw.rect(screen, self.border_color, (self.pos[0], self.pos[1], self.size, self.size), self.border_width)

        if self.checked:
            pygame.draw.rect(screen, self.color, (self.pos[0] + self.inner_pad, self.pos[1] + self.inner_pad, self.size - 2 * self.inner_pad, self.size - 2 * self.inner_pad))

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                mpos = pygame.mouse.get_pos()

                if mpos[0] >= self.pos[0] and mpos[0] <= self.pos[0] + self.size and mpos[1] >= self.pos[1] and mpos[1] <= self.pos[1] + self.size:
                    self.cursor_in_area = True
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    self.cursor_in_area = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.cursor_in_area:
                    self.checked = not self.checked