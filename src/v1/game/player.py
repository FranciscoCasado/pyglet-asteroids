import math

from pyglet.window import key

from game.resources import player_image
from game.physical_object import PhysicalObject


class Player(PhysicalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(img=player_image, *args, **kwargs)
        self.thrust = 300.0
        self.rotate_speed = 200.0
        self.key_handler = key.KeyStateHandler()

    def update(self, dt):
        super(Player, self).update(dt)

        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt
        if self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt

        if self.key_handler[key.UP]:
            self._accelerate(dt)
        if self.key_handler[key.DOWN]:
            self._deaccelerate(dt)

    def _accelerate(self, dt):
        angle_radians = -math.radians(self.rotation)
        force_x = math.cos(angle_radians) * self.thrust * dt
        force_y = math.sin(angle_radians) * self.thrust * dt
        self.velocity_x += force_x
        self.velocity_y += force_y

    def _deaccelerate(self, dt):
        angle_radians = -math.radians(self.rotation)
        force_x = math.cos(angle_radians) * self.thrust * dt
        force_y = math.sin(angle_radians) * self.thrust * dt
        self.velocity_x -= force_x
        self.velocity_y -= force_y
