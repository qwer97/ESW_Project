import time
from digitalio import DigitalInOut, Direction
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
from maze_generator import MazeGenerator

WALL = 1
PATH = 0

class MazeGame:
    def __init__(self, difficulty="Easy"):
        size_map = {"Easy": 11, "Medium": 21, "Hard": 31}
        self.grid_size = size_map[difficulty]
        self.cell_size = 240 // self.grid_size
        self.current_stage = 1

        # 디스플레이 설정 (기존 코드와 동일)
        cs_pin = DigitalInOut(board.CE0)
        dc_pin = DigitalInOut(board.D25)
        reset_pin = DigitalInOut(board.D24)
        spi = board.SPI()

        self.disp = st7789.ST7789(
            spi,
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
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

        # 버튼 설정
        self.button_up = DigitalInOut(board.D17)
        self.button_down = DigitalInOut(board.D22)
        self.button_left = DigitalInOut(board.D27)
        self.button_right = DigitalInOut(board.D23)
        
        # 스테이지 선택 버튼
        self.button_5 = DigitalInOut(board.D5)  # 아니오 버튼
        self.button_6 = DigitalInOut(board.D6)  # 예 버튼

        for button in [self.button_up, self.button_down, self.button_left, self.button_right, 
                       self.button_5, self.button_6]:
            button.direction = Direction.INPUT

        self.reset_game_state()

    def reset_game_state(self):
        generator = MazeGenerator(self.grid_size, self.grid_size)
        self.maze = generator.generate_maze()
        
        self.player_x = 1
        self.player_y = 1
        self.goal_x = self.grid_size - 2
        self.goal_y = self.grid_size - 2
        self.start_time = time.time()
        self.is_game_over = False

        if self.current_stage <= 4:
            self.grid_size = 11 + (self.current_stage - 1) * 2
            self.cell_size = 240 // self.grid_size
        else:
            # 4단계 이후 난이도 요소 추가
            self.add_obstacles()
            self.add_time_limit()
    
    def add_obstacles(self):
        # 장애물 추가 로직
        self.obstacle_positions = [(3, 5), (7, 8), (11, 13)]

    def add_time_limit(self):
        # 시간 제한 추가 로직
        self.time_limit = 60  # 60초


    def draw_next_stage_prompt(self):
        # 다음 스테이지 선택 화면 그리기
        self.draw.rectangle((0, 0, self.width, self.height), fill=(0, 0, 0))
        
        # 프롬프트 텍스트
        self.draw.text((20, 80), "Do you want", font=self.font, fill=(255, 255, 255))
        self.draw.text((20, 110), "Next Stage?", font=self.font, fill=(255, 255, 255))
        
        # #5 버튼 (아니오)
        self.draw.rectangle((20, 150, 100, 190), outline=(255, 255, 255))
        self.draw.text((25, 165), "#5 No", font=self.font, fill=(255, 255, 255))
        
        # #6 버튼 (예)
        self.draw.rectangle((140, 150, 220, 190), outline=(255, 255, 255))
        self.draw.text((145, 165), "#6 Yes", font=self.font, fill=(255, 255, 255))
        
        self.disp.image(self.image)

        def draw_maze(self):
            for y, row in enumerate(self.maze):
                for x, cell in enumerate(row):
                    color = (0, 0, 0) if cell == WALL else (200, 200, 200)
                    self.draw.rectangle(
                        (
                            x * self.cell_size,
                            y * self.cell_size,
                            (x + 1) * self.cell_size - 1,
                            (y + 1) * self.cell_size - 1,
                        ),
                        fill=color,
                    )
            
            # 장애물 그리기
            if self.current_stage > 4:
                for x, y in self.obstacle_positions:
                    self.draw.rectangle(
                        (
                            x * self.cell_size,
                            y * self.cell_size,
                            (x + 1) * self.cell_size - 1,
                            (y + 1) * self.cell_size - 1,
                        ),
                        fill=(255, 0, 0)
                    )
    def handle_stage_selection(self):
        while True:
            if not self.button_5.value:  # #5 버튼 (아니오)
                return False
            elif not self.button_6.value:  # #6 버튼 (예)
                self.current_stage += 1
                # 미로 크기 조정
                self.grid_size = 11 + (self.current_stage - 1) * 2
                self.cell_size = 240 // self.grid_size
                return True
            time.sleep(0.1)

    def run(self):
        while True:
            # 게임 초기화
            self.reset_game_state()

            # 게임 루프
            while not self.is_game_over:
                if not self.button_up.value:
                    self.move_player(0, -1)
                elif not self.button_down.value:
                    self.move_player(0, 1)
                elif not self.button_left.value:
                    self.move_player(-1, 0)
                elif not self.button_right.value:
                    self.move_player(1, 0)

                self.draw.rectangle((0, 0, self.width, self.height), fill=(0, 0, 0))
                self.draw_maze()
                self.draw_player_and_goal()
                self.draw_status()
                self.check_win()

                self.disp.image(self.image)
                time.sleep(0.1)

            # 승리 후 다음 스테이지 선택 화면
            self.draw_next_stage_prompt()
            
            # 사용자 선택 대기
            if not self.handle_stage_selection():
                break  # 사용자가 다음 단계 거부

    def draw_maze(self):
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                color = (0, 0, 0) if cell == WALL else (200, 200, 200)
                self.draw.rectangle(
                    (
                        x * self.cell_size,
                        y * self.cell_size,
                        (x + 1) * self.cell_size - 1,
                        (y + 1) * self.cell_size - 1,
                    ),
                    fill=color,
                )

    def draw_player_and_goal(self):
        self.draw.rectangle(
            (
                self.goal_x * self.cell_size,
                self.goal_y * self.cell_size,
                (self.goal_x + 1) * self.cell_size - 1,
                (self.goal_y + 1) * self.cell_size - 1,
            ),
            fill=(0, 255, 0),
        )
        self.draw.ellipse(
            (
                self.player_x * self.cell_size,
                self.player_y * self.cell_size,
                (self.player_x + 1) * self.cell_size - 1,
                (self.player_y + 1) * self.cell_size - 1,
            ),
            fill=(255, 0, 0),
        )

    def move_player(self, dx, dy):
        nx, ny = self.player_x + dx, self.player_y + dy
        if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
            if self.maze[ny][nx] == PATH:
                self.player_x, self.player_y = nx, ny

    def draw_status(self):
        elapsed_time = time.time() - self.start_time
        self.draw.text((10, 10), f"Stage: {self.current_stage}", font=self.font, fill=(255, 255, 255))
        self.draw.text((10, 40), f"Time: {elapsed_time:.1f}s", font=self.font, fill=(255, 255, 255))

    def check_win(self):
        elapsed_time = time.time() - self.start_time
        
        # 4단계 이후 시간 제한 체크
        if self.current_stage > 4 and elapsed_time > self.time_limit:
            self.is_game_over = True
            self.draw.rectangle((0, 0, self.width, self.height), fill=(0, 0, 0))
            self.draw.text((10, 100), "Time's up!", font=self.font, fill=(255, 255, 255))
            self.disp.image(self.image)
            time.sleep(3)
        elif self.player_x == self.goal_x and self.player_y == self.goal_y:
            self.is_game_over = True
            self.draw.rectangle((0, 0, self.width, self.height), fill=(0, 0, 0))
            self.draw.text((10, 100), "Congratulations!", font=self.font, fill=(255, 255, 255))
            self.draw.text((10, 130), f"Time: {elapsed_time:.1f}s", font=self.font, fill=(255, 255, 255))
            self.disp.image(self.image)
            time.sleep(3)

if __name__ == "__main__":
    game = MazeGame()
    game.run()