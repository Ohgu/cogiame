import random
import curses

def generate_number_string(length):
    """지정된 길이만큼 랜덤 숫자 문자열을 생성"""
    return ''.join(random.choices('0123456789', k=length))

def game(stdscr):
    # 게임 초기화
    curses.curs_set(0)  # 커서 숨기기
    stdscr.clear()
    
    # 게임 설정
    max_levels = 5  # 총 레벨 수
    max_attempts = 3  # 레벨당 최대 실패 횟수
    level_length_start = 3  # 시작 숫자 길이
    level_increase = 1  # 레벨마다 증가하는 숫자 길이

    for level in range(1, max_levels + 1):
        # 레벨별 설정
        number_length = level_length_start + (level - 1) * level_increase
        attempts_left = max_attempts

        # 랜덤 숫자 생성
        number_string = generate_number_string(number_length)
        
        while attempts_left > 0:
            # 숫자 보여주기
            stdscr.clear()
            stdscr.addstr(0, 0, f"레벨 {level}: 숫자를 외우세요 (길이: {number_length})")
            stdscr.addstr(1, 0, f"숫자: {number_string}")
            stdscr.addstr(3, 0, "아무 키나 누르면 입력을 시작합니다.")
            stdscr.refresh()
            stdscr.getch()  # 키 입력 대기

            # 입력 시작
            stdscr.clear()
            stdscr.addstr(0, 0, f"레벨 {level}: 숫자를 입력하세요")
            stdscr.refresh()

            input_string = ""
            while True:
                key = stdscr.getch()
                if key in {curses.KEY_ENTER, 10, 13}:  # Enter 키
                    break
                elif key == curses.KEY_BACKSPACE or key == 127:  # 백스페이스
                    input_string = input_string[:-1]
                elif chr(key).isdigit():
                    input_string += chr(key)

                # 입력값 화면 갱신
                stdscr.clear()
                stdscr.addstr(0, 0, f"레벨 {level}: 숫자를 입력하세요")
                stdscr.addstr(2, 0, input_string)
                stdscr.refresh()

            # 입력 검증
            if input_string == number_string:
                stdscr.clear()
                stdscr.addstr(0, 0, f"레벨 {level} 성공! 다음 레벨로 진행합니다.")
                stdscr.addstr(2, 0, "아무 키나 누르세요.")
                stdscr.refresh()
                stdscr.getch()
                break
            else:
                attempts_left -= 1
                stdscr.clear()
                if attempts_left > 0:
                    stdscr.addstr(0, 0, f"틀렸습니다! 남은 기회: {attempts_left}")
                    stdscr.addstr(2, 0, "아무 키나 누르고 다시 시도하세요.")
                else:
                    stdscr.addstr(0, 0, "기회를 모두 소진했습니다! 게임 종료.")
                stdscr.refresh()
                stdscr.getch()
        
        if attempts_left == 0:
            # 모든 시도 실패 시 게임 종료
            stdscr.clear()
            stdscr.addstr(0, 0, "게임 오버! 다시 도전해보세요.")
            stdscr.refresh()
            stdscr.getch()
            return

    # 모든 레벨 완료
    stdscr.clear()
    stdscr.addstr(0, 0, "축하합니다! 모든 레벨을 성공적으로 완료했습니다!")
    stdscr.addstr(2, 0, "아무 키나 눌러 게임을 종료하세요.")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(game)
