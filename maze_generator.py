import random

WALL = 1
PATH = 0


class MazeGenerator:
    def __init__(self, width, height):
        self.width = max(width, 5)
        self.height = max(height, 5)

    def generate_maze(self):
        width = self.width if self.width % 2 == 1 else self.width + 1
        height = self.height if self.height % 2 == 1 else self.height + 1
        maze = [[WALL for _ in range(width)] for _ in range(height)]
        start_x, start_y = 1, 1
        maze[start_y][start_x] = PATH
        stack = [(start_x, start_y)]
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]

        while stack:
            current_x, current_y = stack[-1]
            unvisited_neighbors = [
                (current_x + dx, current_y + dy, dx, dy)
                for dx, dy in directions
                if 0 < current_x + dx < width - 1
                and 0 < current_y + dy < height - 1
                and maze[current_y + dy][current_x + dx] == WALL
            ]

            if unvisited_neighbors:
                nx, ny, dx, dy = random.choice(unvisited_neighbors)
                maze[current_y + dy // 2][current_x + dx // 2] = PATH
                maze[ny][nx] = PATH
                stack.append((nx, ny))
            else:
                stack.pop()

        return maze
