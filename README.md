# Honeypot Monitoring System  

A simple **Flask + Streamlit-based Honeypot** that logs suspicious HTTP requests, stores them in JSON format, and visualizes them in a real-time dashboard.  

---

## Features  
- Logs every HTTP request (path, method, headers, body, IP, timestamp).  
- Detects **suspicious activities** like requests to `/admin`, `/.env`, `/api/login`, etc.  
- **JSON-based log storage** (`logs/honeypot.json`).  
- Interactive **Streamlit dashboard** with:  
  - Request distribution (Pie Chart).  
  - Requests by HTTP Method (Bar Chart).  
  - Top Attacking IPs (Bar Chart).  
  - Suspicious events summary.  
  - Expandable raw logs view.  
- Auto-refresh every **5 seconds** for real-time monitoring.  

---

## Project Structure 
honeypot-project/
│
├── app.py # Flask Honeypot backend
├── dashboard.py # Streamlit dashboard
├── logs/
│ └── honeypot.json # JSON log file (auto-generated)
├── requirements.txt # Dependencies

## Dashboard Preview
- Pie Chart: Requests by Path
- Bar Chart: Requests by Method
- Bar Chart: Top Attacking IPs
- Table: Expandable Raw Logs

## Author
Ena Luhadia
