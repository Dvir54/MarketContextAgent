echo off@
cd /d "C:\Users\dvir5\Projects\MarketContextAgent"
call claude "Analyze ONDS and alert me via email if price moved more than 10%" >> agent_log.txt 2>&1
exit