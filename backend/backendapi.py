from flask import Flask, request, session
from flask_cors import CORS

from sql import create_connection
from sql import execute_read_query
from sql import execute_update_query

from creds import creds

import secrets

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import os

from fpdf import FPDF
import os

load_dotenv()

# Create the variables that store the gmail address and gmail address password from which form data is sent from.
sender_gmail = os.getenv('sender_gmail')
email_password = os.getenv('email_password')

app = Flask(__name__)
app.config["DEBUG"] = True

app.config['SECRET_KEY'] = secrets.token_hex(16)

CORS(app, origins="http://localhost:8080")

# Function to check whether a client's email is already in the database.
def check_if_client_exists(email):
    sql = f"select * from client where email = '{email}'"
    result = execute_read_query(create_connection(creds.myhostname, creds.uname, creds.passwd, creds.dbname), sql)
    return len(result) > 0

# Function to insert a client's information into the database.
def insert_new_client(first_name, last_name, email):
    sql = f"insert into client (first_name, last_name, email) values ('{first_name}', '{last_name}', '{email}')"
    execute_update_query(create_connection(creds.myhostname, creds.uname, creds.passwd, creds.dbname), sql)

# Function to retrieve a client's data from the database using their email.
def find_client(email):
    sql = f"select client_id from client where email = '{email}'"
    result = execute_read_query(create_connection(creds.myhostname, creds.uname, creds.passwd, creds.dbname), sql)
    return result

# Function to insert contact form information into the database.
def insert_contact_info(client_id, subject, message):
    sql = f"insert into contact (client_id, subject, message) values ({client_id}, '{subject}', '{message}')"
    execute_update_query(create_connection(creds.myhostname, creds.uname, creds.passwd, creds.dbname), sql)

# Function to retrieve the most recent contact form information from the database.
def find_contact():
    sql = f"select * from contact where contact_id = (select max(contact_id) from contact)"
    result = execute_read_query(create_connection(creds.myhostname, creds.uname, creds.passwd, creds.dbname), sql)
    return result

# Function to retrieve client information from the database using their client_id.
def find_client_by_id(id):
    sql = f"select * from client where client_id = {id}"
    result = execute_read_query(create_connection(creds.myhostname, creds.uname, creds.passwd, creds.dbname), sql)
    return result

