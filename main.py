import pygame
import math
import time

# TODO change utils function signature
from utils import BACKGROUND, TRACK, WIDTH, HEIGHT, FPS, FINISH_LINE, TRACK_HITBOX, PATH, FINISH_LINE_HITBOX

from racecar import RaceCar, ManualCar, AutomatedCar


# ----------- helper functions -----------
def check_for_collision(car: RaceCar):
    if car.collide(TRACK_HITBOX) is not None:
        car.invert_velocity_direction()
    else:
        car.move()


def move_manual_car(car: RaceCar, up=pygame.K_w, left=pygame.K_a, down=pygame.K_s, right=pygame.K_d):
    # for arrow keys use K_LEFT, K_RIGHT, K_UP, K_DOWN

    keys = pygame.key.get_pressed()

    if keys[left]:
        car.steer(-5 * math.pi / 180)
    elif keys[right]:
        car.steer(5 * math.pi / 180)
    else:
        car.steer(0)
    if keys[down]:
        car.accelerate(-60)
    elif keys[up]:
        car.accelerate(60)
    else:
        car.accelerate(math.copysign(10, -car.vel))


def print_lap_times():
    for i in range(1, 4):
        lap_time = timestamps[i] - timestamps[i - 1]
        print(f'{i}. round: {int(lap_time // 60)} minutes and {int(lap_time % 60)} seconds')
    total = timestamps[3] - timestamps[0]
    print(f'total time: {int(total // 60)} minutes and {int(total % 60)} seconds')


if __name__ == '__main__':
    pygame.display.set_caption("Project Racecar")
    clock = pygame.time.Clock()
    images = [(BACKGROUND, (0, 0)), (TRACK, (0, 0)), (FINISH_LINE, (0, 0))]
    win = pygame.display.set_mode((WIDTH, HEIGHT))

    manual_car = ManualCar(start=(570, 10))
    automated_car = AutomatedCar(start=(570, 30), path=PATH)

    laps = -1
    # timestamps[0] -> starting time, timestamps[i] i in [1,3] -> lap times
    timestamps = [0 for x in range(4)]
    crossed_finishing_line = True

    run = True

    while run:
        clock.tick(FPS)

        for img, pos in images:
            win.blit(img, pos)

        automated_car.draw(win)
        manual_car.draw(win)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        move_manual_car(manual_car)

        check_for_collision(manual_car)
        check_for_collision(automated_car)

        finished = manual_car.collide(FINISH_LINE_HITBOX)

        if finished is not None:
            if crossed_finishing_line:
                laps += 1
                crossed_finishing_line = False
                # update lap time array

                timestamps[laps] = time.time()

        else:
            crossed_finishing_line = True

        if laps == 3:
            run = False
            print("finished")

    pygame.quit()
    print_lap_times()
