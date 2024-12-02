import random

WALL = 1
PATH = 0

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def generate_maze(self):
        maze = [[WALL for _ in range(self.width)] for _ in range(self.height)]

        def carve_path(x, y):
            maze[y][x] = PATH
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and maze[ny][nx] == WALL:
                    maze[y + dy // 2][x + dx // 2] = PATH
                    carve_path(nx, ny)

        carve_path(1, 1)
        return maze
