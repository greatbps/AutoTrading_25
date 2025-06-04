# stock_top.py
from PyQt5.QtWidgets import QApplication
from PyQt5.QAxContainer import QAxWidget
import sys
import datetime

class Kiwoom:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        self.ocx.OnEventConnect.connect(self._on_login)
        self.ocx.OnReceiveTrData.connect(self._on_receive_tr_data)

        self.tr_data = []
        self.login_complete = False

        self.login()

    def login(self):
        self.ocx.dynamicCall("CommConnect()")
        print("로그인 중...")
        self.app.exec_()

    def _on_login(self, err_code):
        if err_code == 0:
            print("로그인 성공")
            self.login_complete = True
            
            # 시장 운영시간 체크
            if self.is_market_open():
                print("시장 운영시간입니다.")
                self.request_top_volume()
            else:
                print("현재 시장 운영시간이 아닙니다.")
                print("평일 09:00~15:30 시간에 실행해주세요.")
                # 시장 운영시간이 아니어도 테스트를 위해 요청해보기
                print("테스트를 위해 요청을 시도합니다...")
                self.request_top_volume()
        else:
            print(f"로그인 실패 (에러코드: {err_code})")
            self.app.quit()

    def is_market_open(self):
        """시장 운영시간 체크"""
        now = datetime.datetime.now()
        
        # 주말 체크
        if now.weekday() >= 5:  # 토요일(5), 일요일(6)
            return False
        
        # 시간 체크 (09:00 ~ 15:30)
        market_open = now.replace(hour=9, minute=0, second=0, microsecond=0)
        market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
        
        return market_open <= now <= market_close

    def request_top_volume(self):
        # OPT10023: 거래대금 상위 요청 TR
        # 입력값 설정
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "시장구분", "000")  # 000: 전체, 001: 코스피, 101: 코스닥
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "정렬구분", "1")    # 1: 거래대금순
        
        # TR 요청
        ret = self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", 
                                   "거래대금상위요청", "OPT10027", 0, "0186")
        
        if ret == 0:
            print("전일 대비 등락률 상위 요청 전송 완료")
        else:
            print(f"요청 전송 실패 (에러코드: {ret})")
            self.app.quit()

    def _on_receive_tr_data(self, screen_no, rqname, trcode, recordname,
                           prev_next, data_len, err_code, msg1, msg2):
        print(f"TR 데이터 수신 이벤트 발생")
        print(f"화면번호: {screen_no}, 요청명: {rqname}, TR코드: {trcode}")
        print(f"에러코드: {err_code}, 메시지1: {msg1}, 메시지2: {msg2}")
        print(f"데이터길이: {data_len}")
        
        if rqname == "거래대금상위요청":
            # 데이터 개수 확인
            data_count = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
            print(f"수신된 데이터 개수: {data_count}")
            
            if data_count > 0:
                print("\n[거래대금 상위 종목]")
                print("-" * 80)
                
                # 최대 20개까지 출력
                max_count = min(data_count, 20)
                
                for i in range(max_count):
                    # 정확한 필드명 사용
                    name = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", 
                                               trcode, rqname, i, "종목명").strip()
                    code = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", 
                                               trcode, rqname, i, "종목코드").strip()
                    volume = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", 
                                                 trcode, rqname, i, "거래량").strip()
                    value = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", 
                                                trcode, rqname, i, "거래대금").strip()
                    price = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", 
                                                trcode, rqname, i, "현재가").strip()
                    change = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", 
                                                 trcode, rqname, i, "전일대비").strip()
                    
                    # 데이터 정리 및 변환
                    try:
                        int_volume = int(volume) if volume else 0
                        int_value = int(value) if value else 0
                        int_price = int(price) if price else 0
                        int_change = int(change) if change else 0
                    except ValueError:
                        int_volume = int_value = int_price = int_change = 0
                    
                    # 출력
                    print(f"{i+1:2}. {name:<20} ({code}) - 현재가: {int_price:>8,}원 "
                          f"거래량: {int_volume:>12,} 거래대금: {int_value:>15,}원")
                
                print("-" * 80)
            else:
                print("수신된 데이터가 없습니다.")
                print("가능한 원인:")
                print("1. 시장 운영시간이 아님")
                print("2. 네트워크 연결 문제")
                print("3. API 서버 문제")
        
        self.app.quit()

if __name__ == "__main__":
    try:
        kiwoom = Kiwoom()
    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {e}")
        input("엔터를 눌러 종료하세요...")