# main.py

from login import Kiwoom

def main():
    kiwoom = Kiwoom()
    kiwoom.login()

    if kiwoom.login_status:
        print("이제 OpenAPI 기능을 사용할 수 있습니다.")
        # 향후 종목 조회, 실시간 수신, 조건검색 등 모듈 추가 예정

if __name__ == "__main__":
    main()
