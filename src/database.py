import sqlite3
import os

# Получаем абсолютный путь к базе данных, чтобы избежать проблем с путями
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, 'donors.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            blood_type TEXT,
            contact TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_donor(name, age, blood_type, contact):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO donors (name, age, blood_type, contact)
        VALUES (?, ?, ?, ?)
    ''', (name, age, blood_type, contact))
    conn.commit()
    conn.close()

def get_donors(blood_type=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if blood_type:
        cursor.execute("SELECT * FROM donors WHERE blood_type = ?", (blood_type,))
    else:
        cursor.execute("SELECT * FROM donors")
    donors = cursor.fetchall()
    conn.close()
    return donors


def delete_donor(donor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM donors WHERE id = ?', (donor_id,))
    conn.commit()
    conn.close()

def get_donor_by_id(donor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM donors WHERE id = ?', (donor_id,))
    donor = cursor.fetchone()
    conn.close()
    return donor

def update_donor(donor_id, name, age, blood_type, contact):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE donors
        SET name = ?, age = ?, blood_type = ?, contact = ?
        WHERE id = ?
    ''', (name, age, blood_type, contact, donor_id))
    conn.commit()
    conn.close()

def get_filtered_donors(name=None, age=None, blood_type=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM donors WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if age:
        query += " AND age = ?"
        params.append(age)
    if blood_type:
        query += " AND blood_type = ?"
        params.append(blood_type)

    cursor.execute(query, params)
    donors = cursor.fetchall()
    conn.close()
    return donors


# Инициализация базы данных при запуске
if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
