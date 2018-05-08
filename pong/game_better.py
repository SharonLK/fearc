import numpy
import os
import random
import sys

import numpy
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'

WIDTH = 1920
HEIGHT = 1080

ACCELERATION = 1.2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Pong:
    def __init__(self):
        pygame.init()

        self.FPS_CLOCK = pygame.time.Clock()
        self.DISPLAY = pygame.display.set_mode([WIDTH, HEIGHT], pygame.DOUBLEBUF)
        pygame.display.set_caption('FEARC')

        self.ball_poses = [(int(WIDTH / 2), int(HEIGHT / 2))]
        self.radius = 45
        self.directions = [(4, 4)]
        self.pad1_pos = pygame.Rect(30, int(HEIGHT / 2), 60, 200)
        self.pad2_pos = pygame.Rect(WIDTH - 90, int(HEIGHT / 2), 60, 200)

        self.mousex = 0
        self.mousey = 0

        self.score = (0, 0)

        self.font = pygame.font.Font('freesansbold.ttf', 192)

    def update(self):
        # Move the ball in the specified direction
        for i, (pos, direction) in enumerate(zip(self.ball_poses, self.directions)):
            self.ball_poses[i] = (pos[0] + direction[0], pos[1] + direction[1])

            # If ball intersects with the bottom of the screen
            if pos[1] + self.radius >= HEIGHT:
                self.directions[i] = (direction[0], -abs(direction[1]))

            # If ball intersects with the top of the screen
            if pos[1] - self.radius <= 0:
                self.directions[i] = (direction[0], abs(direction[1]))

            # Check if the ball intersects with the left paddle
            if pos[1] - self.radius < self.pad1_pos.bottom and \
                    pos[1] + self.radius > self.pad1_pos.top and \
                    pos[0] - self.radius < self.pad1_pos.right and \
                    pos[0] + self.radius > self.pad1_pos.left:
                self.directions[i] = (abs(direction[0]) * ACCELERATION, direction[1] * ACCELERATION)

            # Check if the ball intersects with the right paddle
            if pos[1] - self.radius < self.pad2_pos.bottom and \
                    pos[1] + self.radius > self.pad2_pos.top and \
                    pos[0] - self.radius < self.pad2_pos.right and \
                    pos[0] + self.radius > self.pad2_pos.left:
                self.directions[i] = (-abs(direction[0]) * ACCELERATION, direction[1] * ACCELERATION)

            self.directions[i] = (numpy.clip(direction[0], -16, 16), numpy.clip(direction[1], -16, 16))

            # Check if ball intersects with the right side of the board
            if pos[0] + self.radius >= WIDTH:
                self.score = (self.score[0] + 1, self.score[1])
                self.directions[i] = (-4, 4)
                self.ball_poses[i] = (int(WIDTH / 2), random.randint(self.radius, HEIGHT - self.radius))

            # Check if ball intersects with the left side of the board
            if pos[0] - self.radius <= 0:
                self.score = (self.score[0], self.score[1] + 1)
                self.directions[i] = (-4, 4)
                self.ball_poses[i] = (int(WIDTH / 2), random.randint(self.radius, HEIGHT - self.radius))

    def draw(self):
        pygame.draw.rect(self.DISPLAY, BLACK, ((0, 0), (WIDTH, HEIGHT)))

        # Draw the ball and bats
        for pos in self.ball_poses:
            pygame.draw.circle(self.DISPLAY, WHITE, (int(pos[0]), int(pos[1])), self.radius)

        pygame.draw.rect(self.DISPLAY, WHITE, self.pad1_pos)
        pygame.draw.rect(self.DISPLAY, WHITE, self.pad2_pos)

        # Draw the boundary
        BORDER_WIDTH = 30
        pygame.draw.rect(self.DISPLAY, WHITE, pygame.Rect(0, 0, BORDER_WIDTH, HEIGHT))
        pygame.draw.rect(self.DISPLAY, WHITE, pygame.Rect(0, 0, WIDTH, BORDER_WIDTH))
        pygame.draw.rect(self.DISPLAY, WHITE, pygame.Rect(WIDTH - BORDER_WIDTH, 0, BORDER_WIDTH, HEIGHT))
        pygame.draw.rect(self.DISPLAY, WHITE, pygame.Rect(0, HEIGHT - BORDER_WIDTH, WIDTH, BORDER_WIDTH))

        # Draw the score
        surf = self.font.render("{}".format(self.score[0]), True, WHITE)
        self.DISPLAY.blit(surf, (200, 75))
        surf = self.font.render("{}".format(self.score[1]), True, WHITE)
        self.DISPLAY.blit(surf, (WIDTH - 270, 75))


if __name__ == "__main__":
    # pygame.init()

    # FPS_CLOCK = pygame.time.Clock()
    # self.DISPLAY = pygame.self.DISPLAY.set_mode([WIDTH, HEIGHT], pygame.DOUBLEBUF)
    # pygame.self.DISPLAY.set_caption('FEARC')

    pong = Pong()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                pong.mousex = event.pos[0]
                pong.mousey = event.pos[1]

        pong.update()

        pygame.draw.rect(self.DISPLAY, BLACK, ((0, 0), (WIDTH, HEIGHT)))
        pong.draw()

        pygame.self.DISPLAY.update()

        FPS_CLOCK.tick(120)
