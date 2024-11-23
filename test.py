import board
import digitalio
import adafruit_ili9341
import time

# SPI 핀 설정
spi = board.SPI()
cs_pin = digitalio.DigitalInOut(board.D5)   # CS 핀
dc_pin = digitalio.DigitalInOut(board.D6)   # DC 핀
reset_pin = digitalio.DigitalInOut(board.D9) # RST 핀

# 디스플레이 객체 생성
display = adafruit_ili9341.ILI9341(spi, cs=cs_pin, dc=dc_pin, rst=reset_pin)

# 화면 초기화
display.fill(0x0000)  # 검은색으로 화면을 채움
time.sleep(1)

# 텍스트 출력
display.text("Hello, World!", 10, 10, color=0xFFFF00)
