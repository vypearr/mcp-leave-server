from typing import Any
from mcp.server.fastmcp import FastMCP

# Start MCP server
mcp = FastMCP("HRLeaveAssistant")

# In-memory mock database
employee_leaves = {
    "E001": {"balance": 18, "history": ["2024-12-25", "2025-01-01"]},
    "E002": {"balance": 20, "history": []}
}

@mcp.tool()
def request_leave(emp_id: str, leave_date: str) -> str:
    """Request leave on a specific date (YYYY-MM-DD)"""
    if emp_id not in employee_leaves:
        return "Employee not found."
    if leave_date in employee_leaves[emp_id]["history"]:
        return "Leave already taken on this date."
    if employee_leaves[emp_id]["balance"] <= 0:
        return "Insufficient leave balance."
    employee_leaves[emp_id]["history"].append(leave_date)
    employee_leaves[emp_id]["balance"] -= 1
    return (
        f"Leave for {leave_date} approved for {emp_id}. "
        f"Remaining balance: {employee_leaves[emp_id]['balance']}"
    )

@mcp.tool()
def check_balance(emp_id: str) -> str:
    """Check available leave balance"""
    if emp_id not in employee_leaves:
        return "Employee not found."
    return f"{emp_id} has {employee_leaves[emp_id]['balance']} day(s) of leave remaining."

@mcp.tool()
def leave_history(emp_id: str) -> str:
    """View leave dates taken"""
    if emp_id not in employee_leaves:
        return "Employee not found."
    history = employee_leaves[emp_id]["history"]
    return f"{emp_id} has taken leave on: {', '.join(history) if history else 'No leaves taken.'}"

@mcp.resource("leave://{emp_id}")
def leave_summary(emp_id: str) -> str:
    """Leave summary resource"""
    if emp_id not in employee_leaves:
        return "Employee not found."
    balance = employee_leaves[emp_id]["balance"]
    history = employee_leaves[emp_id]["history"]
    return (
        f"{emp_id} Leave Summary:\n"
        f"- Balance: {balance} day(s)\n"
        f"- History: {', '.join(history) if history else 'No leaves taken'}"
    )

app = mcp
