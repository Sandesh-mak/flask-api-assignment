import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = "students.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO students (name, department, email)
            VALUES (?, ?, ?)
        ''', ("Sandesh Makhija", "Computer Science", "sandesh.makhija@example.com"))
    conn.commit()
    conn.close()

# 1. GET /students - Retrieve all students
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    students = conn.execute('SELECT id, name, department, email FROM students').fetchall()
    conn.close()
    return jsonify([{
        'id': row['id'],
        'name': row['name'],
        'department': row['department'],
        'email': row['email']
    } for row in students]), 200

# 2. GET /students/<id> - Retrieve a specific student
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db_connection()
    student = conn.execute('SELECT id, name, department, email FROM students WHERE id = ?', (student_id,)).fetchone()
    conn.close()
    if student is None:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify({
        'id': student['id'],
        'name': student['name'],
        'department': student['department'],
        'email': student['email']
    }), 200

# 3. POST /students - Add a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'department', 'email')):
        return jsonify({'error': 'Missing required fields: name, department, email'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO students (name, department, email) VALUES (?, ?, ?)',
        (data['name'], data['department'], data['email'])
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        'id': new_id,
        'name': data['name'],
        'department': data['department'],
        'email': data['email']
    }), 201

# 4. PUT /students/<id> - Update a student's information
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request payload'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    student = cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    if student is None:
        conn.close()
        return jsonify({'error': 'Student not found'}), 404
        
    name = data.get('name', student['name'])
    department = data.get('department', student['department'])
    email = data.get('email', student['email'])
    
    cursor.execute(
        'UPDATE students SET name = ?, department = ?, email = ? WHERE id = ?',
        (name, department, email, student_id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({
        'id': student_id,
        'name': name,
        'department': department,
        'email': email
    }), 200

# 5. DELETE /students/<id> - Delete a student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    student = cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    if student is None:
        conn.close()
        return jsonify({'error': 'Student not found'}), 404
        
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': f'Student with ID {student_id} deleted successfully'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)