from flask import Flask, request, render_template ,session,redirect,url_for
import random
import smtplib
import pyodbc
from flask_mail import Mail,Message
import random
from flask_cors import CORS
from flask import jsonify   

app = Flask(__name__)
app.secret_key = 'e5c8b6c9c00e150734cd07ab14af9ee5'
CORS(app)
CORS(app, origins=["http://127.0.0.1:5000/"])  

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465 
app.config['MAIL_USERNAME'] = 'bbonzana@gmail.com'
app.config['MAIL_PASSWORD'] = 'eojchcxcrdozgnkb'
app.config['MAIL_USE_TLS'] = False 
app.config['MAIL_USE_SSL'] = True 
mail=Mail(app)

server = 'dbserver23jandeepak.database.windows.net'
database = 'dbfeedbackmgt'
username = 'dbadmin'
password = 'Localhost@1234567'
driver = '{SQL Server}'

cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server +
                      ';PORT=1433;DATABASE=' + database +
                      ';UID=' + username + ';PWD=' + password)

otp_storage = {}
stored_email = None

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')

# Define global variables to store email and OTP
global_email = None
global_otp = None

@app.route('/send_otp', methods=['GET', 'POST'])
def send_otp():
    global global_email, global_otp  # Access the global variables
    if request.method == 'POST':
        email = request.form['email']
        otp = random.randint(100000, 999999)
        otp_storage[email] = otp
        session['otp'] = otp
        msg = Message("Your OTP", sender='bbonzana@gmail.com', recipients=[email])
        msg.body = f"Your OTP is: {otp}"
        mail.send(msg)
        print(f"OTP sent: {otp}")
        # Store email and OTP in global variables
        global_email = email
        global_otp = otp
        return redirect(url_for('verify_otp'))
    return render_template('login.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    global global_email, global_otp  # Access the global variables
    if request.method == 'POST':
        cursor = cnxn.cursor()
        # Use global_email and global_otp instead of request.form.get()
        email = global_email
        otp_str = global_otp
        print(f"Received email: {email}")
        print(f"Received OTP string: {otp_str}")
        if otp_str is not None:
            otp = int(otp_str)
            if otp_storage.get(email) == otp:
                cursor.execute("SELECT Name, Role FROM Users WHERE Email = ?", email)
                row = cursor.fetchone()
                if row:
                    if row.Role.lower() == 'trainer':
                        return render_template('Trainer.html', name=row.Name, email=email)
                    elif row.Role.lower() == 'student':
                        return render_template('Student.html', name=row.Name, email=email)
                else:
                    return render_template('register.html', email=email)
            else:
                return 'Invalid OTP. Please try again.'
        else:
            return 'Invalid OTP'

    # Handle GET request
    return render_template('verify_otp.html')


@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    role = request.form.get('role')
    global stored_email
   
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO Users (Email, Name, Role) VALUES (?, ?, ?)",
                   (email, name, role))
    cnxn.commit()
    if role == 'Student':
        stored_email = email
        return render_template('Student.html', name=name, email=email)
    elif role == 'Trainer':
        stored_email = email
        return render_template('Trainer.html', name=name, email=email)
'''
@app.route('/submit', methods=['POST'])
def submit():
    question = request.form['question']
    shortcode = request.form['shortcode']
    question_type = request.form['question_type']
    correct_answer = None  
    mcq_options1 = None
    mcq_options2 = None
    mcq_options3 = None
    mcq_options4 = None

    # Determine the correct_answer based on the question type
    if question_type == 'yes_no':
        correct_answer = request.form['correct_answer']
    elif question_type == 'mcq':
        mcq_options1 = request.form['mcq_option_1']
        mcq_options2 = request.form['mcq_option_2']
        mcq_options3 = request.form['mcq_option_3']
        mcq_options4 = request.form['mcq_option_4']
        correct_answer = request.form['correct_answer']  
    elif question_type == 'descriptive' or question_type == 'text_answer':
        correct_answer = request.form['correct_answer'] 

    # Establish a database connection
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()

    # Insert the question data into the "Questions" table
    cursor.execute("INSERT INTO Question (question_text, shortcode, question_type, mcq_option_1, mcq_option_2, mcq_option_3, mcq_option_4, correct_answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   question, shortcode, question_type, mcq_options1, mcq_options2, mcq_options3, mcq_options4, correct_answer)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
    # return 'Question inserted into the database.'
    #flash('Question submitted successfully!', 'success')
    return render_template('Trainer.html', question_submitted=True)
'''

