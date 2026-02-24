import pygame
import random


class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        self.colors = self.get_cell_colors()
        self.score = 0
        self.lines_cleared = 0
        self.level = 1

        self.pieces = {
            "O": {"shape": [[0,4],[0,5],[1,4],[1,5]], "color": 1},
            "I": {"shape": [[0,3],[0,4],[0,5],[0,6]], "color": 2},
            "T": {"shape": [[0,4],[1,3],[1,4],[1,5]], "color": 3},
            "L": {"shape": [[0,5],[1,3],[1,4],[1,5]], "color": 4}
        }

        self.fall_speed = 500
        self.last_fall_time = pygame.time.get_ticks()

        self.spawn_new_piece()


    def get_cell_colors(self):
        return [
            (26, 31, 40),
            (47, 230, 23),
            (232, 18, 18),
            (226, 116, 17),
            (237, 234, 4),
            (166, 0, 247),
            (21, 204, 209),
            (13, 64, 216)
        ]


    def draw(self, screen):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_value = self.grid[row][col]
                rect = pygame.Rect(
                    col * self.cell_size + 1,
                    row * self.cell_size + 1,
                    self.cell_size - 1,
                    self.cell_size - 1
                )
                pygame.draw.rect(screen, self.colors[cell_value], rect)


    def update(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_fall_time > self.fall_speed:
            if self.can_move(1, 0):
                self.move_piece(1, 0)
            else:
                self.clear_full_rows()
                self.spawn_new_piece()

            self.last_fall_time = current_time


        def spawn_new_piece(self):
            piece_type = random.choice(list(self.pieces.keys()))
            piece_data = self.pieces[piece_type]

            self.current_piece = [cell[:] for cell in piece_data["shape"]]
            self.current_color = piece_data["color"]

            for row, col in self.current_piece:
                self.grid[row][col] = self.current_color


    def can_move(self, row_offset, col_offset):
        for row, col in self.current_piece:
            new_row = row + row_offset
            new_col = col + col_offset

            if (
                new_row < 0 or new_row >= self.num_rows or
                new_col < 0 or new_col >= self.num_cols or
                self.grid[new_row][new_col] != 0
            ):
                return False

        return True


    def move_piece(self, row_offset, col_offset):
        # Clear old
        for row, col in self.current_piece:
            self.grid[row][col] = 0

        # Update positions
        for cell in self.current_piece:
            cell[0] += row_offset
            cell[1] += col_offset

        # Redraw
        for row, col in self.current_piece:
            self.grid[row][col] = 1


    def move(self, direction):
        if self.can_move(0, direction):
            self.move_piece(0, direction)


    def clear_full_rows(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        rows_removed = self.num_rows - len(new_grid)

        for _ in range(rows_removed):
            new_grid.insert(0, [0 for _ in range(self.num_cols)])

        self.grid = new_grid


    def rotate(self):
        pivot_row, pivot_col = self.current_piece[0]
        new_positions = []

        for row, col in self.current_piece:
            new_row = pivot_row - (col - pivot_col)
            new_col = pivot_col + (row - pivot_row)
            new_positions.append([new_row, new_col])

        # Wall kicks
        for offset in [0, -1, 1]:
            valid = True
            shifted = []

            for row, col in new_positions:
                col += offset

                if (
                    row < 0 or row >= self.num_rows or
                    col < 0 or col >= self.num_cols or
                    self.grid[row][col] != 0
                ):
                    valid = False
                    break

                shifted.append([row, col])

            if valid:
                for row, col in self.current_piece:
                    self.grid[row][col] = 0

                self.current_piece = shifted

                for row, col in self.current_piece:
                    self.grid[row][col] = 1
                return