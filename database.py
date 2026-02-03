import sqlite3
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

DB_NAME = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            deadline TEXT,
            priority TEXT,
            completed INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def insert_task(task):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (title, description, deadline, priority, completed)
        VALUES (?, ?, ?, ?, ?)
    """, (task.title, task.description, task.deadline.strftime("%d.%m.%Y"), task.priority, int(task.completed)))

    conn.commit()
    conn.close()


def get_all_tasks():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    conn.close()
    return rows

def filter_by_priority(priority):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE priority = ?", (priority,))
    rows = cursor.fetchall()

    conn.close()
    return rows


def filter_by_status(completed):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE completed = ?", (completed,))
    rows = cursor.fetchall()

    conn.close()
    return rows


def filter_by_deadline_before(date_str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE deadline <= ?", (date_str,))
    rows = cursor.fetchall()

    conn.close()
    return rows

def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

    deleted = cursor.rowcount  # сколько строк удалено
    conn.close()

    return deleted > 0

def mark_task_done(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = 1
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated > 0

def mark_task_not_done(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = 0
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated > 0

def search_by_title(keyword):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    keyword_lower = keyword.lower()

    result = []
    for row in rows:
        task_id, title, description, deadline, priority, completed = row
        if keyword_lower in title.lower():
            result.append(row)

    return result

def export_to_csv(filename="tasks.csv"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    conn.close()

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Title", "Description", "Deadline", "Priority", "Completed"])
        for row in rows:
            task_id, title, description, deadline, priority, completed = row
            if description:
                description = description.replace("\n", " ").replace("\r", " ")

            writer.writerow([task_id, title, description, deadline, priority, completed])

    return True

def export_to_pdf(filename="tasks.pdf"):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    data = [["ID", "Title", "Description", "Deadline", "Priority", "Completed"]]

    for row in rows:
        task_id, title, description, deadline, priority, completed = row

        if description:
            description = description.replace("\n", " ").replace("\r", " ")

        status = "Completed" if completed else "In process"

        data.append([task_id, title, description, deadline, priority, status])

    pdf = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title_style.alignment = 1  # центрирование

    title = Paragraph("Task List", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))  # отступ

    table = Table(data)

    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ])

    table.setStyle(style)
    elements.append(table)

    pdf.build(elements)
    return True

def clear_all_tasks():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks")
    conn.commit()

    conn.close()
    return True

def update_task(task_id, title=None, description=None, deadline=None, priority=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return False

    current_id, current_title, current_description, current_deadline, current_priority, current_completed = row

    new_title = title if title else current_title
    new_description = description if description else current_description
    new_deadline = deadline if deadline else current_deadline
    new_priority = priority if priority else current_priority

    cursor.execute("""
        UPDATE tasks
        SET title = ?, description = ?, deadline = ?, priority = ?
        WHERE id = ?
    """, (new_title, new_description, new_deadline, new_priority, task_id))

    conn.commit()
    conn.close()
    return True
