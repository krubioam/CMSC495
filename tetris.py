import pygame
import sys
from tetris_logic import TetrisLogic

pygame.init()

COLOR = (33, 46, 59)
screen = pygame.display.set_mode((400,800))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

logic = TetrisLogic()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if logic.game_over:
               logic.game_over = False
               logic.reset()

            if event.key == pygame.K_a and not logic.game_over:
                logic.move_left()
            if event.key == pygame.K_d and not logic.game_over:
                logic.move_right()
            if event.key == pygame.K_SPACE and not logic.game_over:
                logic.move_down()
            if event.key == pygame.K_w and not logic.game_over:
                logic.rotate_right()
            if event.key == pygame.K_s and not logic.game_over:
                logic.rotate_left()
        logic.auto_move(event)

    screen.fill(COLOR)
    logic.draw(screen)
    pygame.display.update()
    clock.tick(60)


