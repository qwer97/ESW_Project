import pygame
import sys

# Pygame 초기화
pygame.init()

# 화면 설정 (크기 640x480)
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Raspberry Pi 화면 테스트")

# 색상 정의 (RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면을 흰색으로 채우기
    screen.fill(WHITE)

    # 빨간색 사각형 그리기
    pygame.draw.rect(screen, RED, (200, 150, 240, 180))

    # 화면 업데이트
    pygame.display.flip()

    # 60fps로 게임 루프 실행
    pygame.time.Clock().tick(60)

# Pygame 종료
pygame.quit()
sys.exit()
