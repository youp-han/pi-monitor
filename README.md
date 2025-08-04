# pi-monitor


**pi-monitor** is a Python script for monitoring resources and logs on multiple Linux servers (Apache, Tomcat, etc.) via SSH. It checks CPU, disk, service status, and log files, then prints and saves the results.

---

## Configuration Files

### servers.{env}.json

Contains the list and information of servers to monitor.

```json
[
  {
    "host": "192.168.0.10",
    "type": "apache",      // "apache" or "tomcat"
    "where": "web01",      // Folder name for apache
    "envFile": "extdev"    // Used for log file name
  }
]
```

### .env

Stores SSH credentials for server access.

```
ADMIN_USER=your_ssh_username
ADMIN_PASS=your_ssh_password
```

---

## Features

- Connects to each server via SSH and checks:
  - CPU/memory usage (`vmstat`, `top`)
  - Disk usage (`df`)
  - Service status (`systemctl status`)
  - Error lines in main log files (Apache, Tomcat)
  - Port status (`ss`)
  - Tomcat context.xml resource settings

- Results are printed to the console and saved as `logs/monitor_{host}_{datetime}.log`.

---

## 설치 및 실행

### 1. 환경 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고, SSH 접속에 필요한 관리자 계정 정보를 추가합니다.

```
ADMIN_USER=your_ssh_username
ADMIN_PASS=your_ssh_password
```

### 2. 서버 설정

모니터링할 서버 정보를 담은 JSON 파일을 생성합니다. 파일명은 `servers.{환경}.json` 형식이어야 합니다 (예: `servers.dev.json`, `servers.qas.json`, `servers.prd.json`).

예시: `servers.dev.json`
```json
[
  {
    "host": "your_server_ip_1",
    "type": "tomcat",
    "where": "dev",
    "envFile": "dev",
    "service": "cfagent"
  },
  {
    "host": "your_server_ip_2",
    "type": "apache",
    "where": "dev",
    "envFile": "dev",
    "service": ""
  }
]
```

- `host`: 서버 IP 주소 또는 호스트명
- `type`: 모니터링할 서버 유형 (예: `tomcat`, `apache`)
- `where`: 서버 위치 또는 환경 (예: `dev`, `qas`, `prd`)
- `envFile`: 환경 파일명 (로그 경로 구성에 사용)
- `service`: 추가로 확인할 서비스 (예: `cfagent`, `ecredible`, 없으면 빈 문자열)

### 3. 의존성 설치

Python 3.x가 설치되어 있어야 합니다. 필요한 라이브러리를 설치합니다.

```bash
pip install paramiko python-dotenv
```

### 4. 모니터링 실행

`MONITOR_ENV` 환경 변수를 설정한 후 `main.py`를 실행합니다.

```bash
# 개발 환경 모니터링 (Windows)
run_dev.bat

# QAS 환경 모니터링 (Windows)
run_qas.bat

# PRD 환경 모니터링 (Windows)
run_prd.bat
```

또는 직접 환경 변수를 설정하고 Python 스크립트를 실행할 수 있습니다.

```bash
# 개발 환경 모니터링 (Windows)
set MONITOR_ENV=dev && python main.py

# 또는 QAS 환경 모니터링 (Windows)
set MONITOR_ENV=qas && python main.py
```

실행 후 `logs` 디렉토리에 모니터링 결과 로그 파일이 생성됩니다.

### 5. 보고서 통합

생성된 모든 개별 로그 파일을 하나의 통합 보고서로 합치려면 `aggregate_report.py`를 실행합니다.

```bash
# 통합 보고서 생성 (Windows)
make_report.bat
```

또는 직접 Python 스크립트를 실행할 수 있습니다.

```bash
python aggregate_report.py
```

`logs` 디렉토리에 `aggregated_report_YYYYMMDD_HHMMSS.log` 파일이 생성됩니다.

---

## 프로젝트 구조

```
.
├── aggregate_report.py       # 모니터링 로그 통합 스크립트
├── main.py                   # 메인 실행 스크립트
├── main.spec                 # PyInstaller 스펙 파일
├── make_report.bat           # 통합 보고서 생성 배치 파일
├── run_dev.bat               # 개발 환경 모니터링 실행 배치 파일
├── run_prd.bat               # 운영 환경 모니터링 실행 배치 파일
├── run_qas.bat               # QAS 환경 모니터링 실행 배치 파일
├── servers.spl.json          # 서버 설정 예시 파일 (servers.{환경}.json 형식으로 복사하여 사용)
├── README.md                 # 프로젝트 설명 파일
├── .env                      # 환경 변수 설정 파일 (ADMIN_USER, ADMIN_PASS)
├── logs/                     # 모니터링 로그 저장 디렉토리
└── src/
    ├── config.py             # 설정 로드 및 관리
    ├── monitor.py            # 서버 모니터링 로직
    ├── ssh_utils.py          # SSH 유틸리티 함수
    ├── check/                # 각 서비스별 점검 로직
    │   ├── apache.py
    │   ├── network.py
    │   ├── service.py
    │   ├── system.py
    │   ├── tomcat_log.py
    │   └── tomcat.py
    └── utils/
        ├── log_helpers.py    # 로그 저장 유틸리티
        └── metrics.py        # 지표 관련 유틸리티
```

---

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다.


# PiMonitor

PiMonitor는 원격 서버의 상태를 모니터링하고 보고서를 생성하는 Python 기반의 도구입니다. SSH를 통해 서버에 접속하여 시스템 리소스, 서비스 상태, 로그 파일 등을 점검하고, 그 결과를 파일로 저장합니다.

## 주요 기능

- **시스템 상태 모니터링**: CPU, 메모리, 디스크 사용량 등 시스템 전반의 건강 상태를 점검합니다.
- **서비스 상태 확인**: Apache, Tomcat 등 주요 웹/애플리케이션 서버의 프로세스 및 서비스 상태를 확인합니다.
- **로그 파일 분석**: Apache, Tomcat 로그 파일에서 에러를 탐지하고 보고합니다.
- **네트워크 및 방화벽 점검**: 특정 포트의 LISTEN 상태 및 firewalld 서비스 상태를 확인합니다.
- **보고서 생성**: 모니터링 결과를 개별 로그 파일로 저장하고, 모든 로그를 통합한 보고서를 생성합니다.



---


