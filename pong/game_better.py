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

        self.ball_poses = []
        self.radius = 100
        self.directions = []
        self.pad1_pos = pygame.Rect(30, int(HEIGHT / 2), 60, 200)
        self.pad2_pos = pygame.Rect(WIDTH - 90, int(HEIGHT / 2), 60, 200)

        self.bonuses = []

        self.score = (0, 0)

        self.font = pygame.font.Font('freesansbold.ttf', 192)

        self._reset_balls()

    def _reset_balls(self):
        self.ball_poses.clear()
        self.directions.clear()

        choices = [4, -4]

        for i in range(1):
            self.ball_poses.append((int(WIDTH / 2), random.randint(self.radius, HEIGHT - self.radius)))
            self.directions.append((choices[random.randint(0, 1)], choices[random.randint(0, 1)]))

    def _add_bonus(self):
        self.bonuses.append((random.randint(200, WIDTH - 200), random.randint(200, HEIGHT - 200)))

    def update(self):
        # Move the ball in the specified direction
        for i in range(len(self.ball_poses)):
            self.ball_poses[i] = (self.ball_poses[i][0] + self.directions[i][0], self.ball_poses[i][1] + self.directions[i][1])

            # If ball intersects with the bottom of the screen
            if self.ball_poses[i][1] + self.radius >= HEIGHT:
                self.directions[i] = (self.directions[i][0], -abs(self.directions[i][1]))

            # If ball intersects with the top of the screen
            if self.ball_poses[i][1] - self.radius <= 0:
                self.directions[i] = (self.directions[i][0], abs(self.directions[i][1]))

            # Check if the ball intersects with the left paddle
            if self.ball_poses[i][1] - self.radius < self.pad1_pos.bottom and \
                    self.ball_poses[i][1] + self.radius > self.pad1_pos.top and \
                    self.ball_poses[i][0] - self.radius < self.pad1_pos.right and \
                    self.ball_poses[i][0] + self.radius > self.pad1_pos.left:
                self.directions[i] = (abs(self.directions[i][0]) * ACCELERATION, self.directions[i][1] * ACCELERATION)
                if random.randint(0, 3) == 0:
                    self._add_bonus()

            # Check if the ball intersects with the right paddle
            if self.ball_poses[i][1] - self.radius < self.pad2_pos.bottom and \
                    self.ball_poses[i][1] + self.radius > self.pad2_pos.top and \
                    self.ball_poses[i][0] - self.radius < self.pad2_pos.right and \
                    self.ball_poses[i][0] + self.radius > self.pad2_pos.left:
                self.directions[i] = (-abs(self.directions[i][0]) * ACCELERATION, self.directions[i][1] * ACCELERATION)
                if random.randint(0, 3) == 0:
                    self._add_bonus()

            self.directions[i] = (numpy.clip(self.directions[i][0], -16, 16), numpy.clip(self.directions[i][1], -16, 16))

            choices = [4, -4]

            # Check if ball intersects with the right side of the board
            if self.ball_poses[i][0] + self.radius >= WIDTH:
                self.score = (self.score[0] + 1, self.score[1])
                self.directions[i] = (choices[random.randint(0, 1)], choices[random.randint(0, 1)])
                self.ball_poses[i] = (int(WIDTH / 2), random.randint(self.radius, HEIGHT - self.radius))

            # Check if ball intersects with the left side of the board
            if self.ball_poses[i][0] - self.radius <= 0:
                self.score = (self.score[0], self.score[1] + 1)
                self.directions[i] = (choices[random.randint(0, 1)], choices[random.randint(0, 1)])
                self.ball_poses[i] = (int(WIDTH / 2), random.randint(self.radius, HEIGHT - self.radius))

            for bonus_pos in self.bonuses:
                dist_squared = (self.ball_poses[i][0] - bonus_pos[0]) ** 2 + (self.ball_poses[i][1] - bonus_pos[1]) ** 2
                if (self.radius - self.radius / 2) ** 2 <= dist_squared <= (self.radius + self.radius / 2) ** 2:
                    self.bonuses.remove(bonus_pos)

    def draw(self):
        pygame.draw.rect(self.DISPLAY, BLACK, ((0, 0), (WIDTH, HEIGHT)))

        # Draw the ball and bats
        for pos in self.ball_poses:
            pygame.draw.circle(self.DISPLAY, WHITE, (int(pos[0]), int(pos[1])), self.radius)

        for pos in self.bonuses:
            pygame.draw.circle(self.DISPLAY, WHITE, (int(pos[0]), int(pos[1])), int(self.radius / 2))

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
