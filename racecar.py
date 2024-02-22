from utils import FPS, GameObject, REDCAR, YELLOWCAR

import math
import pygame


# helper functions
def clip(value: float, maximum: float, minimum: float) -> float:
    # check for valid value
    if value > maximum:
        value = maximum
    elif value < minimum:
        value = minimum
    return value


# Task 1
class RaceCar(GameObject):
    def __init__(self, max_vel: float = 300, max_acc: float = 100, max_delta: float = 10 * math.pi / 180):
        # private class member initialized via parameter with defaults
        self.__max_vel = max_vel
        self.__max_acc = max_acc
        self.__max_delta = max_delta

        # private class member initialized to value
        self.__l_r = 1.738
        self.__l_f = 1.738
        self.__c_w = 0.001
        self.__rho = 0.01

        self.__T_s = 1 / FPS

        # public class member initialized to value
        self.vel = 0
        self.psi = 0
        self.beta = 0
        self.acc = 0

        # abstract initialized by derived class
        self.pos_y = self.y_start
        self.pos_x = self.x_start

        super().__init__()

    def steer(self, delta: float) -> None:
        # check for valid delta value
        delta = clip(delta, self.__max_delta, -self.__max_delta)

        # calculate beta
        self.beta = math.atan((self.__l_r / (self.__l_f + self.__l_r)) * math.tan(delta))

    def accelerate(self, acc: float) -> None:
        # check for valid acceleration value
        acc = clip(acc, self.__max_acc, -self.__max_acc)

        # update current acceleration
        self.acc = acc

    def move(self) -> None:
        # update current velocity
        self.vel += self.__T_s * (
                self.acc - math.copysign(self.__rho * math.fabs(self.vel) + self.__c_w * self.vel ** 2, self.vel))
        # check for valid velocity
        self.vel = clip(self.vel, self.__max_vel, -self.__max_vel)

        # update car orientation and car position
        self.psi += self.__T_s * (self.vel / self.__l_r) * math.sin(self.beta)
        self.pos_x += self.__T_s * self.vel * math.cos(self.psi + self.beta)
        self.pos_y += self.__T_s * self.vel * math.sin(self.psi + self.beta)

    def collide(self, mask: pygame.Mask) -> tuple:
        hitbox_car = pygame.mask.from_surface(self.image, threshold=128)

        offset = (int(self.pos_x), int(self.pos_y))
        # overlap returns point of intersection
        collision_point = mask.overlap(hitbox_car, offset)
        return collision_point

    def invert_velocity_direction(self):
        self.vel = (1 / 2) * (-self.vel)
        self.move()


class ManualCar(RaceCar):
    def __init__(self, start: tuple):
        self.x_start = start[0]
        self.y_start = start[1]
        self.image = YELLOWCAR
        super().__init__()


# Task 2
class AutomatedCar(RaceCar):
    def __init__(self, start: tuple, path: [tuple] = []):
        self.__path = path
        self.__current_point = 0
        self.x_start = start[0]
        self.y_start = start[1]
        self.image = REDCAR
        super().__init__()

    def draw_points(self, win: pygame.Surface) -> None:
        for p in self.__path:
            pygame.draw.circle(win, color=(0, 0, 0), center=p, radius=4)

    def draw(self, win: pygame.Surface) -> None:
        self.draw_points(win)
        super().draw(win)

    def update_current_point(self) -> None:
        distance = math.sqrt((self.__path[self.__current_point][0] - self.pos_x) ** 2 + (
                self.__path[self.__current_point][1] - self.pos_y) ** 2)

        if distance < 10:
            self.__current_point += 1

        self.__current_point %= len(self.__path)

    def steering_control(self) -> None:
        point_x, point_y = self.__path[self.__current_point]
        err_x = point_x - self.pos_x
        err_y = point_y - self.pos_y

        desired_psi = math.atan2(err_y, err_x)

        err_psi = desired_psi - self.psi
        while err_psi >= math.pi:
            err_psi -= 2 * math.pi
        while err_psi < -math.pi:
            err_psi += 2 * math.pi

        k_p = 0.75
        self.steer(k_p * err_psi)

    def acceleration_control(self) -> None:
        a_const = 50
        self.accelerate(a_const)

    def move(self) -> None:
        self.update_current_point()
        self.steering_control()
        self.acceleration_control()
        super().move()
