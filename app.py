# 라이브러리 추가
import sys
import tty
import termios
from pi import pi  # GPIO 제어 등을 위한 사용자 정의 라이브러리
import logging
from auth import checkAccess  # QR 코드 인증 처리 함수

# 로그 파일 설정 (디버깅 정보 기록)
logging.basicConfig(filename="./log.txt", level=logging.DEBUG)


# 문자 하나씩 입력받는 함수 (특수 문자 포함)
def get_single_character():
    fd = sys.stdin.fileno()  # 표준 입력 파일 디스크립터
    old_settings = termios.tcgetattr(fd)  # 기존 터미널 설정 저장
    try:
        tty.setraw(sys.stdin.fileno())  # Raw 모드 설정 (버퍼링 없이 입력)
        ch = sys.stdin.read(1)  # 한 문자 읽기
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # 원래 설정 복원
    return ch  # 입력된 문자 반환


# 메인 애플리케이션 클래스
class app:
    def __init__(self) -> None:  # 생성자
        self.pi = pi()  # pi 객체 생성 (GPIO 제어 등)
        while True:  # 무한 루프
            self.waitingQRInput()  # QR 코드 입력 대기 함수 호출

    # QR 코드 입력 대기 및 처리 함수
    def waitingQRInput(self):
        buffer = []  # QR 코드 데이터 저장할 버퍼

        while 1:
            char = get_single_character()  # 문자 하나씩 입력받기
            if char == "(":  # 시작 문자 "("이면 버퍼 초기화
                buffer = []
            if char == "!":  # "!" 입력 시 프로그램 종료
                sys.exit()

            buffer.append(char)  # 입력된 문자 버퍼에 추가

            if char == ")":  # 종료 문자 ")"이면 입력 종료
                break  # 루프 탈출

        # 입력 데이터 전처리 (괄호 제거)
        if buffer[0] == "(" and buffer[-1] == ")":
            buffer.pop(0)
            buffer.pop(-1)
        else:  # 유효하지 않은 QR 코드 형식이면 함수 종료
            return

        # QR 코드 인증 확인
        if checkAccess("".join(buffer)):  # QR 코드 내용 전달하여 인증 확인
            self.pi.doorOpen()  # 인증 성공 시 문 열기


# 프로그램 시작 (오류 처리 포함)
if __name__ == "__main__":
    while 1:  # 무한 루프 (오류 발생 시 재시작)
        try:
            app()  # 메인 애플리케이션 실행
        except Exception as e:  # 예외 처리
            print(e)  # 오류 메시지 출력
            pass  # 오류 무시하고 다음 루프 진행
