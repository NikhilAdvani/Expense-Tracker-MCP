from fastmcp import FastMCP
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP("ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)

init_db()

@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    '''Add a new expense entry to the database.'''

    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "ok", "id": cur.lastrowid}
    
@mcp.tool()
def list_expenses(start_date, end_date):
    '''List expense entries within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def summarize(start_date, end_date, category=None):
    '''Summarize expenses by category within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    
@mcp.tool()
def edit_expense(id: int, date=None, amount=None, category=None, subcategory=None, note=None):
    '''Update one or more fields of an existing expense entry.'''
    
    # First check if the expense exists
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("SELECT * FROM expenses WHERE id = ?", (id,))
        if not cur.fetchone():
            return {"status": "error", "message": f"Expense with id {id} not found"}
        
        # Build the UPDATE query dynamically based on provided parameters
        updates = []
        params = []
        
        if date is not None:
            updates.append("date = ?")
            params.append(date)
        if amount is not None:
            updates.append("amount = ?")
            params.append(amount)
        if category is not None:
            updates.append("category = ?")
            params.append(category)
        if subcategory is not None:
            updates.append("subcategory = ?")
            params.append(subcategory)
        if note is not None:
            updates.append("note = ?")
            params.append(note)
        
        if not updates:
            return {"status": "error", "message": "No fields provided to update"}
        
        # Add the id to params for the WHERE clause
        params.append(id)
        
        query = f"UPDATE expenses SET {', '.join(updates)} WHERE id = ?"
        c.execute(query, params)
        
        return {"status": "ok", "id": id, "updated_fields": len(updates)}

@mcp.tool()
def delete_expense(id: int):
    '''Delete an expense entry by ID.'''
    
    with sqlite3.connect(DB_PATH) as c:
        # First check if the expense exists
        cur = c.execute("SELECT * FROM expenses WHERE id = ?", (id,))
        expense = cur.fetchone()
        
        if not expense:
            return {"status": "error", "message": f"Expense with id {id} not found"}
        
        # Delete the expense
        c.execute("DELETE FROM expenses WHERE id = ?", (id,))
        
        return {"status": "ok", "id": id, "message": "Expense deleted successfully"}

@mcp.tool()
def search_expenses(keyword: str):
    '''Search expenses by keyword in notes, category, or subcategory.'''
    
    with sqlite3.connect(DB_PATH) as c:
        # Use LIKE with wildcards for flexible searching
        search_pattern = f"%{keyword}%"
        
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE note LIKE ? 
               OR category LIKE ? 
               OR subcategory LIKE ?
            ORDER BY date DESC
            """,
            (search_pattern, search_pattern, search_pattern)
        )
        
        cols = [d[0] for d in cur.description]
        results = [dict(zip(cols, r)) for r in cur.fetchall()]
        
        return {
            "status": "ok",
            "keyword": keyword,
            "count": len(results),
            "results": results
        }

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()
    
@mcp.resource("expense://instructions", mime_type="text/plain")
def instructions():
    return f"""
Expense Tracker Instructions:
- current_date: {datetime.now().strftime("%Y-%m-%d")}
- If the user provides a relative date (e.g., "today", "last Tuesday", "yesterday"),
    you MUST use current_date to determine today's date,
    then calculate the correct date according to the user's requirement.
"""

if __name__ == "__main__":
    mcp.run()