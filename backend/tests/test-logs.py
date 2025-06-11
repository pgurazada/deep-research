import sqlite3

def read_logs(db_path="backend/research-logs.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, query, result FROM research_logs ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    if not rows:
        print("No logs found.")
        return
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"Timestamp: {row[1]}")
        print(f"Query: {row[2]}")
        print(f"Result: {row[3]}")
        print("-" * 40)

if __name__ == "__main__":
    read_logs()