# ❓ 자주 묻는 질문 (FAQ)

## 기본 사항

### Q: HanniBot은 어떤 봇인가요?
- 하니봇은 특정 아이돌의 정보 제공과 서버 관리, 게임 기능을 제공하는 다목적 봇입니다.
- 파이썬으로 개발되었으며, Py-cord 라이브러리를 기반으로 제작되었습니다.

### Q: 봇을 서버에 초대하려면 어떻게 해야 하나요?
1. [초대 링크](https://discord.com/oauth2/authorize?client_id=1235089708992696391&permissions=564049867844624&integration_type=0&scope=bot+applications.commands)를 클릭합니다.
2. 봇을 추가할 서버를 선택합니다.
3. 필요한 권한을 확인하고 '승인'을 클릭합니다.

### Q: 봇 사용에 비용이 있나요?
- 하니봇은 완전 무료로 제공됩니다.
- ~~단, 봇의 일부 고급 기능은 서버 부스트나 한디리 투표 등의 조건이 필요할 수 있습니다.~~

## 설치 및 설정

### Q: 봇 설치 시 최소 시스템 요구사항은 무엇인가요?
- Python 3.8 이상
- RAM: 최소 512MB (권장 1GB)
- 저장공간: 최소 100MB
- 안정적인 인터넷 연결

### Q: `pip install -r requirements.txt` 실행 시 오류가 발생해요.
1. 파이썬이 제대로 설치되어 있는지 확인:
```bash
python --version
```
2. pip가 최신 버전인지 확인
```bash
python -m pip install --upgrade pip
```
3. 가상 환경을 사용 권장
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate  # Windows
```

### Q: 봇 토큰은 어디서 얻나요?
1. [디스코드 개발자 포털](https://discord.com/developers/applications)에 접속
2. 'New Application' 클릭
3. Bot 섹션에서 'Add Bot' 클릭
4. 'Reset Token'을 클릭하여 새 토큰 발급
5. **주의**: 토큰은 절대 공개하지 않는게 좋습니다.


### Q: 봇이 응답하지 않아요.
1. 봇이 온라인 상태인지 확인해주세요.
2. 봇이 명령어를 사용할 채널의 권한을 가지고 있는지 확인해주세요.
3. 명령어를 사용할 권한이 있는지 확인해주세요.
4. 봇의 명령어 중 `/버그제보` 명령어를 사용하여 제보해주세요.
5. [GitHub Issues](https://github.com/luxcoa/hannibot/issues)에 제보해주세요.

## 오류 해결

### Q: "Py-cord is not installed" 오류가 발생해요.
```bash
pip install py-cord
```
실행 후 봇을 재시작해주세요.

### Q: "Importer Token is invalid" 오류가 발생해요.
1. 봇 파일 안에 토큰이 올바른지 확인해주세요.
2. 개발자 포털에서 토큰이 유효한지 확인해주세요.
3. 필요한 경우 새 토큰을 발급 받는게 좋습니다.

## 기타 문의

### Q: 버그를 발견했어요.
1. 봇의 명령어 중 `/버그제보` 명령어를 사용하여 제보해주세요.
2. [GitHub Issues](https://github.com/luxcoa/hannibot/issues)에 제보해주세요.
3. 가능한 한 자세한 정보를 제공해주세요:
   - 발생 상황
   - 오류 메시지
   - 실행 환경


### Q: 추가 지원이 필요해요.
- 이메일: hannifam@proton.me
- Discord: lux_co
- [서포트 서버](https://discord.gg/8xZtuQ5rsr)

---

> 💡 **도움말**: 이 FAQ에서 답을 찾지 못했다면, [서포터 서버](https://discord.gg/8xZtuQ5rsr)에서 문의해주세요.

> ⚠️ **주의사항**: 봇 토큰이나 민감한 정보는 절대 공개하지 않는게 좋습니다.