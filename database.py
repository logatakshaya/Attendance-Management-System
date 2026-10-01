import sqlite3
import hashlib


DATABASE = "attendance.db"


def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def create_database():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            year TEXT NOT NULL,
            section TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (student_id)
            REFERENCES students(student_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        SELECT user_id
        FROM users
        WHERE username = ?
    """, ("admin",))

    admin_exists = cursor.fetchone()

    if not admin_exists:

        cursor.execute("""
            INSERT INTO users
            (username, password)
            VALUES (?, ?)
        """, (
            "admin",
            hash_password("admin123")
        ))

    conn.commit()
    conn.close()

    renumber_student_ids()


def login_user(username, password):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id
        FROM users
        WHERE username = ?
        AND password = ?
    """, (
        username,
        hash_password(password)
    ))

    user = cursor.fetchone()

    conn.close()

    if user:
        return True

    return False


def change_password(username, new_password):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET password = ?
        WHERE username = ?
    """, (
        hash_password(new_password),
        username
    ))

    conn.commit()
    conn.close()


def renumber_student_ids():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id
        FROM students
        ORDER BY student_id
    """)

    students = cursor.fetchall()

    if not students:

        cursor.execute("""
            DELETE FROM sqlite_sequence
            WHERE name = 'students'
        """)

        conn.commit()
        conn.close()

        return

    for (old_id,) in students:

        cursor.execute("""
            UPDATE attendance
            SET student_id = ?
            WHERE student_id = ?
        """, (
            -old_id,
            old_id
        ))

        cursor.execute("""
            UPDATE students
            SET student_id = ?
            WHERE student_id = ?
        """, (
            -old_id,
            old_id
        ))

    for new_id, (old_id,) in enumerate(
        students,
        start=1
    ):

        cursor.execute("""
            UPDATE students
            SET student_id = ?
            WHERE student_id = ?
        """, (
            new_id,
            -old_id
        ))

        cursor.execute("""
            UPDATE attendance
            SET student_id = ?
            WHERE student_id = ?
        """, (
            new_id,
            -old_id
        ))

    cursor.execute("""
        DELETE FROM sqlite_sequence
        WHERE name = 'students'
    """)

    cursor.execute("""
        INSERT INTO sqlite_sequence
        (name, seq)
        VALUES ('students', ?)
    """, (
        len(students),
    ))

    conn.commit()
    conn.close()


def add_student(
    name,
    roll_no,
    department,
    year,
    section
):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO students
            (
                name,
                roll_no,
                department,
                year,
                section
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            roll_no,
            department,
            year,
            section
        ))

        conn.commit()

        result = True

    except sqlite3.IntegrityError:

        result = False

    conn.close()

    return result


def get_students():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            student_id,
            name,
            roll_no,
            department,
            year,
            section
        FROM students
        ORDER BY student_id
    """)

    students = cursor.fetchall()

    conn.close()

    return students


def search_students(search_text):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    search_value = f"%{search_text}%"

    cursor.execute("""
        SELECT
            student_id,
            name,
            roll_no,
            department,
            year,
            section
        FROM students
        WHERE name LIKE ?
        OR roll_no LIKE ?
        OR department LIKE ?
        ORDER BY student_id
    """, (
        search_value,
        search_value,
        search_value
    ))

    students = cursor.fetchall()

    conn.close()

    return students


def update_student(
    student_id,
    name,
    roll_no,
    department,
    year,
    section
):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE students
            SET
                name = ?,
                roll_no = ?,
                department = ?,
                year = ?,
                section = ?
            WHERE student_id = ?
        """, (
            name,
            roll_no,
            department,
            year,
            section,
            student_id
        ))

        conn.commit()

        result = True

    except sqlite3.IntegrityError:

        result = False

    conn.close()

    return result


def delete_student(student_id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM attendance
        WHERE student_id = ?
    """, (
        student_id,
    ))

    cursor.execute("""
        DELETE FROM students
        WHERE student_id = ?
    """, (
        student_id,
    ))

    conn.commit()
    conn.close()

    renumber_student_ids()


def save_attendance(
    student_id,
    date,
    status
):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT attendance_id
        FROM attendance
        WHERE student_id = ?
        AND date = ?
    """, (
        student_id,
        date
    ))

    existing = cursor.fetchone()

    if existing:

        cursor.execute("""
            UPDATE attendance
            SET status = ?
            WHERE attendance_id = ?
        """, (
            status,
            existing[0]
        ))

    else:

        cursor.execute("""
            INSERT INTO attendance
            (
                student_id,
                date,
                status
            )
            VALUES (?, ?, ?)
        """, (
            student_id,
            date,
            status
        ))

    conn.commit()
    conn.close()


def get_attendance_by_date(date):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            students.student_id,
            students.name,
            students.roll_no,
            attendance.status
        FROM students
        LEFT JOIN attendance
        ON students.student_id =
           attendance.student_id
        AND attendance.date = ?
        ORDER BY students.student_id
    """, (
        date,
    ))

    records = cursor.fetchall()

    conn.close()

    return records


def get_attendance_records():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            attendance.attendance_id,
            students.student_id,
            students.name,
            students.roll_no,
            attendance.date,
            attendance.status
        FROM attendance
        JOIN students
        ON attendance.student_id =
           students.student_id
        ORDER BY attendance.date DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records


def get_student_attendance(student_id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            date,
            status
        FROM attendance
        WHERE student_id = ?
        ORDER BY date DESC
    """, (
        student_id,
    ))

    records = cursor.fetchall()

    conn.close()

    return records


def get_student_attendance_summary(student_id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(
                CASE
                    WHEN status = 'Present'
                    THEN 1
                    ELSE 0
                END
            ),
            SUM(
                CASE
                    WHEN status = 'Absent'
                    THEN 1
                    ELSE 0
                END
            )
        FROM attendance
        WHERE student_id = ?
    """, (
        student_id,
    ))

    result = cursor.fetchone()

    conn.close()

    total = result[0] if result[0] else 0
    present = result[1] if result[1] else 0
    absent = result[2] if result[2] else 0

    return total, present, absent