@app.route('/submit', methods=['POST'])
def submit():
    question = request.form['question']
    shortcode = request.form['shortcode']
    question_type = request.form['question_type']
    correct_answer = None
    options = None  # Initialize mcq_options as a single string

    # Determine the correct_answer based on the question type
    if question_type == 'yes_no':
        correct_answer = request.form['correct_answer']
    elif question_type == 'mcq':
        # Concatenate mcq_options1, mcq_options2, mcq_options3, and mcq_options4 into a single string
        options = '|'.join([request.form[f'mcq_option_{i}'] for i in range(1, 5)])
        correct_answer = request.form['correct_answer']
    elif question_type == 'descriptive' or question_type == 'text_answer':
        correct_answer = request.form['correct_answer']

    # Establish a database connection
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()

    # Insert the question data into the "Questions" table
    cursor.execute("INSERT INTO Question (question_text, shortcode, question_type, options, correct_answer) VALUES (?, ?, ?, ?, ?)",
                   question, shortcode, question_type, options, correct_answer)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    # return 'Question inserted into the database.'
    #flash('Question submitted successfully!', 'success')
    return render_template('Trainer.html', question_submitted=True)



@app.route('/add-another', methods=['GET'])
def add_another():
    return render_template('Trainer.html')

@app.route('/show-answers', methods=['GET'])
def show_answers():
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()
    cursor.execute('SELECT A.answer_id, A.student_id, A.question_id, A.given_answer,Q.correct_answer FROM Answer A INNER JOIN Question Q ON A.question_id = Q.question_id')
    answers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('answer.html', answers=answers)

@app.route('/ask-question')
def index1():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=dbserver23jandeepak.database.windows.net;DATABASE=dbfeedbackmgt;UID=dbadmin;PWD=Localhost@1234567')
    cursor = conn.cursor()
    
    # Check if global_email is present in the Answer table
    cursor.execute('SELECT 1 FROM Answer WHERE student_id = ?', global_email)
    email_exists = cursor.fetchone()

    if email_exists:
        # If email exists in Answer table, retrieve unanswered questions
        cursor.execute('SELECT  q.* FROM Question q LEFT JOIN Answer a ON q.question_id = a.question_id AND a.student_id = ? WHERE a.student_id IS NULL', global_email)
    else:
        # If email doesn't exist, retrieve all questions
        cursor.execute('SELECT * FROM Question')

    questions = cursor.fetchall()
    cursor.close()
    conn.close()

    questions_list = []

    for row in questions:
        question = {'id': row.question_id, 'text': row.question_text, 'type': row.question_type}
        if row.question_type == 'mcq':
            # Split the mcq_options column by the delimiter (|) to get a list of options
            options = row.options.split('|')
            question['options'] = options
        else:
            question['options'] = []
        questions_list.append(question)

    return jsonify(questions_list)


@app.route('/submit-answers', methods=['POST'])
def submit_answers():
    conn = None
    global stored_email
    try:
        # Establish a database connection
        
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=dbserver23jandeepak.database.windows.net;DATABASE=dbfeedbackmgt;UID=dbadmin;PWD=Localhost@1234567')
        cursor = conn.cursor()

        # Retrieve data from the request
        data = request.get_json()
        email=data.get('email')
        print(email)
        question_id = data.get('questionId')
        user_response = data.get('userResponse')
        
        # Processing the response based on its type
        if user_response in ["false", "true"]:
            user_response = "No" if user_response == "false" else "Yes"
        elif user_response in ["0", "1", "2", "3"]:
            cursor.execute('SELECT options FROM Question WHERE question_id = ?', question_id)
            options_string = cursor.fetchone()[0]  # Fetch the 'options' string
            options_list = options_string.split('|')  # Split the 'options' string into a list
            # Ensure that user_response is within a valid range
            user_response_index = int(user_response)
            if 0 <= user_response_index < len(options_list):
                user_response = options_list[user_response_index]
            else:
                # Handle the case where user_response is out of range or invalid
                user_response = None  # or raise an exception or provide a default value


        # Get the correct answer from the database
        #cursor.execute('SELECT correct_answer FROM Question WHERE question_id = ?', question_id)
        #correct_answer = cursor.fetchone()[0]

        # Insert response into the Answer table with the email as student_id
        cursor.execute("INSERT INTO Answer (student_id, question_id, given_answer) VALUES (?, ?, ?)", 
                       (email, question_id, user_response))
        conn.commit()

        return jsonify({'status': 'success', 'message': 'Response submitted successfully'})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)})
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)







