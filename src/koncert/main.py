from typing import Dict
import requests
from bs4 import BeautifulSoup as bs
from io import BytesIO
from requests.sessions import Session

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class PASSAgent:
    """
    PASS 본인 인증 Agent
    """
    _data: dict
    _session: Session

    def __init__(self, session: Session = Session()):
        self._session = session

    def start(self, encode_data):
        res = self._session.post(
            "https://nice.checkplus.co.kr/CheckPlusSafeModel/service.cb", data={
                "m": "checkplusSerivce",
                "EncodeData": encode_data
            })
        print(res.text)
