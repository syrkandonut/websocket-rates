# Websocket Rates APP 
A high-performance asynchronous REST and WebSocket API that streams real-time currency exchange rates (pegged to **RUB** by default) with an integrated volatility simulation.

Powered by a modern, production-grade Python stack.

# Technologies
- Python 3.12
- aiohttp, websockets
- dishka
- ruff, mypy
- Thank's to `https://open.er-api.com/v6/latest/` 

# Features
- **Dynamic REST API:** Fetch the latest official exchange rates on-demand.
- **Synchronized WebSocket Stream:** Broadcasts real-time rate updates simultaneously to all connected clients.
- **Market Volatility Simulator:** Uses a custom randomized algorithm to simulate real-time live trading fluctuations on top of steady upstream data.
- **Asynchronous custom cache**
- **Vibecoded Frontend** (sorry...)
- **Google Docs-Style Presence Tracking:** See who else is currently analyzing the same currency in real-time. The app tracks the total active user count and dynamically generates anonymous, random nicknames just like Google Docs!
  
  *Examples of what you'll see on the dashboard:*
  - 🦊 `Cool Fox`
  - 🪙 `Rich Capy`
  - 🕷️ `Smart Spider`

<img width="738" height="626" alt="image" src="https://github.com/user-attachments/assets/e7c61740-1c72-4676-8f58-650ba9329b33" />

# Getting Started

### Run the application
  ```bash
  make run
  ```
### What's next?
Go to 
```bash
http://host:port/USD
``` 
Use USD, EUR, CNY, JPY etc. 

# Code Quality Standards
This project maintains strict static analysis compliance
