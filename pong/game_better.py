import sys

import pygame

WIDTH = 1280
HEIGHT = 720

RADIUS = 10
ACCELERATION = 1.2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Pong:
    def __init__(self):
        self.ball_pos = (int(WIDTH / 2), int(HEIGHT / 2))
        self.direction = (4, 4)
        self.pad1_pos = pygame.Rect(10, int(HEIGHT / 2), 10, 80)
        self.pad2_pos = pygame.Rect(WIDTH - 20, int(HEIGHT / 2), 10, 80)

        self.mousex = 0
        self.mousey = 0

        self.score = (0, 0)

        self.font = pygame.font.Font('freesansbold.ttf', 44)

    def update(self):
        # Move the ball in the specified direction
        self.ball_pos = (self.ball_pos[0] + self.direction[0], self.ball_pos[1] + self.direction[1])

        # If ball intersects with the bottom of the screen
        if self.ball_pos[1] + RADIUS >= HEIGHT:
            self.direction = (self.direction[0], -abs(self.direction[1]))

        # If ball intersects with the top of the screen
        if self.ball_pos[1] - RADIUS <= 0:
            self.direction = (self.direction[0], abs(self.direction[1]))

        # Temporary - set the center height of the paddles as the Y coordinate of the mouse
        self.pad1_pos.center = (self.pad1_pos.center[0], self.mousey)
        self.pad2_pos.center = (self.pad2_pos.center[0], self.mousey)

        # Check if the ball intersects with the left paddle
        if self.ball_pos[1] - RADIUS < self.pad1_pos.bottom and \
                self.ball_pos[1] + RADIUS > self.pad1_pos.top and \
                self.ball_pos[0] - RADIUS < self.pad1_pos.right and \
                self.ball_pos[0] + RADIUS > self.pad1_pos.left:
            self.direction = (abs(self.direction[0]) * ACCELERATION, self.direction[1] * ACCELERATION)

        # Check if the ball intersects with the right paddle
        if self.ball_pos[1] - RADIUS < self.pad2_pos.bottom and \
                self.ball_pos[1] + RADIUS > self.pad2_pos.top and \
                self.ball_pos[0] - RADIUS < self.pad2_pos.right and \
                self.ball_pos[0] + RADIUS > self.pad2_pos.left:
            self.direction = (-abs(self.direction[0]) * ACCELERATION, self.direction[1] * ACCELERATION)

        # Check if ball intersects with the right side of the board
        if self.ball_pos[0] + 10 >= WIDTH:
            self.score = (self.score[0] + 1, self.score[1])
            self.direction = (4, 4)
            self.ball_pos = (int(WIDTH / 2), int(HEIGHT / 2))

        # Check if ball intersects with the left side of the board
        if self.ball_pos[0] - 10 <= 0:
            self.score = (self.score[0], self.score[1] + 1)
            self.direction = (4, 4)
            self.ball_pos = (int(WIDTH / 2), int(HEIGHT / 2))

    def draw(self):
        pygame.draw.circle(DISPLAY, WHITE, (int(self.ball_pos[0]), int(self.ball_pos[1])), RADIUS)
        pygame.draw.rect(DISPLAY, WHITE, self.pad1_pos)
        pygame.draw.rect(DISPLAY, WHITE, self.pad2_pos)

        surf = self.font.render("{}".format(self.score[0]), True, (124, 174, 205))
        DISPLAY.blit(surf, (100, 50))
        surf = self.font.render("{}".format(self.score[1]), True, (124, 174, 205))
        DISPLAY.blit(surf, (WIDTH - 100, 50))


if __name__ == "__main__":
    global DISPLAY

    pygame.init()

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
