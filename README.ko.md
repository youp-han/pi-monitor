- [English (영어)](README.md)

# Pi-Monitor (파이 모니터)

Pi-Monitor는 Python으로 작성된 간단한 서버 모니터링 도구입니다. SSH를 통해 여러 원격 서버에 동시에 접속하여 다양한 상태 및 서비스 점검을 병렬로 수행하고 결과를 로그 파일로 저장합니다.

이 도구는 여러 서버의 상태를 빠르고 유연하게 확인해야 하는 시스템 관리자를 위해 설계되었습니다.

## 주요 기능

-   **병렬 모니터링:** 스레드 풀을 사용하여 여러 서버를 동시에 모니터링합니다.
-   **SSH 기반 점검:** SSH(Paramiko 라이브러리)를 통해 서버에 접속하고 명령어를 실행합니다.
-   **확장 가능한 점검 모듈:** 다양한 서비스에 대한 새로운 점검 모듈을 쉽게 추가할 수 있습니다.
-   **서비스 점검 항목:**
    -   **시스템:** CPU, 메모리, 디스크 사용량 (`vmstat`, `df`).
    -   **Apache:** 프로세스 상태, 서비스 상태, 에러 로그.
    -   **Tomcat:** 프로세스 상태, 서비스 상태, 에러 로그, `context.xml` 리소스 설정.
    -   **네트워크:** 방화벽 상태(`firewalld`), 리스닝 포트(`ss`).
    -   **기타 에이전트:** ChangeFlow, Ecredible 등 커스텀 에이전트 점검을 지원합니다.
-   **설정 관리:** 모니터링할 서버 목록을 간단한 JSON 파일로 관리합니다.
-   **로깅:** 상세한 모니터링 결과를 `logs` 디렉터리에 저장합니다.

## 프로젝트 구조

```
pi-monitor/
├── src/
│   ├── check/         # 서비스별 점검 모듈 (Apache, Tomcat 등)
│   ├── utils/         # 유틸리티 함수 (로깅, 메트릭)
│   ├── config.py      # 서버 설정 로드
│   ├── monitor.py     # 단일 서버에 대한 핵심 모니터링 로직
│   └── ssh_utils.py   # SSH 명령어 실행 헬퍼
├── main.py            # 모든 모니터를 실행하는 메인 스크립트
├── servers.spl.json   # 샘플 서버 설정 파일
├── run_prd.bat        # 운영 환경용 샘플 실행 스크립트
└── README.ko.md       # 현재 파일
```

## 사용 방법

### 1. 사전 준비

-   Python 3.x
-   필요 라이브러리: `paramiko`, `python-dotenv`

의존성을 설치합니다:
```bash
pip install paramiko python-dotenv
```

### 2. 설정

**a. `.env` 파일 생성:**

프로젝트 루트에 `.env` 파일을 생성하여 SSH 접속 정보를 저장합니다.

```
ADMIN_USER=your_ssh_username
ADMIN_PASS=your_ssh_password
```

**b. 서버 설정 파일 생성:**

각 환경(예: `dev`, `prod`)에 맞는 JSON 파일을 생성합니다. 이 파일은 모니터링할 서버 목록을 포함합니다.

샘플 파일로 `servers.spl.json`을 참고하세요.

-   `host`: 서버의 IP 주소 또는 호스트명.
-   `type`: 서버 타입 (`apache` 또는 `tomcat`). 실행할 점검 항목을 결정합니다.
-   `where`, `envFile`, `service`: 특정 점검에 필요한 추가 파라미터.

**`servers.dev.json` 예시:**
```json
[
    {
        "host": "192.168.1.10",
        "type": "tomcat",
        "service": "cfagent"
    },
    {
        "host": "192.168.1.11",
        "type": "apache",
        "where": "my-service",
        "envFile": "dev"
    }
]
```

### 3. 모니터 실행

`main.py`를 실행할 때 환경 이름을 인자로 전달합니다. 기본 환경은 `dev`입니다.

**'dev' 환경으로 실행:**
```bash
python main.py dev
```
또는 간단히:
```bash
python main.py
```

**'prod' 환경으로 실행:**
```bash
python main.py prod
```

모니터링 결과는 콘솔에 출력되고 `logs/` 디렉터리에 저장됩니다.
