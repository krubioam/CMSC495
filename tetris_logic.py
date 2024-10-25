from grid import Grid
from pieces import *
import random
import pygame


class TetrisLogic:
    def __init__(self):
        self.grid = Grid(1)
        self.available_pieces = []
        self.current_piece = self.random_piece()
        self.next_piece = self.random_piece()
        self.game_over = False
        self.movement = True
        self.AUTO_MOVE = pygame.USEREVENT + 1
        self.counter = 0
        pygame.time.set_timer(self.AUTO_MOVE,200)

    #Grabs a random piece from an array of 7 pieces
    #Removes selected piece from array
    #When array is empty add all pieces back in
    def random_piece(self):
        if len(self.available_pieces) == 0:
            self.available_pieces = [IPiece(),JPiece(),LPiece(),OPiece(),SPiece(),TPiece(),ZPiece()]

        piece = random.choice(self.available_pieces)
        self.available_pieces.remove(piece)
        return piece

    #Checks if piece collides with any border
    def collision(self):
        cells = self.current_piece.get_position()
        for x,y in cells:
            if not self.grid.border_collision(x,y):
                return False
        return True

    def move_left(self):
        self.current_piece.move(-1,0)
        if not self.collision() or not self.empty_space():
            self.current_piece.move(1,0)

    def move_right(self):
        self.current_piece.move(1,0)
        if not self.collision() or not self.empty_space():
            self.current_piece.move(-1, 0)

    #Moves piece down and if collides with anything locks piece in place
    def move_down(self):
        self.current_piece.move(0,1)
        if not self.collision() or not self.empty_space():
            self.current_piece.move(0, -1)
            self.lock()


    #Locks piece into place
    def lock(self):
       cells = self.current_piece.get_position()

       for x,y in cells:
            self.grid.grid[x][y] = self.current_piece.piece_type

       self.current_piece = self.next_piece
       self.next_piece = self.random_piece()
       self.grid.clear_rows()

       if not self.empty_space():
            self.game_over = True

    #Checks if current position overlaps with another piece
    def empty_space(self):
        cells = self.current_piece.get_position()
        for x,y in cells:
            if not self.grid.empty_space(x,y):
                return False
        return True

    #Moves piece down on a timer
    def auto_move(self,event):
        if event.type == self.AUTO_MOVE and not self.game_over:
            self.move_down()

    def rotate_right(self):
        self.current_piece.right_rotate()
        if not self.collision() or not self.empty_space():
            self.current_piece.left_rotate()

    def rotate_left(self):
        self.current_piece.left_rotate()
        if not self.collision() or not self.empty_space():
            self.current_piece.right_rotate()

    #Draws a ghost piece in the final position a piece can have
    def draw_ghost(self,screen):
        ghost_offset =self.grid.total_y
        ghost_collision = False
        ghost_cells = self.current_piece.get_rotation()
        current_offset = self.current_piece.get_x_offset()

        #Determines what the y offset for the ghost piece can be
        for ghost_x, ghost_y in ghost_cells:
            for i in range(self.grid.total_y):
                if not self.grid.border_collision(ghost_x+current_offset,ghost_y+i) and self.grid.empty_space(ghost_x+current_offset,i):
                    if not ghost_collision:
                        ghost_offset = i-ghost_y
                if not self.grid.empty_space(ghost_x+current_offset,i):
                    ghost_collision = True
                    if i-(ghost_y+1) < ghost_offset:
                        ghost_offset = i-(ghost_y+1)
                    break

        #Draws a transparent piece where ghost piece should be
        for ghost_x, ghost_y in ghost_cells:
            surface = pygame.Surface((self.grid.cell_size,self.grid.cell_size))
            surface.set_alpha(155)
            cell_rect = pygame.Rect((ghost_x+current_offset) * self.grid.cell_size + self.grid.offset,(ghost_y+ghost_offset) * self.grid.cell_size+ self.grid.offset,
                                self.grid.cell_size - 1, self.grid.cell_size - 1)
            surface.fill((92, 97, 102))
            screen.blit(surface,cell_rect)



    def draw(self, screen):
        self.grid.draw(screen)
        self.current_piece.draw(screen)
        self.draw_ghost(screen)

    def reset(self):
        self.grid.reset()
        self.available_pieces = []
        self.current_piece = self.random_piece()
        self.next_piece = self.random_piece()