import math

from pyglet import sprite, clock
from pyglet.window import key

from game.resources import player_image, engine_image, bullet_image
from game.physical_object import PhysicalObject


class Player(PhysicalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(img=player_image, *args, **kwargs)
        self.thrust = 300.0
        self.rotate_speed = 200.0
        self.key_handler = key.KeyStateHandler()
        self.engine_sprite = sprite.Sprite(img=engine_image, *args, **kwargs)
        self.engine_sprite.visible = False
        self.bullet_speed = 700.0
        self.reacts_to_bullets = False

    def update(self, dt):
        super(Player, self).update(dt)
        self.engine_sprite.rotation = self.rotation
        self.engine_sprite.x = self.x
        self.engine_sprite.y = self.y

        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt
        if self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt

        if self.key_handler[key.UP]:
            self._accelerate(dt)
            self.engine_sprite.visible = True
        else:
            self.engine_sprite.visible = False

        if self.key_handler[key.DOWN]:
            self._deaccelerate(dt)

        if self.key_handler[key.SPACE]:
            self.fire()

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

    def delete(self):
        self.engine_sprite.delete()
        super(Player, self).delete()

    def fire(self):
        angle_radians = -math.radians(self.rotation)
        ship_radius = self.image.width / 2
        bullet_x = self.x + math.cos(angle_radians) * ship_radius
        bullet_y = self.y + math.sin(angle_radians) * ship_radius
        new_bullet = Bullet(x=bullet_x, y=bullet_y, batch=self.batch)

        bullet_vx = self.velocity_x + math.cos(angle_radians) * self.bullet_speed
        bullet_vy = self.velocity_y + math.sin(angle_radians) * self.bullet_speed
        new_bullet.velocity_x = bullet_vx
        new_bullet.velocity_y = bullet_vy

        self.new_objects.append(new_bullet)


class Bullet(PhysicalObject):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(img=bullet_image, *args, **kwargs)
        clock.schedule_once(self.die, 0.5)
        self.is_bullet = True

    def die(self, dt):
        self.dead = True
