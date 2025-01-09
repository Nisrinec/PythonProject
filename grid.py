import pygame
import os

letterX = pygame.image.load(os.path.join('./res', 'letterX.png'))
letterO = pygame.image.load(os.path.join('./res', 'letterO.png'))
letterX = pygame.transform.scale(letterX, (200, 200))
letterO = pygame.transform.scale(letterO, (200, 200))

class Grid:
    def __init__(self):
        self.grid_lines = [
            ((0, 200), (600, 200)),
            ((0, 400), (600, 400)),
            ((200, 0), (200, 600)),
            ((400, 0), (400, 600)),
        ]
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.switch_player = True
        self.search_dirs = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        self.game_over = False  # Add this line

    def draw(self, surface):
        for line in self.grid_lines:
            pygame.draw.line(surface, (200, 200, 200), line[0], line[1], 2)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == "X":
                    surface.blit(letterX, (x * 200, y * 200))
                elif self.get_cell_value(x, y) == "O":
                    surface.blit(letterO, (x * 200, y * 200))

        # Check for a winner and display the result
        winner = self.check_winner()
        if winner:
            font = pygame.font.Font(None, 74)
            text = font.render(f"Player {winner} wins!", True, (255, 0, 0))
            surface.blit(text, (150, 250))

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    def get_cell_value(self, x, y):
        return self.grid[y][x]

    @staticmethod
    def is_within_bounds(x, y):
        return 0 <= x < 3 and 0 <= y < 3

    def check_winner(self):
        # Check rows and columns
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] != 0:
                self.game_over = True  # Set game_over to True
                return self.grid[i][0]
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] != 0:
                self.game_over = True  # Set game_over to True
                return self.grid[0][i]

        # Check diagonals
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != 0:
            self.game_over = True  # Set game_over to True
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != 0:
            self.game_over = True  # Set game_over to True
            return self.grid[0][2]

        return None

    def print_grid(self):
        for row in self.grid:
            print(row)
    def get_mouse(self, x, y, player):
        if self.get_cell_value(x, y) == 0:
           self.set_cell_value(x, y, player)
           self.check_grid(x, y, player)
    def clear_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.set_cell_value(x, y, 0)

    def check_grid(self, x, y, player):
        count = 1
        for index, (dirx, diry) in enumerate(self.search_dirs):
            if self.is_within_bounds(x + dirx, y + diry) and self.get_cell_value(x+dirx, y+diry) == player:
                count += 1
                xx = x + dirx
                yy = y + diry
                if self.is_within_bounds(xx+dirx, yy+diry) and self.get_cell_value(xx+dirx, yy+diry) == player:
                    count += 1
                    if count == 3:
                        break
                    if count < 3:
                        new_dir = 0
                        if index == 0:
                            new_dir = self.search_dirs[4]
                        elif index == 1:
                            new_dir = self.search_dirs[5]
                        elif index == 2:
                            new_dir = self.search_dirs[6]
                        elif index == 3:
                            new_dir = self.search_dirs[7]
                        elif index == 4:
                            new_dir = self.search_dirs[0]
                        elif index == 5:
                            new_dir = self.search_dirs[1]
                        elif index == 6:
                            new_dir = self.search_dirs[2]
                        elif index == 7:
                            new_dir = self.search_dirs[3]
                        if self.is_within_bounds(x + new_dir[0], y + new_dir[1]) and self.get_cell_value(x+new_dir[0], y+new_dir[1]) == player:
                            count += 1
                            if count == 3:
                                break
                        else:
                            count = 1
            if count == 3:
                print(player, 'wins!')