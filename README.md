# :studio_microphone: KONCERT : NICE 본인인증 스크래핑 </br> ![pypi version](https://img.shields.io/pypi/v/koncert) [![License: MIT](https://img.shields.io/pypi/l/koncert)](https://opensource.org/licenses/MIT)
> NICE 본인인증 스크래핑 라이브러리

[ORCINUS: 해군교육사령부 모바일 인터넷편지 시스템](https://github.com/jiwonMe/orcinus)을 만들면서 본인 인증을 서비스 내부로 집어넣어야 했는데, 구현 과정에서 분리시킨 프로젝트입니다.

NICE 본인인증모듈의 패킷 요청 및 응답을 분석하고, django에서 사용할 수 있는 python 라이브러리를 제공합니다.

## Support
- NICE 휴대폰본인확인

## Installation

```bash
pip install koncert
```

## Usage

```python
import koncert
from requests.session import Session

with Session() as s :
    agent = koncert.PASSAgent(session=s)
    agent.start(encode_data="[ENCODE DATA]") # 업체정보 암호화 데이터

    # 문자로 인증
    agent.check_by_sms(
            mno = "SKT", # 통신사
            name = "김철수", # 실명
            birth="010615", # 주민등록번호 앞 6자리
            sex="3", # 주민등록번호 뒤 첫번째 숫자
            mobile_number="01012345678" # 휴대폰 번호
        )

    # 보안문자 이미지 받아오기 (base64 encoded)
    img = agent.get_captcha()

    # 보안문자 정답 전송
    answer = input()
    agent.check_captcha(answer)

    # 인증번호 문자 발송 요청
    agent.request_auth(type="sms")

    # 인증번호 입력
    auth_number = input()
    agent.check_auth(auth_number)

    # 인증 결과 수신
    result = agent.get_result()
    print(result)

```

## Reference

- [NICE아이디 휴대폰본인확인 서비스 설명 페이지](https://www.niceid.co.kr/prod_mobile.nc)

## Legal Notices

본 라이브러리를 사용하여 대한민국 법률에 위배되는 서비스를 제작하는 것을 엄격하게 금합니다.