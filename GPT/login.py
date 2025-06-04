# login.py
from PyQt5.QtWidgets import QApplication
from PyQt5.QAxContainer import QAxWidget
import sys
import time

class Kiwoom:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        self.ocx.OnEventConnect.connect(self._on_login)
        self.ocx.OnReceiveTrData.connect(self._on_receive_tr_data)

        self.account_number = ''   # 계좌번호 저장
        self.tr_data = {}          # 수신 데이터 저장용

        self.login()

    def login(self):
        self.ocx.dynamicCall("CommConnect()")
        print("로그인 중...")
        self.app.exec_()

    def _on_login(self, err_code):
        if err_code == 0:
            print("로그인 성공")
            self.account_number = self.get_account_info()
            print("계좌번호:", self.account_number)

            # 예수금 조회 요청
            self.request_deposit()
        else:
            print("로그인 실패", err_code)
            self.app.quit()

    def get_account_info(self):
        account_list = self.ocx.dynamicCall("GetLoginInfo(QString)", "ACCNO")
        accounts = account_list.split(';')
        return accounts[0]

    def request_deposit(self):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_number)
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")  # 필요시 실제 비밀번호 입력
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
        self.ocx.dynamicCall("SetInputValue(QString, QString)", "조회구분", "2")
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", "예수금상세현황요청", "opw00001", 0, "0101")
        print("예수금 조회 요청 전송 완료")

    def _on_receive_tr_data(self, screen_no, rqname, trcode, recordname, prev_next, data_len, error_code, message, splm_msg):
        if rqname == "예수금상세현황요청":
            deposit = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)",
                                           trcode, rqname, 0, "예수금")
            deposit = int(deposit.strip())
            print(f"예수금: {deposit:,}원")
            self.app.quit()
