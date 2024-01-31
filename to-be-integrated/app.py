# app.py

from flask import Flask, jsonify, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Update the connection string with your own database details
connection_string = 'Driver={SQL Server};Server=tcp:server29janpraneet.database.windows.net,1433;Database=db29jan;Uid=dbadmin;Pwd={Localhost@1234567};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
def get_db_connection():
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    fullname = request.form.get('fullname')
    phone = request.form.get('phone')
    conn = get_db_connection()
    parts = email.split('@')
    username = parts[0]
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO User_Table (email, fullname, phone, username) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (email, fullname, phone, username))
            conn.commit()
            cursor.close()
            conn.close()

            message = 'Registration Successful!'
            return render_template('index.html', message=message)
        except Exception as e:
            print(f"Error during registration: {str(e)}")
            conn.rollback()
            return render_template('index.html', message='Email ID already registered. Please go to Login Page.')
    else:
        return render_template('index.html', message='Unable to connect to the database.')

if __name__ == '__main__':
    app.run(debug=True)
