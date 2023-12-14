import pygame
import pymunk
class TetrisShape:
    def __init__(self, body: pymunk.Body):
        self._body = body
        self._landed = False
        self._sleep_time = 1000
        self._sleep_start_time = 0
        self._is_sleeping = False
        self._is_done = False
        self._move_speed = 2
        self._dead = False
        self._fall_speed = 200
        self._landed_position = 0, 0
        self._dead_distance = 50
        self._stop_magnitude = 10
        self._landed_mass = 10
        self._landed_friction = 10
        self._landed_collision_type = 1

    def update(self, left_boundary, right_boundary):
        if self._is_done:
            return

        if self._landed:
            now = pygame.time.get_ticks()
            if self._body.velocity.get_length_sqrd() <= self._stop_magnitude:
                if not self._is_sleeping:
                    self._sleep_start_time = now
                    self._is_sleeping = True
            else:
                self._is_sleeping = False

            if self._body.position.get_distance(self._landed_position) > self._dead_distance:
                self._dead = True
                self._is_done = True

            if self._is_sleeping and now - self._sleep_start_time > self._sleep_time:
                self._is_done = True
        else:
            self._body.velocity = 0, self._fall_speed
            self._handle_input(left_boundary, right_boundary)

    def crossed_boundary(self, left_boundary, right_boundary):
        return self._body.position.x <= left_boundary or self._body.position.x >= right_boundary

    def get_height(self):
        return self._body.position.y

    def dead(self):
        return self._dead

    def handle_collisions(self, arbiter: pymunk.arbiter.Arbiter, space, data):
        if self._landed:
            return
        self._landed_position = self._body.position
        self._landed = True
        for shape in self._body.shapes:
            shape.collision_type = self._landed_collision_type
            shape.friction = self._landed_friction
            shape.mass = self._landed_mass

    def is_done(self):
        return self._is_done

    def _handle_input(self, left_boundary, right_boundary):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self._body.position.x > left_boundary:
                self._body.position = self._body.position.x - self._move_speed, self._body.position.y
        elif keys[pygame.K_d]:
            if self._body.position.x < right_boundary:
                self._body.position = self._body.position.x + self._move_speed, self._body.position.y
        pymunk.Space.reindex_shapes_for_body(self._body.space, self._body)

    @staticmethod
    def create_shape(space, vertices, color, x, y, width, height):
        body = pymunk.Body()

        body.position = x, y

        shapes = []
        for v in vertices:
            t = pymunk.transform.Transform(tx=-width * 3 // 2, ty=-height * 3 // 2)
            top_left = v[0] * width, v[1] * height
            top_right = v[0] * width + width, v[1] * height
            bottom_right = v[0] * width + width, v[1] * height + height
            bottom_left = v[0] * width, v[1] * height + height
            shape = pymunk.Poly(body, [top_left, top_right, bottom_right, bottom_left], transform=t)
            shape.mass = 0.1
            shape.friction = 0
            shape.collision_type = 0
            shape.color = color
            shapes.append(shape)

        space.add(body, *shapes)

        return TetrisShape(body)
