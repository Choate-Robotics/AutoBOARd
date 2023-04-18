import pygame

import config


class Button:
    def __init__(self, x, y, width, height, color, text='', font_size=32, font_color=(0, 0, 0), action=lambda: None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.font_color = font_color
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.font_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def click(self, surface):
        self.action()


class Toggle(Button):
    def __init__(self, x, y, width, height, color, text='', font_size=32, font_color=(0, 0, 0), start_state=False, action=lambda: None):
        super().__init__(x, y, width, height, color, text, font_size, font_color, action)
        self.state = start_state

    def draw(self, surface):
        # Draw border polygon around button
        width = self.rect.width + 10
        height = self.rect.height + 10

        pygame.draw.polygon(surface, (0 if self.state else 255, 255 if self.state else 0, 0), [
            (self.rect.center[0] - width / 2, self.rect.center[1] - height / 2),
            (self.rect.center[0] + width / 2, self.rect.center[1] - height / 2),
            (self.rect.center[0] + width / 2, self.rect.center[1] + height / 2),
            (self.rect.center[0] - width / 2, self.rect.center[1] + height / 2)
        ])
        super().draw(surface)

    def toggle(self, surface):
        self.state = not self.state
        self.draw(surface)

    def click(self, surface):
        self.toggle(surface)
        super().click(surface)


class OptionList(Button):
    def __init__(self, x, y, width, height, color, text='', font_size=32, font_color=(0, 0, 0), states=["Default"], start_state=0, action=lambda: None):
        super().__init__(x, y, width, height, color, text, font_size, font_color, action)
        self.states = states
        self.current_state = start_state
        self.text = self.states[self.current_state]

    def click(self, surface):
        self.current_state = (self.current_state + 1) % len(self.states)
        self.text = self.states[self.current_state]
        self.draw(surface)
        super().click(surface)
