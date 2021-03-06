from flask import Flask, request
from twilio.rest import Client
import os
import boto3
from dotenv import load_dotenv
load_dotenv()

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World Flask for notifications!"

@app.route("/email", methods=['POST'])
def email():
    hash = request.form['hash_validator']
    hash_validator=os.environ.get("hash_validator")
    if(hash == hash_validator):
        to = request.form['destination']
        subject = request.form['subject']
        message = request.form['message']
        SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
        message = Mail(
            from_email=os.environ.get("SENDGRID_EMAIL_FROM"),
            to_emails=to,
            subject=subject,
            html_content=message)
        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
    else:
        return "hash_error"  



@app.route("/sms", methods=['POST'])
def sms():
    hash = request.form['hash_validator']
    hash_validator=os.environ.get("hash_validator")
    if(hash == hash_validator):
        destination = request.form['destination']
        message = request.form['message']
        try:
        # Create an SNS client
            account_sid = os.environ.get("account_sid")
            auth_token = os.environ.get("auth_token")
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                messaging_service_sid=os.environ.get("messaging_service_sid"),
                body=message,
                to=destination
            )
            print(message.sid)
            return "OK", 200
        except:
             return "KO", 500
    else:
        return "hash_error", 401



@app.route("/wpp", methods=['POST'])
def wpp():
    hash = request.form['hash_validator']
    hash_validator=os.environ.get("hash_validator")
    if(hash == hash_validator):
        destination = request.form['destination']
        message = request.form['message']
        try:
            whatsapp_from = os.environ.get("whatsapp_from")
            account_sid = os.environ.get("account_sid")
            auth_token = os.environ.get("auth_token")
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                from_=whatsapp_from,
                body=message,
                to='whatsapp:'+ destination
            )
            print(message.sid)
            return "OK", 200
        except:
            return "KO", 500
    else:
        return "hash_error", 401


if __name__ == '__main__':
    app.run()