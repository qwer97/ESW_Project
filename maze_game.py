import time
from digitalio import DigitalInOut, Direction
import board
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7789
from maze_generator import MazeGenerator
from player import Player

class MazeGame:
    def __init__(self, difficulty="Easy"):
        self.difficulty_map = {"Easy": 10, "Medium": 15, "Hard": 20}
        self.grid_size = self.difficulty_map.get(difficulty, 10)
        self.cell_size = 240 // self.grid_size

        # Initialize display
        cs_pin = DigitalInOut(board.CE0)
        dc_pin = DigitalInOut(board.D25)
        reset_pin = DigitalInOut(board.D24)
        self.disp = st7789.ST7789(
            board.SPI(),
            height=240,
            y_offset=80,
            rotation=180,
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=24000000,
        )

        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new("RGB", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

        # Initialize input buttons
        self.init_buttons()

        # Generate maze and initialize player
        self.maze = MazeGenerator(self.grid_size, self.grid_size).generate_maze()
        self.player = Player(1, 1)

    def init_buttons(self):
        self.button_U = DigitalInOut(board.D17)
        self.button_D = DigitalInOut(board.D22)
        self.button_L = DigitalInOut(board.D27)
        self.button_R = DigitalInOut(board.D23)
        self.button_C = DigitalInOut(board.D4)

        for btn in [self.button_U, self.button_D, self.button_L, self.button_R, self.button_C]:
            btn.direction = Direction.INPUT

    def draw_maze(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                color = (255, 255, 255) if self.maze[y][x] == 0 else (0, 0, 0)
                self.draw.rectangle(
                    (
                        x * self.cell_size,
                        y * self.cell_size,
                        (x + 1) * self.cell_size,
                        (y + 1) * self.cell_size,
                    ),
                    fill=color,
                )

    def draw_player(self):
        self.draw.rectangle(
            (
                self.player.x * self.cell_size,
                self.player.y * self.cell_size,
                (self.player.x + 1) * self.cell_size,
                (self.player.y + 1) * self.cell_size,
            ),
            fill=(0, 0, 255),
        )

    def handle_input(self):
        if not self.button_U.value:
            self.player.move(0, -1, self.maze)
        elif not self.button_D.value:
            self.player.move(0, 1, self.maze)
        elif not self.button_L.value:
            self.player.move(-1, 0, self.maze)
        elif not self.button_R.value:
            self.player.move(1, 0, self.maze)

    def run(self):
        while True:
            self.draw.rectangle((0, 0, self.width, self.height), fill=(0, 0, 0))
            self.handle_input()
            self.draw_maze()
            self.draw_player()
            self.disp.image(self.image)
            time.sleep(0.1)
