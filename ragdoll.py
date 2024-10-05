import pygame
import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import DrawOptions
import math

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Human Body Physics Simulation")

# Set up Pymunk space
space = pymunk.Space()
draw_options = DrawOptions(screen)
space.gravity = 0, 980.0  # Set gravity (adjust as needed)

# Create ground
ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
ground_shape = pymunk.Segment(ground_body, (0, height-5), (width, height-5), 10)
ground_shape.friction = 1.0
ground_shape.color = (45, 215, 67, 255)
space.add(ground_body, ground_shape)

# Ceilling
ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
ground_shape = pymunk.Segment(ground_body, (0, -5), (width, -5), 10)
ground_shape.friction = 1.0
ground_shape.color = (45, 215, 67, 255)
space.add(ground_body, ground_shape)

# Left Wall
ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
ground_shape = pymunk.Segment(ground_body, (0, height-5), (0, -5), 10)
ground_shape.friction = 1.0
ground_shape.color = (45, 215, 67, 255)
space.add(ground_body, ground_shape)

# Right Wall
ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
ground_shape = pymunk.Segment(ground_body, (width, height-5), (width, -5), 10)
ground_shape.friction = 1.0
ground_shape.color = (45, 215, 67, 255)
space.add(ground_body, ground_shape)

# Function to create a limb
def create_limb(space, parent_body, mass, start, end, rad, jstart, jend, ang, color):
    limb_body = pymunk.Body()
    limb_body.position = parent_body.position
    limb_shape = pymunk.Segment(limb_body, start, end, rad)
    limb_shape.filter = pymunk.ShapeFilter(group=1)
    limb_shape.mass = mass
    limb_shape.color = color
    space.add(limb_body, limb_shape)

    # Create a pivot joint to connect the limb to the parent body
    joint = pymunk.PinJoint(parent_body, limb_body, jstart, jend)
    joint._set_distance(0)
    joint._set_max_force(float("inf"))
    space.add(joint)

    # Create a rotary limit joint to constrain the rotation of the limb
    limit = pymunk.RotaryLimitJoint(parent_body, limb_body, -ang, ang)
    space.add(limit)

    return limb_body

# Create a simple 2D human body with limbs
head = pymunk.Body()
head.position = (200, 300)
head_shape = pymunk.Circle(head, 20)
head_shape.filter = pymunk.ShapeFilter(group=1)
head_shape.mass = 1
head_shape.color = (255, 0, 0, 255)
space.add(head, head_shape)

torso = create_limb(space, head, 15, (0,0), (0, 60), 30, (0,20), (0,-30), 0.5, (0,255,0,255))

left_arm = create_limb(space, torso, 2, (-15,0), (-15, 30), 10, (-30,-10), (-15,-10), 2, (0,0,255,255))
left_hand = create_limb(space, left_arm, 1, (0,0), (0, 30), 7, (-15,35), (0,-10), 1, (0,255,255,255))

right_arm = create_limb(space, torso, 2, (15,0), (15, 30), 10, (30,-10), (15,-10), 2, (0,0,255,255))
right_hand = create_limb(space, right_arm, 1, (0,0), (0, 30), 7, (15,35), (0,-10), 1, (0,255,255,255))

left_leg = create_limb(space, torso, 3, (-15,80), (-15, 120), 15, (-15,70), (-15,60), 1, (255,0,255,255))
left_feet = create_limb(space, left_leg, 2, (0,0), (0, 55), 12, (-15,130), (0,-10), 1, (255,255,0,255))

right_leg = create_limb(space, torso, 3, (15,80), (15, 120), 15, (15,70), (15,60), 1, (255,0,255,255))
right_feet = create_limb(space, right_leg, 2, (0,0), (0, 55), 12, (15,130), (0,-10), 1, (255,255,0,255))



# Pygame clock
clock = pygame.time.Clock()

running = True
dragged_body = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            mouse_position = Vec2d(x, y)
            body = space.point_query_nearest(mouse_position, 10, pymunk.ShapeFilter())
            if body:
                dragged_body = body.shape.body
                dragged_body._set_type(pymunk.Body.KINEMATIC)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if dragged_body:
                dragged_body._set_type(pymunk.Body.DYNAMIC)
            dragged_body = None

    # Drag the body with the mouse
    if dragged_body:
        x, y = pygame.mouse.get_pos()
        x, y = max(0, min(x, width)), max(0, min(y, height))
        mouse_position = Vec2d(x, y)
        dragged_body.position = mouse_position

    screen.fill((50, 50, 50))
    space.debug_draw(draw_options)
    
    # Step the simulation
    dt = 1.0 / 60.0
    space.step(dt)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
