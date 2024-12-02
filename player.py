class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy, maze):
        new_x, new_y = self.x + dx, self.y + dy
        if maze[new_y][new_x] == 0:  # PATH
            self.x, self.y = new_x, new_y
