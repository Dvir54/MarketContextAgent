# 🤖 MarketContextAgent

**An Autonomous AI Financial Analyst powered by Claude Code CLI and Model Context Protocol**

MarketContextAgent is an intelligent monitoring system that autonomously tracks stock market volatility and delivers instant email alerts when significant price movements occur. Built on Claude's agentic AI framework with a custom MCP server, this agent operates 24/7 without human intervention.

---

## ✨ Features

- **🎯 Real-Time Market Monitoring**: Tracks stock prices using live Yahoo Finance data
- **📊 Intelligent Threshold Detection**: Triggers analysis when price movement exceeds 10%
- **🧠 Context-Aware Analysis**: Synthesizes recent news to identify market catalysts
- **📧 Automated Email Alerts**: Sends professional analysis reports to your inbox
- **⚡ 24/7 Autonomous Operation**: Runs continuously via Windows Task Scheduler
- **🔒 Secure by Design**: Environment variables and granular permissions for safe execution

---

## 🏗️ Architecture: The Reasoning-Action-Observation Loop

MarketContextAgent implements a **RAO loop** where Claude operates as the reasoning engine and the custom FastMCP server acts as its interface to external systems:

**1. Task Scheduling** → Windows Task Scheduler executes the agent every 30 minutes

**2. Reasoning Phase** → Claude receives instruction: _"Analyze [TICKER] and alert if price moved more than 10%"_

**3. Action Phase** → Claude calls MCP tools in sequence:
   - `get_stock_price(ticker)` → Retrieves current price and % change
   - **Decision Gate**: If |change| < 10%, workflow terminates (resource optimization)
   - If |change| ≥ 10%, proceeds to `get_stock_news(ticker)`
   - Synthesizes professional financial analysis report
   - `send_email_alert(ticker, report)` → Delivers insights via email

**4. Observation** → Claude receives tool results and adapts based on success/failure

**5. Logging** → All output appended to `agent_log.txt` for audit trails

### Custom MCP Tools

| Tool | Technology | Purpose |
|------|-----------|---------|
| `get_stock_price(ticker)` | yfinance | Fetches real-time price and % change |
| `get_stock_news(ticker)` | yfinance | Retrieves latest news headlines |
| `send_email_alert(ticker, report)` | smtplib + Gmail | Sends formatted email alerts |
| `check_connection()` | FastMCP | Validates server health |

---

## 🛠️ Tech Stack

- **AI Engine**: Claude 3.5 Sonnet (via Claude Code CLI)
- **MCP Framework**: FastMCP (Python)
- **Data Source**: yfinance (Yahoo Finance API)
- **Communication**: smtplib + Gmail SMTP
- **Automation**: Windows Task Scheduler + Batch Script
- **Security**: python-dotenv + `.env` file

---

## 📦 Installation

### Prerequisites

- Python 3.11+
- [Claude Code CLI](https://docs.anthropic.com/en/docs/build-with-claude/claude-code)
- Gmail Account with [App Password](https://support.google.com/accounts/answer/185833)

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/MarketContextAgent.git
cd MarketContextAgent

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Configure Environment Variables

Create `.env` file in project root:

```env
SENDER_EMAIL=your_email@gmail.com
RECEIVER_EMAIL=your_email@gmail.com
EMAIL_APP_PASSWORD=your_16_digit_app_password
```

### Verify Installation

```bash
python market_server.py
```

Expected output: `MCP Server running on stdio`

---

## 🚀 Usage

### Manual Execution

```bash
claude "Analyze AAPL and alert me via email if price moved more than 10%"
```

### 24/7 Automation (Windows Task Scheduler)

**1. Edit `run_stock_agent.bat`:**

```batch
@echo off
cd /d "C:\path\to\MarketContextAgent"
call claude "Analyze TSLA and alert me via email if price moved more than 10%" >> agent_log.txt 2>&1
exit
```

**2. Configure Task Scheduler:**
- Open Task Scheduler → Create Task
- **General**: Name = `MarketContextAgent`, Run whether user is logged on or not
- **Triggers**: Daily, repeat every 30 minutes
- **Actions**: Run `run_stock_agent.bat`

**3. Test:** Right-click task → Run, then check `agent_log.txt`

---

## 📁 Project Structure

```
MarketContextAgent/
├── market_server.py           # FastMCP server with custom tools
├── run_stock_agent.bat        # Automated execution script
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (gitignored)
├── .claudecode.md             # Claude's operational instructions
└── agent_log.txt              # Execution history (gitignored)
```

---

## 🔒 Security Features

- **Granular Permissions**: Claude operates in "don't ask" mode with tool-specific access
- **10% Threshold Filter**: Prevents spam by only alerting on significant movements
- **Environment Variables**: Credentials stored in `.env` (never committed to Git)
- **Audit Logging**: All actions logged to `agent_log.txt`
- **Gmail App Passwords**: Uses app-specific passwords instead of account credentials

---

## 🔮 Future Enhancements

- Multi-stock portfolio monitoring from config file
- SMS alerts via Twilio integration
- Web dashboard for real-time visualization
- Historical backtesting and threshold optimization

---

## 📧 Contact

**Dvir** - [dvir54693@gmail.com](mailto:dvir54693@gmail.com)

**Project Link**: [https://github.com/yourusername/MarketContextAgent](https://github.com/yourusername/MarketContextAgent)

---

<div align="center">
  <strong>Built with Claude Code CLI and Model Context Protocol</strong>
  <br>
  <em>Demonstrating the future of Agentic AI</em>
</div>
