from pyglet import clock

from game.resources import bullet_image
from game.physical_object import PhysicalObject


class Bullet(PhysicalObject):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(img=bullet_image, *args, **kwargs)
        clock.schedule_once(self.die, 0.5)
        self.is_bullet = True

    def die(self, dt):
        self.dead = True
