import re
import requests
import pprint
import time
import json
from bs4 import BeautifulSoup as bs
from io import BytesIO
import base64
from requests.sessions import Session

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class PASSAgent:
    """
    PASS 본인 인증 Agent
    """
    _data: dict = {}
    _session: Session
    _menu_id: str
    _timestamp: int

    def _get_menu_id(self, response: str) -> str:
        """`menuId`값 getter

        주어진 response에서 `menuId` 값 64글자를 리턴합니다

        Args:
            response (response): requests.get/post의 응답 결과

        Returns:
            menu_id (str): `menuId` 값
        """
        data = response.text

        menu_id = re.search(
            r'menuId\s{0,}=\s{0,}"([a-z\d]{64})"', data).group(1)

        return menu_id

    def get_data(self):
        return pprint.pformat(self._data)

    def __init__(self, session: Session = Session()):
        self._session = session

    def start(self, encode_data):

        self._data.update({"encode_data": encode_data})

        res = self._session.post(
            "https://nice.checkplus.co.kr/CheckPlusSafeModel/service.cb", data={
                "m": "checkplusSerivce",
                "EncodeData": encode_data
            })

        self._menu_id = self._get_menu_id(res)
        return res.text

    def check_by_sms(self, mno, name, birth, sex, mobile_number):
        """sms 본인확인

        Args:
            mno (str): 통신사
            name (str): 실명
            birth (digit[6]): YYMMDD형식의 생년월일
            sex (digit): 성별(주민등록번호 뒤 7자리 중 첫번째 숫자)
            mobile_number (numbers): 휴대폰 번호(no hyphen'-')

        Returns:
            (str): 응답 텍스트
        """
        data = {
            "m": "authMobile01",
            "mobileAuthType": "SMS",
            "nciInfo": "",
            "menuId": self._menu_id,
            "mobileco": mno,
            "agree": "on",  # 전체 동의
            "agree1": "Y",  # 개인정보이용동의
            "agree2": "Y",  # 고유식별정보처리동의
            "agree3": "Y",  # 서비스이용약관동의
            "agree4": "Y",  # 통신사이용약관동의
        }

        self._data.update({
            "name": name,
            "birth": birth,
            "sex": sex,
            "mobile_number": mobile_number
        })

        res = self._session.post(
            "https://nice.checkplus.co.kr/CheckPlusSafeModel/service.cb", data=data)

        self._menu_id = self._get_menu_id(res)

        # BDC_VCID_CAPTCHA 값 추출 후 저장
        html = res.text
        soup = bs(html, 'html.parser')
        self._data.update({
            "BDC_DATA": {
                "BDC_VCID_CAPTCHA": soup.find(
                    'input', {'name': 'BDC_VCID_CAPTCHA'}).attrs['value']
            }
        })
        return res.text

    def get_captcha(self, mode="image"):
        """bot detect captcha image/sound request

        Args:
            mode (str, optional): [description]. Defaults to "image".

        Returns:
            [type]: [description]
        """

        url = "https://nice.checkplus.co.kr/botdetectcaptcha"

        self._timestamp = int(time.time())

        # GET p
        res = self._session.get(url, params={
            "get": "p",
            "c": "CAPTCHA",
            "t": self._data
            .get("BDC_DATA")
            .get("BDC_VCID_CAPTCHA"),
            "d": self._timestamp
        })

        p_data = json.loads(res.text)  # p_data dictionary로 변환

        self._data.get("BDC_DATA").update({
            "BDC_Hs_CAPTCHA": p_data.get("hs"),
            "BDC_SP_CAPTCHA": p_data.get("sp"),
        })

        # GET image/sound
        res = self._session.get(url, params={
            "get": mode,  # image or sound
            "c": "CAPTCHA",
            "t": self._data
            .get("BDC_DATA")
            .get("BDC_VCID_CAPTCHA"),
            "d": self._timestamp
        })

        # base64 encoded image
        image = BytesIO(res.content).read()
        b64image = base64.b64encode(image)
        return b64image

    def check_captcha(self, answer: str):
        """CAPTCHA validation request

        Args:
            answer (str): [description]
        """

        url = "https://nice.checkplus.co.kr/botdetectcaptcha"

        res = self._session.get(url, params={
            "get": "validation-result",
            "c": "CAPTCHA",
            "t": self._data
            .get("BDC_DATA")
            .get("BDC_VCID_CAPTCHA"),
            "d": time,  # TODO modify
            "i": answer
        })

        is_success = (lambda x: x == "true")

        if(is_success(res.text)):
            res = self._session.post(url, data={
                "m": "authMobile01Proc",
                "authType": "SMS",
                "menuId": self._menu_id,
                "username": "",
                "mynum1": "",
                "mynum2": "",
                "mobileno": "",
                "BDC_VCID_CAPTCHA": "",
                "BDC_BackWorkaround_CAPTCHA": "1",
                "BDC_Hs_CAPTCHA": "",
                "BDC_SP_CAPTCHA": "",
                "answer": answer
            })

    def request_auth(self, type: str = "sms"):
        pass

    def check_auth(self, auth_number: str):
        pass
