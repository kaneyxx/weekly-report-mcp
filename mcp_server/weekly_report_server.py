import gspread
import datetime
import os
from mcp.server.fastmcp import FastMCP, Context
from typing import List, Dict, Optional

# Create an MCP server
mcp = FastMCP("Weekly Report Checker")

# Define the name lists
NAME_LIST = ["陳冠宇", "林柏志", "潘班", "董屹煊", "王宇軒", "許圃瑄", "陳冠言", "黃祈緯", "黃渝凌"]

# Get the path to the service account file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(CURRENT_DIR, "service_account.json")

def get_report_data() -> Dict[str, Dict]:
    """Helper function to get report data from Google Sheets"""
    # Connect to Google Sheets
    sa = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    sh = sa.open("週報")
    wks = sh.worksheet("週報")
    
    # Get current time
    current_time = datetime.datetime.now()
    
    # Dictionary to store report data for each person
    report_data = {name: {
        "submitted": False,
        "timestamp": None,
        "content": None,
        "days_ago": None
    } for name in NAME_LIST}
    
    # Check each row in the sheet
    for i in range(2, 15):  # Assuming data starts from row 2 and goes to row 14
        try:
            row = wks.get(f"A{i}:F{i}")
            if not row or not row[0][0]:  # Skip empty rows
                continue
                
            # Parse the timestamp from the sheet
            item_time = datetime.datetime.strptime(row[0][0], '%m/%d/%Y %H:%M:%S')
            name = row[0][2]  # Assuming name is in column C
            
            # Skip if the name is not in our list
            if name not in report_data:
                continue
                
            # Calculate days ago
            delta_sec = (current_time - item_time).total_seconds()
            days_ago = delta_sec / 86400  # Convert seconds to days
            
            # Check if the report was submitted within the last 6 days (518400 seconds + 12 hours buffer)
            if delta_sec < (518400 + 43200):
                report_data[name] = {
                    "submitted": True,
                    "timestamp": item_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "content": row[0][3] if len(row[0]) > 3 else "No content",  # Assuming content is in column D
                    "days_ago": round(days_ago, 1)
                }
        except Exception:
            continue
    
    return report_data

# Tool functions
@mcp.tool()
def check_missing_reports() -> str:
    """Check who hasn't submitted their weekly reports yet"""
    report_data = get_report_data()
    
    # Get names of people who haven't submitted
    missing_names = [name for name in NAME_LIST if not report_data[name]["submitted"]]
    
    # Format the response
    if missing_names:
        return f"本週未寫週報名單：{', '.join(missing_names)}"
    else:
        return "本週未寫週報名單：無"

@mcp.tool()
def check_person_report(name: str) -> str:
    """Check if a specific person has submitted their weekly report"""
    report_data = get_report_data()
    
    if name not in report_data:
        return f"找不到 {name} 的資料。請確認名字是否正確。"
    
    if report_data[name]["submitted"]:
        return f"{name} 已於 {report_data[name]['timestamp']} 提交週報（{report_data[name]['days_ago']} 天前）。\n內容摘要：{report_data[name]['content'][:100]}..."
    else:
        return f"{name} 尚未提交本週週報。"

@mcp.tool()
def get_submission_stats() -> str:
    """Get statistics about weekly report submissions"""
    report_data = get_report_data()
    
    # Calculate statistics
    total = len(NAME_LIST)
    submitted = sum(1 for name in NAME_LIST if report_data[name]["submitted"])
    
    return f"""週報提交統計：
已提交：{submitted}/{total} ({round(submitted/total*100 if total else 0, 1)}%)
"""

# Resource endpoints
@mcp.resource("weekly-report://status")
def get_report_status() -> str:
    """Get the current status of weekly report submissions"""
    return check_missing_reports()

@mcp.resource("weekly-report://stats")
def get_report_stats() -> str:
    """Get statistics about weekly report submissions"""
    return get_submission_stats()

@mcp.resource("weekly-report://all-members")
def get_all_members() -> str:
    """Get a list of all team members who should submit reports"""
    return f"需要繳交週報的成員：{', '.join(NAME_LIST)}"

@mcp.resource("weekly-report://person/{name}")
def get_person_status(name: str) -> str:
    """Get the status of a specific person's weekly report"""
    return check_person_report(name)

# Prompt templates
@mcp.prompt()
def check_reports_prompt() -> str:
    """Prompt to check who hasn't submitted their weekly reports"""
    return "請幫我檢查誰還沒有繳交本週的週報。"

@mcp.prompt()
def check_person_prompt() -> str:
    """Prompt to check a specific person's report status"""
    return "請幫我檢查特定人員的週報提交狀況。"

@mcp.prompt()
def get_stats_prompt() -> str:
    """Prompt to get statistics about weekly report submissions"""
    return "請幫我提供本週週報提交的統計資料。"

if __name__ == "__main__":
    mcp.run()