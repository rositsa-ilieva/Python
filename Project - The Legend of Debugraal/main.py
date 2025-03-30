import pygame
import sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('The Legend of Debugraal')
        self.clock = pygame.time.Clock()

        self.level = Level()

        main_sound = pygame.mixer.Sound('images/audio/main_sound.ogg')
        main_sound.set_volume(0.1)
        main_sound.play(loops = -1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()

            self.screen.fill(COVERAGE_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
