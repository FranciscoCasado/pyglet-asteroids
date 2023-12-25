import pyglet
from game import resources, load, player

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
    for obj in game_objects:
        obj.update(dt)


pyglet.clock.schedule_interval(update, 1 / 120.0)


if __name__ == "__main__":
    pyglet.app.run()
