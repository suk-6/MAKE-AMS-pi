import time  # 시간 관련 함수 (sleep)
import multiprocessing  # 멀티프로세싱 지원
import datetime  # 날짜 및 시간 정보
import RPi.GPIO as GPIO  # 라즈베리 파이 GPIO 제어
import logging  # 로그 기록
from auth import checkAccess  # 외부 인증 모듈 (QR 코드 등)

# 라즈베리 파이 GPIO 제어 클래스
class pi:
    def __init__(self):  # 생성자
        self.openPin = 17  # 문 열림 제어 핀 번호 (GPIO 17)
        self.keyPin = 27  # 키 입력 감지 핀 번호 (GPIO 27)

        GPIO.setwarnings(False)  # GPIO 경고 메시지 비활성화
        GPIO.setmode(GPIO.BCM)  # GPIO 핀 번호 모드 설정 (BCM 모드)

        GPIO.setup(self.openPin, GPIO.OUT)  # 문 열림 핀 출력 설정
        GPIO.setup(self.keyPin, GPIO.IN)   # 키 입력 핀 입력 설정
        GPIO.output(self.openPin, False)  # 초기 문 열림 핀 상태 (닫힘)

        # 키 입력 감지 프로세스 생성 (데몬 프로세스)
        self.keyProcess = multiprocessing.Process(target=self.checkKey, daemon=True)
        self.keyProcess.start()  # 프로세스 시작

    # 문 열림 함수
    def doorOpen(self):
        logging.debug(f"{datetime.datetime.now()} - Open Door")  # 로그 기록 (시간, 문 열림)
        GPIO.output(self.openPin, True)  # 문 열림 핀 HIGH (문 열림)
        time.sleep(1)  # 1초 대기
        GPIO.output(self.openPin, False)  # 문 열림 핀 LOW (문 닫힘)

    # 키 입력 감지 및 처리 함수 (별도 프로세스에서 실행)
    def checkKey(self):
        while True:  # 무한 루프
            # 키 입력 감지 (GPIO 핀 HIGH 상태 확인)
            if GPIO.input(self.keyPin) == GPIO.HIGH: 
                if checkAccess():  # 인증 확인 (checkAccess 함수 호출)
                    self.doorOpen()  # 인증 성공 시 문 열림
            time.sleep(0.1)  # 0.1초 대기 (루프 반복 속도 조절)
