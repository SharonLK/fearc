import sys

import pygame

WIDTH = 1280
HEIGHT = 720

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Pong:
    def __init__(self):
        self.ball_pos = (int(WIDTH / 2), int(HEIGHT / 2))
        self.direction = (1, 1)
        self.pad1_pos = pygame.Rect(10, int(HEIGHT / 2), 10, 80)
        self.pad2_pos = pygame.Rect(WIDTH - 20, int(HEIGHT / 2), 10, 80)

        self.mousex = 0
        self.mousey = 0

    def update(self):
        self.ball_pos = (self.ball_pos[0] + self.direction[0], self.ball_pos[1] + self.direction[1])

        self.pad1_pos.center = (self.pad1_pos.center[0], self.mousey)
        self.pad2_pos.center = (self.pad2_pos.center[0], self.mousey)

        if self.ball_pos[1] - 10 < self.pad1_pos.bottom and \
                                self.ball_pos[1] + 10 > self.pad1_pos.top and \
                                self.ball_pos[0] - 10 < self.pad1_pos.right and \
                                self.ball_pos[0] + 10 > self.pad1_pos.left:
            self.direction = (-abs(self.direction[0]), self.direction[1])

    def draw(self):
        pygame.draw.circle(DISPLAY, WHITE, self.ball_pos, 10)
        pygame.draw.rect(DISPLAY, WHITE, self.pad1_pos)
        pygame.draw.rect(DISPLAY, WHITE, self.pad2_pos)


if __name__ == "__main__":
    global DISPLAY

    FPS_CLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('FEARC')

    pong = Pong()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                pong.mousex = event.pos[0]
                pong.mousey = event.pos[1]

        pong.update()

        pygame.draw.rect(DISPLAY, BLACK, ((0, 0), (WIDTH, HEIGHT)))
        pong.draw()

        pygame.display.update()

        FPS_CLOCK.tick(60)
