import sys
import threading

import pygame

from object_capturer import objectCapturer
from pong.game_better import Pong

def capturer_loop(capturer):
    while not objectCapturer.is_video_done:
        pointL, pointR = objectCapturer.get_locations()

        if pointL is not None:
            transformedL = (pointL[1] / objectCapturer.calibrated_height) * 1080
            pong.pad1_pos.center = (pong.pad1_pos.center[0], transformedL)
        if pointR is not None:
            transformedR = (pointR[1] / objectCapturer.calibrated_height) * 1080
            pong.pad2_pos.center = (pong.pad2_pos.center[0], transformedR)


if __name__ == "__main__":
    objectCapturer = objectCapturer()

    pong = Pong()

    threading.Thread(target=capturer_loop, args=[objectCapturer]).start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        pong.update()
        pong.draw()
        pygame.display.update()

        pong.FPS_CLOCK.tick(120)