# Function to send an email using a hardcoded email (dotenv variables) along with client and contact form information retrieved from the database.
def send_email(to_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_gmail
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_gmail, email_password) 
        text = msg.as_string()
        server.sendmail(sender_gmail, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Function to insert form inquiry information into the database.
def insert_inquiry_info(client_id, destination, departure, start_date, end_date, is_passport_valid, num_travelers, underage_travelers, num_underage_travelers, accommodations, rooms, payment_date, atmosphere, budget, activities, reference):
    sql = f"insert into travel_inquiries (client_id, destination, departure, start_date, end_date, is_passport_valid, num_travelers, underage_travelers, num_underage_travelers, accommodations, rooms, payment_date, atmosphere, budget, activities, referenced_by) values ({client_id}, '{destination}', '{departure}', '{start_date}', '{end_date}', '{is_passport_valid}', '{num_travelers}', '{underage_travelers}', '{num_underage_travelers}','{accommodations}', '{rooms}', '{payment_date}', '{atmosphere}', '{budget}', '{activities}', '{reference}')"
    execute_update_query(create_connection(creds.myhostname, creds.uname, creds.passwd, creds.dbname), sql)

# Function to generate inquiry form pdf using data from the database
def generate_inquiry_pdf(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add Title
    pdf.set_font('Times', 'B', 20)
    pdf.cell(200, 10, f"Travel Inquiry Form - {data['first_name']} {data['last_name']}", ln=True, align='C')
    
    # Add Watermark
    pdf.image('../public/img/watermark.png', x=5, y=35, w=200)

    # Add Client Information
    pdf.ln(10)  # Line break
    pdf.set_font('Times', '', 16)
    pdf.cell(200, 10, f"Client: {data['first_name']} {data['last_name']}", ln=True)
    pdf.cell(200, 10, f"Email: {data['email']}", ln=True)
    
    # Add Form Details
    pdf.ln(10)  # Line break
    pdf.cell(200, 10, f"Destination: {data['destination']}", ln=True)
    pdf.cell(200, 10, f"Departure City: {data['departure']}", ln=True)
    pdf.cell(200, 10, f"Start Date: {data['start_date']}", ln=True)
    pdf.cell(200, 10, f"End Date: {data['end_date']}", ln=True)
    pdf.cell(200, 10, f"Valid Passport: {data['is_passport_valid']}", ln=True)
    pdf.cell(200, 10, f"Number of Travelers: {data['num_travelers']}", ln=True)
    pdf.cell(200, 10, f"Underage Travelers: {data['underage_travelers']}", ln=True)
    pdf.cell(200, 10, f"Number of Underage Travelers: {data['num_underage_travelers']}", ln=True)
    pdf.cell(200, 10, f"Accommodations: {data['accommodations']}", ln=True)
    pdf.cell(200, 10, f"Rooms: {data['rooms']}", ln=True)
    pdf.cell(200, 10, f"Able to make Payment on: {data['payment_date']}", ln=True)
    pdf.cell(200, 10, f"Atmosphere: {data['atmosphere']}", ln=True)
    pdf.cell(200, 10, f"Budget: {data['budget']}", ln=True)
    pdf.cell(200, 10, f"Activities: {data['activities']}", ln=True)
    pdf.cell(200, 10, f"How did you hear about us? {data['reference']}", ln=True)

    return pdf

# Select most recent entry from the travel_inquiries table in the database
def find_inquiry():
    sql = f"select * from travel_inquiries where form_id = (select max(form_id) from travel_inquiries)"
    result = execute_read_query(create_connection(creds.myhostname, creds.uname, creds.passwd, creds.dbname), sql)
    return result

# Funtion to send an email that includes pdf with the travel inquiry details
def send_email_with_inquiry_pdf(to_email, subject, message, pdf, pdf_data):
    msg = MIMEMultipart()
    msg['From'] = sender_gmail
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    # Save PDF
    output_directory = os.path.join(os.getcwd(), "generated_pdfs")
    os.makedirs(output_directory, exist_ok=True)  # Create directory if it doesn't exist
    pdf_file_path = os.path.join(output_directory, f"travel_inquiry_{pdf_data['first_name']}_{pdf_data['last_name']}.pdf")
    pdf.output(pdf_file_path)

    # Attach PDF
    with open(pdf_file_path, 'rb') as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(pdf_file_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_file_path)}"'
        msg.attach(part)

    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_gmail, email_password) 
        text = msg.as_string()
        server.sendmail(sender_gmail, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to generate contact pdf with data from the database
def generate_contact_pdf(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font('Times', 'B', 20)
    pdf.cell(200, 10, f"Contact Form - {data['first_name']} {data['last_name']}", ln=True, align='C')

    # Add Watermark
    pdf.image('../public/img/watermark.png', x=5, y=35, w=200)

    # Client information
    pdf.ln(10)  # Line break
    pdf.set_font('Times', '', 16)
    pdf.cell(200, 10, f"Client: {data['first_name']} {data['last_name']}", ln=True)
    pdf.cell(200, 10, f"Email: {data['email']}", ln=True)
    
    # Form details
    pdf.ln(10)  # Line break
    pdf.cell(200, 10, f"Subject: {data['subject']}", ln=True)
    pdf.cell(200, 10, f"Message: {data['message']}", ln=True)

    return pdf

# Funtion to send an email that includes pdf with contact message
def send_email_with_contact_pdf(to_email, subject, message, pdf, pdf_data):
    msg = MIMEMultipart()
    msg['From'] = sender_gmail
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    # Save PDF
    output_directory = os.path.join(os.getcwd(), "generated_pdfs")
    os.makedirs(output_directory, exist_ok=True)  # Create directory if it doesn't exist
    pdf_file_path = os.path.join(output_directory, f"contact_{pdf_data['first_name']}_{pdf_data['last_name']}.pdf")
    pdf.output(pdf_file_path)

    # Attach PDF
    with open(pdf_file_path, 'rb') as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(pdf_file_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_file_path)}"'
        msg.attach(part)

    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_gmail, email_password) 
        text = msg.as_string()
        server.sendmail(sender_gmail, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Create a backend path which recieves a post request when the callback page is accessed.
@app.route('/callback', methods=['POST'])

def register_client():
    data = request.get_json()
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    global store_email
    store_email = email

    session['email_store'] = email

    if not check_if_client_exists(email):
        insert_new_client(first_name, last_name, email)
    return "Client added unless already exists"

# Create a backend path which recieves a post request when the travel inquiry form page is accessed.
@app.route('/travelinquiryformsubmit', methods=['POST'])
def submit_travel_inquiry_form():
    data = request.get_json() # Retrieve JSON data

    # Extract specific values from JSON data
    email = data.get('email')
    destination = data.get('destination')
    departure = data.get('departure')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    is_passport_valid = data.get('is_passport_valid')
    num_travelers = data.get('num_travelers')
    underage_travelers = data.get('underage_travelers')
    num_underage_travelers = data.get('num_underage_travelers')
    accommodations = data.get('accommodations')
    rooms = data.get('rooms')
    payment_date = data.get('payment_date')
    atmosphere = data.get('atmosphere')
    budget = data.get('budget')
    activities = data.get('activities')
    referenced_by = data.get('reference')

    # Find the client ID in the database via email
    client = find_client(email) 
    client_id = client[0]['client_id']

    # Retrieve specific client information from the database
    client_data = find_client_by_id(client[0]['client_id']) 
    first_name = client_data[0]['first_name']
    last_name = client_data[0]['last_name']
    email = client_data[0]['email']

    # Insert form data into the database
    insert_inquiry_info(client_id, destination, departure, start_date, end_date, is_passport_valid, num_travelers, underage_travelers, num_underage_travelers, accommodations, rooms, payment_date, atmosphere, budget, activities, referenced_by)

    form_data = find_inquiry() # Retrieve most recent travel inquiry from the database
    print(form_data)
    # Extract specific inquiry details from the retrieved form data
    destination = form_data[0]['destination']
    departure = form_data[0]['departure']
    start_date = form_data[0]['start_date']
    end_date = form_data[0]['end_date']
    is_passport_valid = form_data[0]['is_passport_valid']
    num_travelers = form_data[0]['num_travelers']
    underage_travelers = form_data[0]['underage_travelers']
    num_underage_travelers = form_data[0]['num_underage_travelers']
    accommodations = form_data[0]['accommodations']
    rooms = form_data[0]['rooms']
    payment_date = form_data[0]['payment_date']
    atmosphere = form_data[0]['atmosphere']
    budget = form_data[0]['budget']
    activities = form_data[0]['activities']
    referenced_by = form_data[0]['referenced_by'] 
    
    # Prepare the data for the pdf generation
    pdf_data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'destination': destination,
        'departure': departure,
        'start_date': start_date.strftime('%m-%d-%Y'), # Format dates as MM-DD-YYYY
        'end_date': end_date.strftime('%m-%d-%Y'),
        'is_passport_valid': is_passport_valid,
        'num_travelers': num_travelers,
        'underage_travelers': underage_travelers,
        'num_underage_travelers': num_underage_travelers,
        'accommodations': accommodations,
        'rooms': rooms,
        'payment_date': payment_date.strftime('%m-%d-%Y'),
        'atmosphere': atmosphere,
        'budget': budget,
        'activities': activities,
        'reference': referenced_by
    }

    # Generate pdf using the prepared data
    pdf_file = generate_inquiry_pdf(pdf_data)

    # Send email with attached pdf
    send_email_with_inquiry_pdf(sender_gmail, f"New Travel Inquiry Form Submission from {first_name} {last_name}", "Please find the travel inquiry form attached.", pdf_file, pdf_data)

    return "Travel Inquiry Form added to db and sent to email"
    
    

# Create a backend path which recieves a post request when a contact form is submitted.
@app.route('/contact', methods=['POST'])
def contact_form():
    data = request.get_json()

    email = data['email']
    subject = data['subject']
    message = data['message']

    client = find_client(email)
    client_id = client[0]['client_id']

    insert_contact_info(client_id, subject, message)

    contact_data = find_contact()
    client_data = find_client_by_id(contact_data[0]['client_id'])
    subject = contact_data[0]['subject']
    first_name = client_data[0]['first_name']
    last_name = client_data[0]['last_name']
    email = client_data[0]['email']
    message = contact_data[0]['message']

    pdf_data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'subject': subject,
        'message': message
    }

    pdf_file = generate_contact_pdf(pdf_data)

    send_email_with_contact_pdf(sender_gmail, f"New Contact Form Submission from {first_name} {last_name}", "Please find the contact form attached.", pdf_file, pdf_data)

    return "Contact form info added to database and sent to email"

app.run()