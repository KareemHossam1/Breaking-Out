import pyglet
from pyglet import window
import pymunk
from pymunk.pyglet_util import DrawOptions
from pymunk.vec2d import Vec2d
import random
global dx, dy
# Variables
start = True
bricks, bricksPy = [], []
x, y = 0, 575
direction = Vec2d(random.choice([(50, 500), (100, 500), (-50, 500), (-100, 500)]))
collision_types = {
    "ball": 1,
    "brick": 2,
    "bottom": 3,
    "paddle": 4
}
# Loading photos
backGround = pyglet.resource.image('image-2.png')
icon = pyglet.image.load('icon.png')
paddle_image = pyglet.image.load('output-onlinepngtools.png')
Brick_image = pyglet.image.load('PURPLEBRICK.png')
game_over = pyglet.image.load('GAME OVER.png')
# Loading media
# smash sound
smashSound = pyglet.media.load('Smashing-Yuri_Santana-1233262689 (mp3cut.net).mp3')
smash = pyglet.media.Player()
smash.queue(smashSound)
smash.volume = 1
# Background soundtrack
backMusic = pyglet.media.load('Back music.mp3')
player = pyglet.media.Player()
player.queue(backMusic)
player.loop = True
player.volume = 0.5
player.play()
# Window
window = pyglet.window.Window(630, 600, "Breakout", style=window.Window.WINDOW_STYLE_DIALOG)
window.set_icon(icon)

########################################################################################################################
# pymunk Section
space = pymunk.Space()
space.gravity = (0, 0)
# Creating and removing objects functions


def create_ball(space):
    shape = pymunk.Circle(None, 10)
    body = pymunk.Body(1, pymunk.inf, body_type=pymunk.Body.DYNAMIC)
    shape.body = body
    shape.elasticity = 0.98
    shape.color = (65, 56, 72, 255)
    body.position = (315, 60)
    space.add(body, shape)
    shape.collision_type = collision_types["ball"]
    return shape


def create_paddle(space):
    shape = pymunk.Poly.create_box(None, (130, 30))
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    shape.body = body
    shape.elasticity = 0.98
    body.position = (315, 35)
    space.add(body, shape)
    shape.collision_type = collision_types["paddle"]
    return shape


def create_wall(space, pos1, pos2):
    shape = pymunk.Segment(space.static_body, pos1, pos2, 2)
    shape.elasticity = 0.98
    shape.color = (21, 163, 169, 255)
    shape.collision_type = collision_types["bottom"]
    space.add(shape)
    return shape


def create_brick(space, pos_x, pos_y):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (pos_x+45, pos_y+10)
    shape = pymunk.Poly.create_box(body, (88, 21))
    shape.elasticity = 0.98
    space.add(body, shape)
    shape.collision_type = collision_types["brick"]
    return shape


def remove_brick(arbiter, space, data):
    block_shape = arbiter.shapes[0]
    space.remove(block_shape, block_shape.body)
    bricksPy.remove(block_shape)
    smash.play()
    smash.queue(smashSound)


# Creating walls
left_wall = create_wall(space, (5, 50), (5, window.height))
up_wall = create_wall(space, (5, window.height), (window.width, window.height))
right_wall = create_wall(space, (window.width-5, window.height), (window.width-5, 50))
# Creating objects
ballPy = create_ball(space)


def const_velocity(body, gravity, damping, dt):
    ballPy.body.velocity = body.velocity.normalized()*500


ballPy.body.velocity_func = const_velocity
paddle = pyglet.sprite.Sprite(paddle_image, x=250, y=20)
paddlePy = create_paddle(space)
for i in range(5):
    for j in range(7):
        brickPy = create_brick(space, x, y)
        bricksPy.append(brickPy)
        x += 90
    y -= 25
    x = 0
# Handle collisions
handler = space.add_collision_handler(collision_types["brick"], collision_types["ball"])
handler.separate = remove_brick
########################################################################################################################
options = DrawOptions()
batch = pyglet.graphics.Batch()
# Events


@window.event
def on_text_motion(motion):
    if motion == pyglet.window.key.MOTION_RIGHT and paddle.x < 500:
        paddlePy.body.position += (10, 0)
        paddle.update(x=paddlePy.body.position.x-65)
        if start:
            ballPy.body.position += (10, 0)

    elif motion == pyglet.window.key.MOTION_LEFT and paddle.x > 0:
        paddlePy.body.position -= (10, 0)
        paddle.update(x=paddlePy.body.position.x-65)
        if start:
            ballPy.body.position -= (10, 0)


@window.event
def on_key_press(symbol, modifiers):
    global start
    if symbol == pyglet.window.key.SPACE and start:
        start = False
        ballPy.body.apply_impulse_at_local_point(direction)


@window.event
def on_draw():
    window.clear()
    backGround.blit(0, 0)
    batch.draw()
    space.debug_draw(options)
    paddle.draw()
    for brick in range(len(bricksPy)):
        brick_image = pyglet.sprite.Sprite(Brick_image, x=bricksPy[brick].body.position.x-44, y=bricksPy[brick].body.position.y-10)
        bricks.append(brick_image)
        brick_image.draw()
    if ballPy.body.position.y < 40:
        game_over.blit(180, 200)
# Let's go


def update(dt):
    space.step(dt)


pyglet.clock.schedule_interval(update, 1.0/60)
pyglet.app.run()
