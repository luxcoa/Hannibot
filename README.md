# Winterbot

이 레포지토리는 Seong Park의 원본 [Discord-Yena-Bot](https://github.com/seongpark/Discord-Yena-Bot)을 수정한 것입니다.

## 변경 사항

- 새로운 명령어 추가
- 대체로 수정.
- yena-bot -> winterbot (IZONE 예나의 대한 정보 봇 -> aespa 윈터의 대한 정보 봇으로 변경.) 

## 설치 방법

1. 저장소를 클론하기:
    ```sh
    git clone https://github.com/pokelochi/mingjeong.git
    ```
2. 프로젝트 디렉토리로 이동:
    ```sh
    cd winterbot
    ```
3. 가상 환경을 생성하고 활성화:
    ```sh
    python -m venv venv
    source venv/bin/activate  # Windows에서는 `venv\Scripts\activate`
    ```
4. 종속성 설치:
    ```sh
    pip install -r requirements.txt
    ```
5. Discord 토큰으로 봇을 설정:
    ```client.run('token')에 자신의 봇 토큰을 넣기.```
6. 윈도우 + R로 실행을 열고 cmd를 입력해 열어 아래 명령어를 입력:
    ```
    python (파일이름).py
    ```

## 라이선스

이 프로젝트는 GNU General Public License v2.0에 따라 라이선스가 부여됩니다 - 자세한 내용은 [LICENSE]([LICENSE](https://github.com/pokelochi/minjeongbot/blob/main/LICENSE)) 파일을 참조해주세요.
