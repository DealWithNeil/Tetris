import pygame

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        self.colors = self.get_cell_colors()

        # Active falling cell
        self.current_row = 0
        self.current_col = 4
        self.current_piece = [
            [0, 4],
            [0, 5],
            [1, 4],
            [1, 5]
        ]

        for row, col in self.current_piece:
            self.grid[row][col] = 1

        # Gravity timer
        self.fall_speed = 500  # milliseconds
        self.last_fall_time = pygame.time.get_ticks()

    def print_grid(self):
        for row in self.grid:
            print(row)

    def get_cell_colors(self):
        dark_grey = (26, 31, 40)
        green = (47, 230, 23)
        red = (232, 18, 18)
        orange = (226, 116, 17)
        yellow = (237, 234, 4)
        purple = (166, 0, 247)
        cyan = (21, 204, 209)
        blue = (13, 64, 216)
        return [dark_grey, green, red, orange, yellow, purple, cyan, blue]

    def draw(self, screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(
                    column * self.cell_size + 1,
                    row * self.cell_size + 1,
                    self.cell_size - 1,
                    self.cell_size - 1
                )
                pygame.draw.rect(
                    screen,
                    self.colors[cell_value],
                    cell_rect
                )

    def update(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_fall_time > self.fall_speed:
            # Check if piece can move down
            can_move = True

            for row, col in self.current_piece:
                next_row = row + 1
                if next_row >= self.num_rows or self.grid[next_row][col] != 0:
                    can_move = False
                    break

            if can_move:
                # Clear old positions
                for row, col in self.current_piece:
                    self.grid[row][col] = 0

                # Move piece down
                for cell in self.current_piece:
                    cell[0] += 1

                # Redraw piece
                for row, col in self.current_piece:
                    self.grid[row][col] = 1
            else:
                self.spawn_new_piece()

            self.last_fall_time = current_time


    def spawn_new_piece(self):
        self.current_piece = [
            [0, 4],
            [0, 5],
            [1, 4],
            [1, 5]
        ]

        for row, col in self.current_piece:
            self.grid[row][col] = 1

        # If spawn position already filled → game over later

    def move(self, direction):
        new_col = self.current_col + direction

        # Check boundaries
        if 0 <= new_col < self.num_cols:
            # Clear current position
            self.grid[self.current_row][self.current_col] = 0

            # Update column
            self.current_col = new_col

            # Draw new position
            self.grid[self.current_row][self.current_col] = 1

        


        def clear_full_rows(self):
            new_grid = []

            for row in self.grid:
                if any(cell == 0 for cell in row):
                    new_grid.append(row)

            # Count how many rows were removed
            rows_removed = self.num_rows - len(new_grid)

            # Add empty rows at top
            for _ in range(rows_removed):
                new_grid.insert(0, [0 for _ in range(self.num_cols)])

            self.grid = new_grid
