from PyQt5.QAxContainer import QAxWidget
import logging

logger = logging.getLogger(__name__)

class KiwoomAPI:
    def __init__(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.connected = False
        self.account_list = []
        self.account_num = ""
        self.ocx.OnEventConnect.connect(self.on_event_connect)

    def login(self):
        try:
            ret = self.ocx.dynamicCall("CommConnect()")
            if ret == 0:
                logger.info("로그인 요청 성공")
                return True
            else:
                logger.error(f"로그인 요청 실패: {ret}")
                return False
        except Exception as e:
            logger.error(f"로그인 중 오류: {e}")
            return False

    def on_event_connect(self, err_code):
        if err_code == 0:
            self.connected = True
            self.get_account_info()
            logger.info("로그인 성공")
        else:
            logger.error(f"로그인 실패: {err_code}")

    def get_account_info(self):
        acc_list = self.ocx.dynamicCall("GetLoginInfo(QString)", "ACCLIST")
        self.account_list = acc_list.split(';')[:-1]
        if self.account_list:
            self.account_num = self.account_list[0]
            logger.info(f"계좌번호: {self.account_num}")
