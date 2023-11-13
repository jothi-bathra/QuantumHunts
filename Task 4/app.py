from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from email.mime.text import MIMEText
import smtplib

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/QH'
mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    mobile = data.get('mobile')
    email = data.get('email')
    password = data.get('password')

    # Backend validation
    if len(name) < 3 or len(mobile) != 10:
        return jsonify({'error': 'Invalid data. Name must be at least 3 characters long, and mobile must be 10 digits.'}), 400

    # Store data in MongoDB
    users_collection = mongo.db.QH
    users_collection.insert_one({'name': name, 'mobile': mobile, 'password': password})

    send_registration_email(name, email)

    return jsonify({'message': 'Registration successful'}), 201

def send_registration_email(name, email):
    subject = 'Registration Confirmation'
    body = f'Thank you, {name}, for registering with our platform.'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'jothibathra22@gmail.com'
    msg['To'] = email

    try:
        # Establish a connection to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to the Gmail account
        server.login('jothibathra22@gmail.com', 'mnzrestaepdbacmz')

        # Send the email
        server.sendmail('jothibathra22@gmail.com', email, msg.as_string())

        # Close the connection
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

    
if __name__ == '__main__':
    app.run(debug=True)
