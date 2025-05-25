# login.py

from PyQt5.QtWidgets import QApplication
from PyQt5.QAxContainer import QAxWidget

class Kiwoom:
    def __init__(self):
        self.app = QApplication([])
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self._on_login)
        self.login_status = False

    def login(self):
        self.ocx.dynamicCall("CommConnect()")
        self.app.exec_()  # 이벤트 루프 실행

    def _on_login(self, err_code):
        if err_code == 0:
            print("로그인 성공")
            self.login_status = True
        else:
            print("로그인 실패")
        self.app.quit()  # 로그인 끝나면 이벤트 루프 종료
