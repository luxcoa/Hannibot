## 설치 방법

1. **레포지토리 다운로드**:
    - [여기](https://github.com/luxcoa/hannibot/tree/main/Hannibot)에서 프로젝트 파일을 다운로드합니다.
      ![Download ZIP](https://img.icons8.com/ios-filled/50/000000/download-2.png) <!-- 다운로드 아이콘 추가 -->
    - `Code` 버튼을 클릭하고 `Download ZIP`을 선택하여 ZIP 파일로 다운로드하거나, 직접 파일을 복사할 수 있습니다.

2. **프로젝트 디렉토리로 이동**:
    ```sh
    cd Hannibot
    ```
    - 다운로드한 `Hannibot` 디렉토리로 이동하여 프로젝트 파일에 접근합니다.
      ![Command Line](https://img.icons8.com/ios-filled/50/000000/command-line.png) <!-- 명령어 아이콘 추가 -->

3. **종속성 설치**:
    ```sh
    pip install -r requirements.txt
    ```
    - 프로젝트에 필요한 모든 패키지를 설치합니다. `requirements.txt` 파일에는 필요한 라이브러리 목록이 포함되어 있습니다.
      ![Requirements](https://img.icons8.com/ios-filled/50/000000/requirements.png) <!-- 요구 사항 아이콘 추가 -->

4. **토큰으로 봇 설정**:
    - `코드 내 30번째 줄`에서 `'Token'` 부분에 자신의 봇 토큰을 입력합니다. 
    - **토큰 보안 주의**: 자신의 토큰을 안전하게 보관하고 외부에 노출되지 않도록 주의하세요.

5. **봇 실행**:
    - Windows + R 키를 눌러 실행 창을 열고 `cmd`를 입력하여 명령 프롬프트를 실행합니다. 
    - 아래 명령어를 입력하여 봇을 실행합니다:
    ```
    python (파일이름).py
    ```
    - `(파일이름)`은 실제 Python 파일의 이름으로 대체해야 합니다. 예를 들어, `bot.py`라면 `python bot.py`로 입력합니다.
      ![Run Command](https://img.icons8.com/ios-filled/50/000000/play.png) <!-- 실행 아이콘 추가 -->

## 라이선스

이 프로젝트는 [GNU General Public License v2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)에 따라 라이선스가 부여됩니다. 이 라이선스는 사용자에게 소스 코드를 자유롭게 사용, 수정 및 배포할 수 있는 권한을 부여합니다. 하지만 다음 조건을 준수해야 합니다:

- 모든 복제본 또는 수정본에는 원래 저작자 및 라이선스 정보를 명시해야 합니다.
- 출처를 명시하지 않고 한디리 (koreanbots.dev) 또는 Top.gg 등 봇 배포 사이트에 등록한 경우, 저작자의 권리를 침해하는 것으로 간주될 수 있습니다.
- 소스 코드를 수정하여 배포하는 경우, 동일한 라이선스 조건에 따라 배포해야 합니다.
- 이 소스코드의 오용으로 인해 발생하는 문제나 손해에 대해 저작자는 법적 책임과 지지 않습니다.

자세한 내용은 [LICENSE](https://github.com/pokelochi/minjeongbot/blob/main/LICENSE) 파일을 참조해 주세요. 이 라이선스 조건을 이해하고 준수하는 것은 사용자 본인의 책임입니다.

## 기여 방법

- 기여를 원하시는 분은 다음 단계를 따라 주세요:
  1. 레포지토리를 포크(Fork)
  2. 새로운 브랜치를 생성: `git checkout -b feature/YourFeature`
  3. 변경 사항을 커밋: `git commit -m "Add some feature"`
  4. 포크한 레포지토리에 푸시: `git push origin feature/YourFeature`
  5. Pull Request (PR)을 생성하여 변경 사항을 제안해주세요!

<p align="center">
  <img src="https://img.shields.io/github/stars/luxcoa/hannibot?style=social" alt="Stars" />
  <img src="https://img.shields.io/github/forks/luxcoa/hannibot" alt="Forks" />
  <img src="https://img.shields.io/github/issues/luxcoa/hannibot" alt="Open Issues" />
  <img src="https://img.shields.io/github/contributors/luxcoa/hannibot" alt="Contributors" />
  <img src="https://img.shields.io/github/last-commit/luxcoa/hannibot" alt="Last Commit" />
</p>

## 연락처

- 문제가 발생하거나 궁금한 점이 있으시면, 아래의 이메일로 문의해 주세요.:
  - hannifam@proton.me
