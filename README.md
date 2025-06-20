# pi-monitor
- a script to monitor resources from the linux servers
- servers.spl.json contains server info
  -- host: ip, type: "apache" or "tomcat", where "apache" foldername. it's in the code
  -- envFile "extdev" the file name

# requires .env file containing credential info to log into servers
ADMIN_USER=username
ADMIN_PASS=password

# running the monitoring app
python main.py spl

