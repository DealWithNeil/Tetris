class Grid:
    ...

    def rotate(self):
        pivot_row, pivot_col = self.current_piece[0]
        new_positions = []

        for row, col in self.current_piece:
            new_row = pivot_row - (col - pivot_col)
            new_col = pivot_col + (row - pivot_row)
            new_positions.append([new_row, new_col])

        for offset in [0, -1, 1]:
            valid = True
            shifted = []

            for row, col in new_positions:
                col += offset
                if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols or self.grid[row][col] != 0:
                    valid = False
                    break
                shifted.append([row, col])

            if valid:
                for row, col in self.current_piece:
                    self.grid[row][col] = 0

                self.current_piece = shifted

                for row, col in self.current_piece:
                    self.grid[row][col] = self.current_color
                return

    # --- NEW: Hard Drop ---
    def hard_drop(self):
        if self.game_over:
            return
        while self.can_move(1, 0):
            self.move_piece(1, 0)
        self.clear_full_rows()
        self.spawn_new_piece()

    # --- NEW: Ghost Piece ---
    def get_ghost_piece(self):
        ghost = [cell[:] for cell in self.current_piece]
        while True:
            can_move = True
            for row, col in ghost:
                if row + 1 >= self.num_rows or self.grid[row + 1][col] != 0:
                    can_move = False
                    break
            if not can_move:
                break
            for cell in ghost:
                cell[0] += 1
        return ghost