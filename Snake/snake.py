import pygame
import time
from random import randint
from collections import deque

pygame.init()
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
fps = 8

size = width, height = 1400, 640
window = pygame.display.set_mode(size)
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
white = 255, 255, 255
black = 0, 0, 0

block_size = 40
block_spacing = 2
block_spacing_twice = 2 * block_spacing
apple_size = block_size - block_spacing_twice


class Block:
    def __init__(self, x, y, direction):
        self.width = block_size
        self.height = block_size
        self.x = x
        self.y = y
        self.rect = None
        self.create(direction)

    def create(self, direction):
        coordinates = self.update_coordinates(direction)
        self.rect = pygame.Rect(*coordinates)

    def update(self, direction):
        coordinates = self.update_coordinates(direction)
        pygame.Rect.update(self.rect, *coordinates)
        return self.x, self.y

    def update_coordinates(self, direction):
        coordinates = None
        match direction:
            case 'r':
                coordinates = self.x + block_spacing, self.y + block_spacing, self.width, self.height - block_spacing_twice
            case 'l':
                coordinates = self.x - block_spacing, self.y + block_spacing, self.width, self.height - block_spacing_twice
            case 'u':
                coordinates = self.x + block_spacing, self.y - block_spacing, self.width - block_spacing_twice, self.height
            case 'd':
                coordinates = self.x + block_spacing, self.y + block_spacing, self.width - block_spacing_twice, self.height
        return coordinates


class Snake:
    def __init__(self, blocks, directions, block_positions):
        self.blocks = blocks
        self.block_positions = block_positions
        self.movements = None
        self.next_direction = directions[-1]

    def update(self):
        for block in self.blocks:
            pygame.draw.rect(window, green, block)

    def handle_movements(self):
        self.movements = [True, True, True, True]
        match self.next_direction:
            case 'r' | 'l':
                self.movements[0] = False
                self.movements[1] = False
            case 'u' | 'd':
                self.movements[2] = False
                self.movements[3] = False

    def handle_collisions(self):
        last_block_position = self.block_positions.pop()
        if last_block_position in self.block_positions:
            game_over(apple.score)
        elif last_block_position[0] == -block_size or last_block_position[1] == 0:
            game_over(apple.score)
        elif last_block_position[0] == width or last_block_position[1] == height:
            game_over(apple.score)
        self.block_positions.append(last_block_position)

    def handle_growth(self, apple):
        match self.next_direction:
            case 'r':
                self.block_positions.append((self.block_positions[-1][0] + block_size, self.block_positions[-1][1]))
            case 'l':
                self.block_positions.append((self.block_positions[-1][0] - block_size, self.block_positions[-1][1]))
            case 'u':
                self.block_positions.append((self.block_positions[-1][0], self.block_positions[-1][1] - block_size))
            case 'd':
                self.block_positions.append((self.block_positions[-1][0], self.block_positions[-1][1] + block_size))
        self.blocks.append(Block(*self.block_positions[-1], self.next_direction))
        self.blocks[-2].update(self.next_direction)
        if self.block_positions[-1] == apple.position:
            apple.respawn(self.block_positions)
            apple.score += 1
        else:
            self.block_positions.popleft()
            self.blocks.popleft()


class Apple:
    def __init__(self):
        self.position = None
        self.score = 0

    def respawn(self, snake_block_positions):
        self.position = randint(0, 34) * block_size, randint(1, 15) * block_size
        while self.position in snake_block_positions:
            self.position = randint(0, 34) * block_size, randint(1, 15) * block_size

    def update(self):
        pygame.draw.rect(window, red, pygame.Rect(self.position[0] + block_spacing, self.position[1] + block_spacing, apple_size, apple_size))


def show_score(score):
    score_font = pygame.font.SysFont('consolas', 20)
    score_surface = score_font.render(f'Score: {score}', True, white)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (50, 10)
    window.blit(score_surface, score_rect)


def show_score_geme_over(score):
    score_font = pygame.font.SysFont('consolas', 40)
    score_surface = score_font.render(f'Score: {score}', True, white)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (width // 2, height // 1.25)
    window.blit(score_surface, score_rect)


def game_over(score):
    my_font = pygame.font.SysFont('consolas', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width/2, height/4)
    window.fill(black)
    window.blit(game_over_surface, game_over_rect)
    show_score_geme_over(score)
    pygame.display.flip()
    time.sleep(3)
    exit()


def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.movements[0]:
                snake.next_direction = 'r'
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.movements[1]:
                snake.next_direction = 'l'
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.movements[2]:
                snake.next_direction = 'u'
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.movements[3]:
                snake.next_direction = 'd'


block_positions = deque([(680, 320), (720, 320), (760, 320)])
directions = ['r', 'r', 'r']
blocks = deque(Block(*block_position, direction) for block_position, direction in zip(block_positions, directions))
snake = Snake(blocks, directions, block_positions)
apple = Apple()
apple.respawn(snake.block_positions)

while True:
    snake.handle_movements()
    event_handler()
    snake.handle_growth(apple)
    window.fill(black)
    snake.handle_collisions()
    snake.update()
    apple.update()
    show_score(apple.score)
    pygame.display.update()
    clock.tick(fps)