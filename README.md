- [한국어 (Korean)](README.ko.md)

# Pi-Monitor

Pi-Monitor is a simple Python-based server monitoring tool. It connects to multiple remote servers via SSH, performs various health and service checks concurrently, and logs the results.

This tool is designed for system administrators who need a quick and customizable way to check the status of multiple servers.

## Features

-   **Parallel Monitoring:** Uses a thread pool to monitor multiple servers simultaneously.
-   **SSH-Based Checks:** Connects to servers using SSH (Paramiko) to execute commands.
-   **Extensible Check Modules:** Easily add new checks for different services.
-   **Service Checks:**
    -   **System:** CPU, memory, and disk usage (`vmstat`, `df`).
    -   **Apache:** Process status, service status, and error logs.
    -   **Tomcat:** Process status, service status, error logs, and `context.xml` resource settings.
    -   **Network:** Firewall status (`firewalld`) and listening ports (`ss`).
    -   **Other Agents:** Supports checks for custom agents like ChangeFlow and Ecredible.
-   **Configuration:** Server lists are managed via simple JSON files.
-   **Logging:** Saves detailed monitoring results to a `logs` directory.

## Project Structure

```
pi-monitor/
├── src/
│   ├── check/         # Modules for specific service checks (Apache, Tomcat, etc.)
│   ├── utils/         # Utility functions (logging, metrics)
│   ├── config.py      # Loads server configurations
│   ├── monitor.py     # Core monitoring logic for a single server
│   └── ssh_utils.py   # SSH command execution helper
├── main.py            # Main entry point to run all monitors
├── servers.spl.json   # Sample server configuration file
├── run_prd.bat        # Sample run script for production environment
└── README.md          # This file
```

## How to Use

### 1. Prerequisites

-   Python 3.x
-   Required libraries: `paramiko`, `python-dotenv`

Install the dependencies:
```bash
pip install paramiko python-dotenv
```

### 2. Configuration

**a. Create a `.env` file:**

Create a `.env` file in the project root to store the SSH credentials.

```
ADMIN_USER=your_ssh_username
ADMIN_PASS=your_ssh_password
```

**b. Create a Server Configuration File:**

Create a JSON file for each environment (e.g., `servers.dev.json`, `servers.prod.json`). This file contains the list of servers to monitor.

See `servers.spl.json` for an example.

-   `host`: The server's IP address or hostname.
-   `type`: The server type (`apache` or `tomcat`). This determines which checks to run.
-   `where`, `envFile`, `service`: Additional parameters for specific checks.

**Example `servers.dev.json`:**
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

### 3. Running the Monitor

Execute `main.py` with the environment name as an argument. The default environment is `dev`.

**To run for the 'dev' environment:**
```bash
python main.py dev
```
or simply:
```bash
python main.py
```

**To run for the 'prod' environment:**
```bash
python main.py prod
```

The monitoring results will be printed to the console and saved in the `logs/` directory.
