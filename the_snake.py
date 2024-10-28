from random import choice, randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10  # Изменено на более низкое значение для управляемости

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()

# Базовый класс игрового объекта
class GameObject:
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# Класс для змейки
class Snake(GameObject):
    def __init__(self):
        super().__init__((GRID_SIZE, GRID_SIZE), SNAKE_COLOR)
        self.body = [(GRID_SIZE, GRID_SIZE)]  # Начальное положение головы
        self.direction = RIGHT
        self.next_direction = None

    def update(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        # Новая голова
        new_head = (self.body[0][0] + self.direction[0] * GRID_SIZE,
                    self.body[0][1] + self.direction[1] * GRID_SIZE)

        # Учитываем "появление" с другой стороны
        new_head = (new_head[0] % SCREEN_WIDTH, new_head[1] % SCREEN_HEIGHT)

        # Проверка на столкновение с собой
        if new_head in self.body:
            raise SystemExit("Game Over!")

        self.body.insert(0, new_head)  # Добавляем новую голову

    def grow(self):
        self.body.append(self.body[-1])  # Увеличиваем змейку на один сегмент

    def draw(self):
        for segment in self.body:
            rect = pygame.Rect(segment, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# Класс для яблока
class Apple(GameObject):
    def __init__(self):
        self.position = self.random_position()
        super().__init__(self.position, APPLE_COLOR)

    def random_position(self):
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def spawn_new_apple(self):
        self.position = self.random_position()

# Функция обработки действий пользователя
def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT

def main():
    # Инициализация PyGame
    pygame.init()
    
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        snake.update()

        # Проверка на съедение яблока
        if snake.body[0] == apple.position:
            snake.grow()
            apple.spawn_new_apple()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()

if __name__ == '__main__':
    main()
