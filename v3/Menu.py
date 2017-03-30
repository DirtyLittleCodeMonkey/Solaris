

class Menu:

    def __init__(self, fonts, buttons, title, title_pos):
        self.fonts = fonts
        self.buttons = buttons
        self.title = title
        self.title_pos = title_pos

    def render(self, screen):
        title = self.fonts[7].render(self.title, False, (255, 255, 255))
        title_rect = title.get_rect(center=self.title_pos)
        screen.blit(title, title_rect)