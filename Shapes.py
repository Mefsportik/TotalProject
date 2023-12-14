import pygame
import pymunk


class TetrisShape:
    def __init__(self, body: pymunk.Body):
        self._body = body  # Экземпляр тела Pymunk, представляющий фигуру Тетриса.
        self._landed = False  # Флаг, указывающий, приземлилась ли фигура.
        self._sleep_time = 1000  # Время ожидания после приземления перед завершением жизненного цикла.
        self._sleep_start_time = 0  # Время начала ожидания после приземления.
        self._is_sleeping = False  # Флаг, указывающий, находится ли фигура в состоянии ожидания.
        self._is_done = False  # Флаг,указывающий,завершен ли жизненный цикл фигуры.
        self._move_speed = 2
        self._dead = False  # Флаг, указывающий, мертва ли фигура.
        self._fall_speed = 200  # Скорость падения фигуры.
        self._landed_position = 0, 0  # Позиция, на которой фигура приземлилась.
        self._dead_distance = 50  # Расстояние, после которого фигура считается мертвой.
        self._stop_magnitude = 10  # Минимальная скорость, при которой фигура считается остановившейся.
        self._landed_mass = 10  # Масса фигуры после приземления.
        self._landed_friction = 10  # Коэффициент трения фигуры после приземления.
        self._landed_collision_type = 1  # Тип столкновения для приземленной фигуры.

    def update(self, left_boundary, right_boundary):
        # Метод для обновления состояния фигуры.
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
        # Проверяет, пересекла ли фигура указанные границы.
        return self._body.position.x <= left_boundary or self._body.position.x >= right_boundary

    def get_height(self):
        # Возвращает текущую высоту фигуры.
        return self._body.position.y

    def dead(self):
        # Возвращает True, если фигура мертва.
        return self._dead

    def handle_collisions(self, arbiter: pymunk.arbiter.Arbiter, space, data):
        # Обрабатывает столкновения для фигуры(создается при начале столкновения и сохраняются до тех пор, пока не будет столкновений).
        if self._landed:
            return
        self._landed_position = self._body.position
        self._landed = True
        for shape in self._body.shapes:
            shape.collision_type = self._landed_collision_type
            shape.friction = self._landed_friction
            shape.mass = self._landed_mass

    def is_done(self):
        # Возвращает True, если жизненный цикл фигуры завершен.
        return self._is_done

    def _handle_input(self, left_boundary, right_boundary):
        # Приватный метод для обработки ввода пользователя.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self._body.position.x > left_boundary:
                self._body.position = self._body.position.x - self._move_speed, self._body.position.y
        elif keys[pygame.K_d]:
            if self._body.position.x < right_boundary:
                self._body.position = self._body.position.x + self._move_speed, self._body.position.y
        pymunk.Space.reindex_shapes_for_body(self._body.space, self._body)  # Обновление данных обнаружения столкновений

    def create_shape(space, vertices, color, x, y, width, height):
        # Создает экземпляр фигуры TetrisShape в пространстве Pymunk.
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
