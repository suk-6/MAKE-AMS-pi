# 라이브러리 추가
import logging  # 로그 기록을 위한 라이브러리
import requests  # HTTP 요청을 보내기 위한 라이브러리

# 인증 서버 URL 설정
apiUrl = "https://ams-api.dyhs.kr"  # 실제 API 엔드포인트 주소로 변경해야 함

# QR 코드 인증 확인 함수
def checkAccess(code=None):  # QR 코드 문자열을 매개변수로 받음 (기본값: None)
    '''인증 서버에 인식한 QR 코드 정보가 DB에 존재하는지 확인하는 로직'''

    logging.debug(f"Check Access: {code}")  # 디버그 로그에 QR 코드 정보 기록

    try:  # 예외 처리 시작 (HTTP 요청 중 오류 발생 가능성 대비)
        if code is None:  # QR 코드가 제공되지 않은 경우
            res = requests.get(f"{apiUrl}/auth/access", timeout=5)  # QR 코드 없이 인증 요청
        else:  # QR 코드가 제공된 경우
            res = requests.get(  # QR 코드를 파라미터로 추가하여 인증 요청
                f"{apiUrl}/auth/access", params={"code": code}, timeout=5
            )

        if res.status_code != 200:  # HTTP 응답 상태 코드가 200 (성공)이 아닌 경우
            return False  # 인증 실패

        data = res.json()  # JSON 형식의 응답 데이터 파싱
        return data["status"]  # 응답 데이터에서 인증 상태 값 반환

    except requests.exceptions.ReadTimeout:  # 요청 시간 초과 예외 발생 시
        return True  # True 반환 (일시적인 네트워크 문제 등으로 인증 서버 응답 지연 가능성 고려)
