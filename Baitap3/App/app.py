from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection information
DB_NAME = 'dbtest'
USER = 'postgres'
PASSWORD = '123456'
HOST = 'localhost'
PORT = '5432'

def connect_db():
    return psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username == "admin" and password == "123":
        session['logged_in'] = True
        return redirect(url_for('student_management'))
    else:
        flash('Invalid username or password!')
        return redirect(url_for('home'))

@app.route('/student_management', methods=['GET', 'POST'])
def student_management():
    if not session.get('logged_in'):
        return redirect(url_for('home'))

    conn = connect_db()
    cur = conn.cursor()

    if request.method == 'POST':
        # Adding a new student
        if 'add_student' in request.form:
            hoten = request.form['hoten']
            mssv = request.form['mssv']
            nganh = request.form['nganh']
            namsinh = request.form['namsinh']
            try:
                insert_query = "INSERT INTO sinhvien (hoten, mssv, nganh, namsinh) VALUES (%s, %s, %s, %s)"
                cur.execute(insert_query, (hoten, mssv, nganh, namsinh))
                conn.commit()
                flash('Thêm sinh viên thành công!')
            except Exception as e:
                conn.rollback()
                flash(f'Lỗi khi thêm sinh viên!')

        # Deleting a student
        elif 'delete_student' in request.form:
            mssv = request.form['mssv']
            try:
                delete_query = "DELETE FROM sinhvien WHERE mssv = %s"
                cur.execute(delete_query, (mssv,))
                conn.commit()
                flash('Sinh viên đã được xóa!')
            except Exception as e:
                conn.rollback()
                flash(f'Lỗi khi xóa sinh viên!')

        # Searching for students
        elif 'search_student' in request.form:
            search_value = request.form['search_value']
            search_query = "SELECT * FROM sinhvien WHERE hoten ILIKE %s OR CAST(mssv AS TEXT) ILIKE %s OR nganh ILIKE %s OR CAST(namsinh AS TEXT) ILIKE %s"
            search_pattern = f"%{search_value}%"
            cur.execute(search_query, (search_pattern, search_pattern, search_pattern, search_pattern))
            students = cur.fetchall()  # Fetch searched students and display them
            cur.close()  # Close cursor to avoid conflicts
            conn.close()  # Close connection after search
            return render_template('student_management.html', students=students)

    # If it's a GET request or no POST action
    cur.execute("SELECT * FROM sinhvien")
    students = cur.fetchall()  # Always fetch all students at the end

    cur.close()
    conn.close()
    return render_template('student_management.html', students=students)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
