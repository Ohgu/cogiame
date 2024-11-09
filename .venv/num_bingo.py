import pygame
import random
import sys

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('레벨별 수식 게임')

# 폰트 설정
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 게임 변수 초기화
score = 0
user_input = ''
equation = ''
correct_answer = 0
level = 1
correct_in_level = 0  # 현재 레벨에서 맞춘 정답 수
answers_to_level_up = 3  # 다음 레벨로 가기 위한 정답 수
mistakes = 0  # 현재 레벨에서 틀린 횟수
max_mistakes = 3  # 레벨당 최대 오답 허용 횟수

def generate_equation(level):
    operators = ['+', '-', '*', '/']
    while True:
        if level == 1:
            num1 = random.randint(0, 9)
            num2 = random.randint(0, 9)
            op = random.choice(['+', '-'])
        elif level == 2:
            num1 = random.randint(0, 20)
            num2 = random.randint(1, 20)
            op = random.choice(['*', '/'])
        elif level >= 3:
            num1 = random.randint(0, 20)
            num2 = random.randint(0, 20)
            num3 = random.randint(0, 20)
            op1 = random.choice(operators)
            op2 = random.choice(operators)
        else:
            num1 = random.randint(0, 10)
            num2 = random.randint(0, 10)
            op = random.choice(operators)

        # 결과값이 정수가 되는지 확인하기 위해 임시로 저장
        if level <= 2:
            if op == '/':
                if num2 == 0 or num1 % num2 != 0:
                    continue  # 0으로 나누거나 결과가 정수가 아니면 다시 생성
                result = num1 // num2
            elif op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2

            # 누락될 값 선택
            missing = random.choice(['num1', 'num2', 'result'])
            if missing == 'num1':
                answer = num1
                if answer < 0:
                    continue  # 정답이 음수이면 다시 생성
                eq = f"? {op} {num2} = {result}"
            elif missing == 'num2':
                answer = num2
                if answer < 0:
                    continue
                eq = f"{num1} {op} ? = {result}"
            else:
                answer = result
                eq = f"{num1} {op} {num2} = ?"

        elif level >= 3:
            expression = f"{num1} {op1} {num2} {op2} {num3}"
            try:
                result = eval(expression)
                if not isinstance(result, int):
                    continue  # 결과가 정수가 아니면 다시 생성
            except ZeroDivisionError:
                continue  # 0으로 나누면 다시 생성

            # 누락될 값 선택
            missing = random.choice(['num1', 'num2', 'num3', 'result'])
            if missing == 'num1':
                answer = num1
                if answer < 0:
                    continue
                eq = expression.replace(str(num1), '?', 1) + f" = {result}"
            elif missing == 'num2':
                answer = num2
                if answer < 0:
                    continue
                eq = expression.replace(str(num2), '?', 1) + f" = {result}"
            elif missing == 'num3':
                answer = num3
                if answer < 0:
                    continue
                eq = expression.replace(str(num3), '?', 1) + f" = {result}"
            else:
                answer = result
                eq = expression + f" = ?"

        else:
            continue  # 해당하지 않으면 다시 생성

        # 정답이 0 이상의 정수인지 확인
        if not isinstance(answer, int) or answer < 0:
            continue  # 정답이 음수이거나 정수가 아니면 다시 생성

        return eq, answer

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    text_rect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, text_rect)

# 첫 번째 식 생성
equation, correct_answer = generate_equation(level)

# 게임 루프
running = True
level_up_text = False
game_over = False
while running:
    screen.fill(WHITE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # 정답 체크
                try:
                    player_answer = int(user_input)
                    if player_answer == correct_answer:
                        score += 1
                        correct_in_level += 1
                        # 레벨 업 체크
                        if correct_in_level >= answers_to_level_up:
                            level += 1
                            correct_in_level = 0
                            mistakes = 0  # 오답 횟수 초기화
                            # 레벨 업 알림
                            level_up_text = True
                            level_up_counter = 0
                    else:
                        mistakes += 1
                        if mistakes >= max_mistakes:
                            # 게임 오버
                            running = False
                            game_over = True
                except ValueError:
                    # 유효하지 않은 입력
                    mistakes += 1
                    if mistakes >= max_mistakes:
                        running = False
                        game_over = True

                user_input = ''
                if running:
                    equation, correct_answer = generate_equation(level)

            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                if event.unicode in '0123456789':
                    user_input += event.unicode

    # 화면 표시
    draw_text(f"LEVEL {level}", small_font, BLACK, screen, WIDTH // 2, 30)
    draw_text(equation, font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)

    # 사용자 입력 표시
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    pygame.draw.rect(screen, BLACK, input_box, 2)
    draw_text(user_input, font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 25)

    # 점수 및 오답 횟수 표시
    draw_text(f"SCORE: {score}", small_font, BLACK, screen, WIDTH - 80, 30)
    draw_text(f"CHANCE: {mistakes}/{max_mistakes}", small_font, BLACK, screen, WIDTH - 100, 70)

    # 레벨 업 알림
    if level_up_text:
        draw_text("LEVEL UP!", font, (0, 128, 0), screen, WIDTH // 2, HEIGHT // 2 + 100)
        level_up_counter += 1
        if level_up_counter > 60:  # 2초 동안 표시
            level_up_text = False

    pygame.display.flip()
    pygame.time.Clock().tick(30)

# 게임 종료 화면
screen.fill(WHITE)
if game_over:
    draw_text("GAME OVER!", font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
else:
    draw_text("GAME OVER!", font, BLACK, screen, WIDTH // 2, HEIGHT // 2 - 50)
draw_text(f"SCORE: {score}", font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 25)
pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
