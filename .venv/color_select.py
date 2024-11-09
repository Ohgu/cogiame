import pygame
import random
import sys

# 색상 정의
COLORS = {
    "RED": (255, 0, 0),
    "ORANGE": (255, 165, 0),
    "YELLOW": (255, 255, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "PURPLE": (128, 0, 128),
    "BLACK": (0, 0, 0)
}

# 색상에 맞는 키 정의
KEYS = {
    "RED": pygame.K_r,
    "ORANGE": pygame.K_o,
    "YELLOW": pygame.K_y,
    "GREEN": pygame.K_g,
    "BLUE": pygame.K_b,
    "PURPLE": pygame.K_p,
    "BLACK": pygame.K_k
}

# 초기 설정
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("색상 연결 게임")
font = pygame.font.Font(None, 74)

# 점수와 시간 설정
score = 0
clock = pygame.time.Clock()

# 랜덤한 색상 텍스트 생성
def get_random_color_text():
    color_name = random.choice(list(COLORS.keys()))
    color = random.choice(list(COLORS.values()))
    return color_name, color

# 게임 루프
running = True
color_name, color = get_random_color_text()
while running:
    screen.fill((255, 255, 255))
    
    # 텍스트 표시
    text = font.render(color_name, True, color)
    screen.blit(text, (300, 250))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # 사용자가 올바른 키를 눌렀는지 확인
            if event.key == KEYS[color_name]:
                score += 1
                color_name, color = get_random_color_text()  # 새로운 색상 텍스트 생성
            else:
                print("WRONG ANSWER!")
    
    # 점수 표시
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
