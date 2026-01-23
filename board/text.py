from pygame.font import SysFont
class Text():
    def __init__(self, screen):
        self.screen = screen
        self.font = SysFont(None, 48)
    def write(self, message:str="No Message Given", x:int=0, y:int=0, color:tuple=(255, 255, 255), border_color=(0, 0, 0), border_size=2):
        """ Write text with border """
        
        # Render border text in black (or whatever color)
        border_img = self.font.render(message, True, border_color)

        # Draw the border text around the main text
        for dx in range(-border_size, border_size + 1):
            for dy in range(-border_size, border_size + 1):
                if dx == 0 and dy == 0:
                    continue
                self.screen.blit(border_img, (x + dx, y + dy))
        """ Write text """
        image = self.font.render(message, True, color)
        self.screen.blit(image, (round(x), round(y)))