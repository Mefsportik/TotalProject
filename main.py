import random
from Shapes import TetrisShape
import pymunk
import pymunk.pygame_util
import pygame


def main():
    # Основная функция, представляющая главный цикл игры.
    pygame.init()
    music = [pygame.mixer.Sound('Options/GFF.ogg'), pygame.mixer.Sound('Options/BW.ogg'),
             pygame.mixer.Sound('Options/RX.ogg'), pygame.mixer.Sound('Options/BS.ogg'),
             pygame.mixer.Sound('Options/MZ.ogg')]

    s = random.choice(music)
    s.play()

    width = 800  # Размеры окна игры.
    height = 600

    win_height = 100  # Высота для победы.
    win_color = (255, 255, 0)  # Цвет линии победы.
    current_height = height  # Текущая высота фигур в игре.
    left_boundary = 200  # Левая граница для движения фигур.
    right_boundary = width - 200  # Правая.
    boundary_color = (150, 0, 0)  # Цвет границ.
    current_height_color = (200, 200, 200)  # Цвет текущей высоты фигур.
    dead_line_height = height  # Высота линии поражения.
    dead_line_color = (200, 0, 0)  # Цвет линии поражения.
    dead_line_appeared = False  # Флаг, указывающий, появилась ли линия поражения.
    dead_line_delay = 15000  # Задержка перед появлением линии поражения.
    dead_line_delay_start = 0  # Время начала задержки перед появлением линии поражения.
    dead_line_speed = 0.05  # Скорость движения линии поражения.

    screen = pygame.display.set_mode((width, height))  # Экран Pygame.

    running = True  # Флаг, указывающий, выполняется ли игра.

    score = 100  # Текущий счет игрока.

    clock = pygame.time.Clock()  # Объект для управления временем в игре.
    fps = 60  # Количество кадров в секунду.
    delta_time = 1 / fps  # Время между кадрами.

    space = pymunk.Space()  # Пространство Pymunk для физической симуляции.
    space.gravity = (0, 981)  # Гравитация.

    shape = pymunk.Segment(space.static_body, (-width, height), (width * 2, height),
                           1)  # Сегмент, представляющий нижнюю границу игры в пространстве Pymunk.
    shape.collision_type = 1
    shape.friction = 10.0
    space.add(shape)

    draw_options = pymunk.pygame_util.DrawOptions(screen)  # Опции отрисовки Pymunk.

    colors = [
        (255, 0, 0, 255),
        (0, 150, 0, 255),
        (0, 0, 255, 255),
        (255, 120, 0, 255),
        (255, 255, 0, 255),
        (180, 0, 255, 255),
        (0, 220, 220, 255)
    ]  # Список возможных цветов фигур.

    tetris_shapes = [
        [(1, 0), (1, 1), (1, 2), (1, 3)],  # I-shape
        [(0, 1), (1, 1), (2, 1), (3, 1)],  # I-shape
        [(1, 0), (2, 0), (2, 1), (2, 2)],  # Z-shape
        [(2, 0), (1, 0), (1, 1), (0, 1)],  # S-shape
        [(1, 0), (1, 1), (1, 2), (2, 2)],  # L-shape
        [(1, 0), (1, 1), (1, 2), (0, 2)],  # L-shape
        [(0, 0), (0, 1), (0, 2), (1, 0), (-1, 0)],  # T-shape
        [(0, 0), (0, 1), (0, 2), (1, 2), (-1, 2)],  # T-shape
        [(0, 0), (0, 1), (0, 2), (-2, 1), (-1, 1)],  # T-shape
        [(0, 0), (0, 1), (1, 1), (1, 0)],  # O-shape
    ]  # Список возможных форм Тетриса.

    cell_size = 30  # Размер ячейки фигуры.

    collision_handler = space.add_collision_handle(0, 1)  # Обработчик столкновений для форм Тетриса.

    font = pygame.font.Font(None, 64)  # Шрифт для отображения счета и результатов игры.

    def get_shape():
        # Возвращает новую случайную форму TetrisShape.
        t_shape = TetrisShape.create_shape(space,
                                           random.choice(tetris_shapes),
                                           random.choice(colors),
                                           width // 2, -height // 2,
                                           cell_size, cell_size)
        collision_handler.post_solve = t_shape.handle_collisions
        return t_shape

    current_shape = get_shape()
    t_shapes = [current_shape]

    game_won = False
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    s.stop()
                elif event.key == pygame.K_RIGHT:
                    s.stop()
                    s = random.choice(music)
                    s.play()

        if current_shape.is_done():
            if current_shape.dead():
                if not dead_line_appeared:
                    dead_line_appeared = True
                    dead_line_delay_start = pygame.time.get_ticks()
                score -= 20
            else:
                score += 10
            if score <= 0:
                score = 0
                game_over = True
                game_won = False
                running = False
            current_shape = get_shape()
            t_shapes.append(current_shape)
        else:
            current_shape.update(left_boundary, right_boundary)

        now = pygame.time.get_ticks()
        if dead_line_appeared and now - dead_line_delay_start > dead_line_delay:
            if dead_line_height <= current_height:
                game_over = True
                game_won = False
                running = False
            else:
                dead_line_height -= dead_line_speed

        max_height = height
        for t_shape in t_shapes:
            if t_shape.is_done() and t_shape.get_height() < max_height:
                max_height = t_shape.get_height()
        current_height = max_height
        if current_height <= win_height:
            game_over = True
            game_won = True
            running = False

        screen.fill('black')
        pygame.draw.rect(screen, boundary_color, (0, 0, left_boundary, height))
        pygame.draw.rect(screen, boundary_color, (right_boundary, 0, width, height))
        pygame.draw.rect(screen, current_height_color, (0, current_height, width, 5))
        pygame.draw.rect(screen, win_color, (0, win_height, width, 5))
        pygame.draw.rect(screen, dead_line_color, (0, dead_line_height, width, 5))
        space.debug_draw(draw_options)

        text = font.render(str(score), True, (255, 255, 255))
        rect = text.get_rect(center=(width // 2, 50))
        screen.blit(text, rect)

        pygame.display.update()

        space.step(delta_time)
        clock.tick(fps)

    if game_over:
        if game_won:
            text = font.render(str(score), True, (255, 255, 255))
            rect = text.get_rect(center=(width // 2, 50))
            screen.blit(text, rect)
            text = font.render('Ты выиграл!', True, (255, 255, 255))
            rect = text.get_rect(center=(width // 2, 150))
            screen.blit(text, rect)
        else:
            text = font.render(str(score), True, (255, 255, 255))
            rect = text.get_rect(center=(width // 2, 50))
            screen.blit(text, rect)
            text = font.render('Ты проиграл.', True, (255, 255, 255))
            rect = text.get_rect(center=(width // 2, 150))
            screen.blit(text, rect)
        pygame.display.update()
        pygame.time.delay(5000)


if __name__ == '__main__':
    main()