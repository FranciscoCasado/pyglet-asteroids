import math

from pyglet.window import key

from game.resources import player_image
from game.physical_object import PhysicalObject


class Player(PhysicalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(img=player_image, *args, **kwargs)
        self.thrust = 300.0
        self.rotate_speed = 200.0
        self.keys = dict(left=False, right=False, up=False, down=False)

    def on_key_press(self, symbol, modifiers):
        match symbol:
            case key.UP:
                self.keys["up"] = True
            case key.DOWN:
                self.keys["down"] = True
            case key.LEFT:
                self.keys["left"] = True
            case key.RIGHT:
                self.keys["right"] = True

    def on_key_release(self, symbol, modifiers):
        match symbol:
            case key.UP:
                self.keys["up"] = False
            case key.DOWN:
                self.keys["down"] = False
            case key.LEFT:
                self.keys["left"] = False
            case key.RIGHT:
                self.keys["right"] = False

    def update(self, dt):
        super(Player, self).update(dt)

        if self.keys["left"]:
            self.rotation -= self.rotate_speed * dt
        if self.keys["right"]:
            self.rotation += self.rotate_speed * dt

        if self.keys["up"]:
            self._accelerate(dt)
        if self.keys["down"]:
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