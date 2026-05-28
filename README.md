# wuma-proxy 사용 설명서

같은 네트워크에서 컴퓨터2의 명조 맵스를 컴퓨터1의 트래커와 연동하는 프록시입니다.

---

## 구조

컴퓨터1 : 명조, 명조 맵스 트래커 서버 실행 PC
컴퓨터2 : 명조 맵스 브라우저 실행, 프록시 기능 실행 PC
```
[컴퓨터2: maps.wuwa.moe]
        ↓  ws://localhost:46821  (로컬 연동)
[컴퓨터2: wuma-proxy.exe]
        ↓  ws://컴퓨터1IP:46821  (LAN)
[컴퓨터1: 명조 맵스 트래커]
```

---

## 준비 (최초 1회)

### 컴퓨터1 설정

1. [명조 맵스 트래커](https://github.com/wuwamoe/wuma-tracker/releases/latest) 설치 및 실행
2. 고급 설정 펼치기
3. IP 주소를 `0.0.0.0` 으로 변경
4. "설정 적용 및 서버 재시작" 클릭
5. `ipconfig` 명령어로 IPv4 주소 확인 (예: `192.168.0.10`)

### 컴퓨터2 빌드

1. [Python 다운로드](https://www.python.org/downloads/) 후 설치
   - **"Add Python to PATH" 반드시 체크!**
2. `wuma_proxy.py` 와 `build.bat` 을 같은 폴더에 저장
3. `build.bat` 더블클릭
4. `dist\wuma-proxy.exe` 생성 확인

---

## 매번 사용하는 방법

### 컴퓨터1

1. 명조 맵스 트래커 실행
2. 게임 실행 후 "게임 연결" 버튼 클릭

### 컴퓨터2

1. `wuma-proxy.exe` 실행
   - 처음 실행 시 컴퓨터1의 IP 주소 입력 (이후 자동 저장)
2. [maps.wuwa.moe](https://maps.wuwa.moe) 접속
3. 트래커 연동 메뉴에서 **"로컬 연동"** 버튼 클릭

---

## 파일 구조

```
wuma-proxy.exe     <- 실행 파일
tracker_ip.txt     <- 컴퓨터1 IP 저장 (자동 생성)
```

tracker_ip.txt 를 삭제하면 다음 실행 시 IP를 다시 입력할 수 있습니다.

---

## 문제 해결

**"Cannot connect to tracker" 오류**
- 컴퓨터1에서 트래커 앱이 실행 중인지 확인
- 트래커 고급 설정에서 IP가 `0.0.0.0` 인지 확인
- 컴퓨터1 Windows 방화벽에서 포트 46821 허용 필요할 수 있음

**"Port 46821 is already in use" 오류**
- 컴퓨터2에 트래커 앱이 설치되어 실행 중이면 종료 후 프록시 실행

**IP가 바뀐 경우**
- `tracker_ip.txt` 파일 삭제 후 프록시 재실행
