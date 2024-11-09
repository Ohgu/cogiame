import pygame
import random
import time

# pygame 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 게임 설정
MOLE_APPEAR_TIME = 1.5  # 두더지가 화면에 나타나는 시간 (초)
TIME_LIMIT = 30  # 게임 시간 (초)

# 화면 초기화
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("두더지 게임")

# 폰트 설정
font = pygame.font.Font(None, 36)

# 두더지 이미지 로드 및 크기 조정
mole_image = pygame.image.load("mole.png")
mole_image = pygame.transform.scale(mole_image, (80, 80))  # 두더지 크기를 80x80으로 조정

# 게임 상태 변수
running = True
score = 0
start_time = time.time()
last_mole_time = 0
mole_position = None

def draw_mole(position):
    """두더지를 이미지로 그리기"""
    x, y = position
    screen.blit(mole_image, (x - 40, y - 40))  # 두더지가 중심에 맞도록 좌표 조정

def display_score():
    """현재 점수를 화면에 표시"""
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def display_time_left():
    """남은 시간을 화면에 표시"""
    elapsed_time = time.time() - start_time
    time_left = max(0, TIME_LIMIT - elapsed_time)
    time_text = font.render(f"TIME: {int(time_left)}s", True, WHITE)
    screen.blit(time_text, (SCREEN_WIDTH - 150, 10))
    return time_left

def generate_mole_position():
    """화면 내 랜덤 위치에 두더지 생성"""
    x = random.randint(40, SCREEN_WIDTH - 40)  # 이미지 크기(80)의 절반을 고려해 좌표 제한
    y = random.randint(40, SCREEN_HEIGHT - 40)
    return x, y

# 게임 메인 루프
while running:
    screen.fill(BLACK)
    
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mole_position:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mole_x, mole_y = mole_position
                # 두더지 클릭 여부 확인
                if ((mouse_x - mole_x) ** 2 + (mouse_y - mole_y) ** 2) ** 0.5 <= 40:
                    score += 1
                    mole_position = None  # 두더지 제거
    
    # 두더지 생성 시간 체크
    current_time = time.time()
    if not mole_position or current_time - last_mole_time > MOLE_APPEAR_TIME:
        mole_position = generate_mole_position()
        last_mole_time = current_time

    # 두더지 그리기
    if mole_position:
        draw_mole(mole_position)

    # 점수 및 남은 시간 표시
    display_score()
    time_left = display_time_left()

    # 게임 시간 종료 확인
    if time_left == 0:
        running = False

    # 화면 업데이트
    pygame.display.flip()

# 종료 화면
screen.fill(BLACK)
end_text = font.render(f"GAME END! Score: {score}", True, WHITE)
screen.blit(end_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
pygame.display.flip()

# 종료 전 대기
time.sleep(3)
pygame.quit()
