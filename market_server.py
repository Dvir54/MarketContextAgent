from mcp.server.fastmcp import FastMCP
import yfinance as yf
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# create the server
mcp = FastMCP("Market-Analyzer")

# get stock price tool
@mcp.tool()
def get_stock_price(ticker: str) -> str:
    """
    get the current price and percentage change of a specific stock.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        current_price = info.get('regularMarketPrice') or info.get('currentPrice')
        prev_close = info.get('previousClose')
        
        if current_price and prev_close:
            change = ((current_price - prev_close) / prev_close) * 100
            return f"The current price of {ticker} is ${current_price:.2f} ({change:+.2f}%)"
        return f"Could not find complete price data for {ticker}."
    except Exception as e:
        return f"Error fetching price for {ticker}: {str(e)}"


# get stock news tool
@mcp.tool()
def get_stock_news(ticker: str) -> str:
    """
    get the latest news for a specific stock.
    """
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        
        if not news:
            return f"No news available for {ticker}."
        
        report = f"Latest news for {ticker}:\n\n"
        valid_news_count = 0
        
        # get the latest 5 news items
        for i, news_item in enumerate(news[:3], 1):
            # The news data is nested inside 'content' dictionary
            content = news_item.get('content', {})
            
            # Extract title
            title = content.get('title', '')
            
            # Extract summary/description
            summary = content.get('summary', content.get('description', ''))
            
            # Extract provider (nested in a dictionary)
            provider_dict = content.get('provider', {})
            if isinstance(provider_dict, dict):
                provider = provider_dict.get('displayName', 'Unknown source')
            else:
                provider = 'Unknown source'
            
            # Extract date (already in string format)
            pub_date = content.get('pubDate', content.get('displayTime', ''))
            
            # Extract URL (nested in canonicalUrl dictionary)
            canonical_url = content.get('canonicalUrl', {})
            if isinstance(canonical_url, dict):
                url = canonical_url.get('url', '')
            else:
                url = ''
            
            # Fallback to clickThroughUrl if canonicalUrl not found
            if not url:
                click_url = content.get('clickThroughUrl', {})
                if isinstance(click_url, dict):
                    url = click_url.get('url', '')
            
            # Only include news items that have at least a title
            if title:
                valid_news_count += 1
                report += f"{valid_news_count}. {title}\n"
                report += f"   Source: {provider}\n"
                report += f"   Published: {pub_date if pub_date else 'Date not available'}\n"
                if summary:
                    report += f"   Summary: {summary}\n"
                report += f"   Link: {url if url else 'No link available'}\n\n"
        
        if valid_news_count == 0:
            return f"News data for {ticker} is available but lacks complete metadata. Try using a web search or financial news site for {ticker} news instead."
        
        return report.strip()
    except Exception as e:
        return f"Error fetching news for {ticker}: {str(e)}"


# send email alert tool
@mcp.tool()
def send_email_alert(ticker: str, analysis_report: str) -> str:
    """
    Send an email alert about significant stock movement with the analysis report.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'AAPL', 'TSLA')
        analysis_report: The detailed analysis report to include in the email body
    
    Returns:
        Success or error message
    """
    sender_email = os.getenv("SENDER_EMAIL", "dvir54693@gmail.com")
    receiver_email = os.getenv("RECEIVER_EMAIL", "dvir54693@gmail.com")
    app_password = os.getenv("EMAIL_APP_PASSWORD")
    
    # Check if app password is configured
    if not app_password:
        return "❌ Error: EMAIL_APP_PASSWORD environment variable is not set. Please configure it in your .env file."
    
    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"🚀 Stock Alert: Significant movement in {ticker}!"
    
    # Attach the analysis report as the email body
    message.attach(MIMEText(analysis_report, "plain"))
    
    try:
        # Port 465 is used for SSL/TLS encrypted connection
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            
            # Send the email
            server.send_message(message)
            
        return f"✅ Email alert sent successfully for {ticker}!"
    
    except smtplib.SMTPAuthenticationError:
        return "❌ Error: Authentication failed. Please check your email and App Password."
    
    except smtplib.SMTPException as e:
        return f"❌ SMTP error occurred: {str(e)}"
    
    except Exception as e:
        return f"❌ Error sending email: {str(e)}"


# test tool
@mcp.tool()
def check_connection() -> str:
    """test if the MCP server is connected and active."""
    return "the connection is successful! the financial analyst is ready to work."

if __name__ == "__main__":
    mcp.run()