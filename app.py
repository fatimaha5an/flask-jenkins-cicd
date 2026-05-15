from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "students.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    db = get_db()
    students = db.execute('SELECT * FROM students').fetchall()
    db.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get('name', '').strip()
    grade = data.get('grade', '').strip()
    if not name or not grade:
        return jsonify({'error': 'Name and grade are required'}), 400
    db = get_db()
    db.execute('INSERT INTO students (name, grade) VALUES (?, ?)', (name, grade))
    db.commit()
    db.close()
    return jsonify({'message': 'Student added successfully'}), 201

@app.route('/students', methods=['GET'])
def get_students():
    db = get_db()
    students = db.execute('SELECT * FROM students').fetchall()
    db.close()
    return jsonify([dict(s) for s in students])

@app.route('/delete/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    db = get_db()
    db.execute('DELETE FROM students WHERE id = ?', (student_id,))
    db.commit()
    db.close()
    return jsonify({'message': 'Student deleted'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
