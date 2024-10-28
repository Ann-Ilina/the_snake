from random import randint
import pygame

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 10  # Изменено на более низкое значение для управляемости

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), color=(0, 0, 0)):
        self.position = position
        self.color = color
        self.body_color = color  # Добавляем атрибут `body_color`

    def draw(self):
        """Отрисовывает объект на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку."""

    def __init__(self):
        super().__init__(position=(GRID_SIZE, GRID_SIZE), color=SNAKE_COLOR)
        self.body = [(GRID_SIZE, GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.positions = self.body  # Добавляем атрибут `positions`

    def update(self):
        """Обновляет позицию змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        new_head = (
            self.body[0][0] + self.direction[0] * GRID_SIZE,
            self.body[0][1] + self.direction[1] * GRID_SIZE
        )

        new_head = (new_head[0] % SCREEN_WIDTH, new_head[1] % SCREEN_HEIGHT)

        if new_head in self.body:
            raise SystemExit("Game Over!")

        self.body.insert(0, new_head)

    def grow(self):
        """Увеличивает змейку на один сегмент."""
        self.body.append(self.body[-1])

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.body[0]

    def move(self):
        """Перемещает змейку в текущем направлении."""
        self.update()

    def reset(self):
        """Сбрасывает состояние змейки."""
        self.body = [(GRID_SIZE, GRID_SIZE)]
        self.direction = RIGHT

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        if new_direction in (UP, DOWN, LEFT, RIGHT):
            if (self.direction[0] + new_direction[0],
                    self.direction[1] + new_direction[1]) != (0, 0):
                self.next_direction = new_direction

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        for segment in self.body:
            super().draw()


class Apple(GameObject):
    """Класс, представляющий яблоко."""

    def __init__(self):
        super().__init__(position=self.random_position(), color=APPLE_COLOR)
        self.body_color = APPLE_COLOR  # Добавляем атрибут `body_color`

    def random_position(self):
        """Генерирует случайную позицию для яблока."""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def spawn_new_apple(self):
        """Перемещает яблоко на новую случайную позицию."""
        self.position = self.random_position()

    def randomize_position(self):
        """Обновляет позицию яблока случайным образом."""
        self.position = self.random_position()


def handle_keys(snake):
    """Обрабатывает ввод с клавиатуры для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)


def main():
    """Основная функция игры."""
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        snake.move()

        if snake.body[0] == apple.position:
            snake.grow()
            apple.spawn_new_apple()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
