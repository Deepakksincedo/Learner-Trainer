from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
import random
from django.urls import reverse
from django.contrib import messages

import pyodbc


# Specify the DSN name
dsn_name = 'your_dsn_name'

# Your global variables
otp_storage = {}
global_email = None
global_otp = None

#connect to the server in microsoft sql

server = 'dbserver23jandeepak.database.windows.net'
database = 'dbfeedbackmgt'
username = 'dbadmin'
password = 'Localhost@1234567'
driver = '{SQL Server}'

# Construct the connection string
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Connect to SQL Server
cnxn = pyodbc.connect(connection_string)



def homePage(request):
    return render(request, "login.html")

def send_otp(request):
    global global_email, global_otp, otp_storage
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = random.randint(100000, 999999)
        otp_storage[email] = otp
        request.session['otp'] = otp
        send_mail("Your OTP", f"Your OTP is: {otp}", 'bbonzana@gmail.com', [email])
        global_email = email
        global_otp = otp
        return redirect(reverse('verify_otp'))  # Redirect to the 'verify_otp' URL
    return render(request, 'myapp/login.html')





# Define the verify_otp function
def verify_otp(request):
    print("Into the OTP verification function")
    global global_email, global_otp  # Access the global variables

    if request.method == 'POST':
        cursor = cnxn.cursor()

        # Use global_email and global_otp instead of request.form.get()
        email = global_email
        otp_str = global_otp
        print(f"received mail is equal to {request.POST.get('emailname')}")
        print(f"received otp is euqal to {request.POST.get('otpname')}")

        print(f"Stored email: {email}")
        print(f"Stored OTP string: {otp_str}")

        if otp_str is not None:
            entered_otp = request.POST.get('otpname')  # Get the entered OTP from the form

            if entered_otp.isdigit():  # Check if entered OTP is a valid integer
                entered_otp = int(entered_otp)

                if entered_otp == int(otp_str):
                    cursor.execute("SELECT Name, Role FROM Users WHERE Email = ?", (email,))
                    row = cursor.fetchone()

                    if row:
                        if row.Role.lower() == 'trainer':
                            return render(request, 'Trainer.html', {'name': row.Name, 'email': email})
                        elif row.Role.lower() == 'student':
                            return render(request, 'Student.html', {'name': row.Name, 'email': email})
                    else:
                        return render(request, 'register.html')
                else:
                    messages.error(request, 'Wrong OTP. Please try again.')
                    return render(request, 'verify_otp.html')  # Render a template for invalid OTP
            else:
                messages.error(request, 'Wrong OTP. Please try again.')
                return render(request, 'verify_otp.html')  # Render a template for invalid OTP
        else:
            messages.error(request, 'Wrong OTP. Please try again.')
            return render(request, 'verify_otp.html')  # Render a template for invalid OTP

    # Handle GET request
    return render(request, 'verify_otp.html')



def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        
        try:
            cursor = cnxn.cursor()
            cursor.execute("INSERT INTO Users (Email, Name, Role) VALUES (?, ?, ?)", (email, name, role))
        except pyodbc.Error as e:
            if 'Violation of UNIQUE KEY constraint' in str(e):
                print(f"Error: Duplicate email found for {email}")
            else:
                print(f"Error: {e}")
        
        if role == 'Student':
            # You may want to pass data to the template using context
            context = {'email': email, 'name': name, 'role': role}
            return render(request, 'Student.html', context)
        elif role == 'Trainer':
            # You may want to pass data to the template using context
            context = {'email': email, 'name': name, 'role': role}
            return render(request, 'Trainer.html', context)
    
    # Handle other cases (e.g., GET request)
    return render(request, 'register.html')  # Render your registration form template

#Trainers page logic handling


#to submit the question to the backend or database
def submit(request):
    if request.method == 'POST':
        question_text = request.POST.get('question')
        shortcode = request.POST.get('shortcode')
        question_type = request.POST.get('question_type')
        correct_answer = None
        options = None  # Initialize options as None

        # Determine the correct_answer based on the question type
        if question_type == 'yes_no':
            correct_answer = request.POST.get('correct_answer')
        elif question_type == 'mcq':
            # Concatenate mcq_option_1, mcq_option_2, mcq_option_3, and mcq_option_4 into a single string
            options = '|'.join([request.POST.get(f'mcq_option_{i}') for i in range(1, 5)])
            correct_answer = request.POST.get('correct_answer')
        elif question_type in ['descriptive', 'text_answer']:
            correct_answer = request.POST.get('correct_answer')

        # Create a new Question instance and save it to the database
        question = Question.objects.create(
            question_text=question_text,
            shortcode=shortcode,
            question_type=question_type,
            options=options,
            correct_answer=correct_answer
        )

        # Redirect to a success page or render a success template
        return render(request, 'Trainer.html', {'question_submitted': True})

   

#If trainer add another page it will load the same page again
def add_another(request):
    messages.success(request,'Successfully added the question')
    return render(request,'Trainer.html')

#To show the answers the student have given
def show_answers(request):
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()
    cursor.execute('SELECT A.answer_id, A.student_id, A.question_id, A.given_answer,Q.correct_answer FROM Answer A INNER JOIN Question Q ON A.question_id = Q.question_id')
    answers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request,'answer.html', answers=answers)

    