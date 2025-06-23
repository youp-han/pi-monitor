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

## How to Run

1. **Prepare the .env file**  
   Create a `.env` file in the project root with your SSH credentials.

2. **Prepare the server info file**  
   Create `servers.{env}.json` for each environment (e.g., dev, prod, spl).

3. **Run the monitor**  
   Use the following command:
   ```bash
   python main.py spl
   ```
   - Replace `spl` with your environment name (`dev`, `prod`, etc.).
   - If omitted, the default is `dev`.

---

## Notes

- Logs are automatically saved in the `logs` directory.
- Monitoring is performed in parallel for all servers.
- If SSH fails or files are missing, error messages will be shown.

---

**Example:**
```bash
python main.py dev
```
This will monitor all servers listed in `servers.dev.json`.

---

If you have any questions, feel free
