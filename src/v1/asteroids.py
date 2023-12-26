import pyglet
from game import load, player

game_window = pyglet.window.Window(800, 600)


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


main_batch = pyglet.graphics.Batch()

level_label = pyglet.text.Label(
    text="My Amazing Game",
    x=game_window.width // 2,
    y=game_window.height // 2,
    anchor_x="center",
    batch=main_batch,
)

player_ship = player.Player(x=400, y=300, batch=main_batch)

game_window.push_handlers(player_ship)
game_window.push_handlers(player_ship.key_handler)

asteroids = load.asteroids(3, player_ship.position, batch=main_batch)
player_lives = load.player_lives(5, batch=main_batch)
score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)


game_objects = [player_ship] + asteroids


def update(dt):
    check_collisions(game_objects)
    remove_dead_objects(game_objects)

    new_objects = []
    for obj in game_objects:
        obj.update(dt)
        new_objects.extend(obj.new_objects)
        obj.new_objects = []

    game_objects.extend(new_objects)


def check_collisions(game_objects):
    for i in range(len(game_objects)):
        for j in range(i + 1, len(game_objects)):
            obj_1 = game_objects[i]
            obj_2 = game_objects[j]

            if not obj_1.dead and not obj_2.dead:
                if obj_1.collides_with(obj_2):
                    obj_1.handle_collision_with(obj_2)
                    obj_2.handle_collision_with(obj_1)


def remove_dead_objects(game_objects):
    dead = [obj for obj in game_objects if obj.dead]
    for obj in dead:
        obj.delete()
        game_objects.remove(obj)


pyglet.clock.schedule_interval(update, 1 / 120.0)


if __name__ == "__main__":
    pyglet.app.run()
