from flask import Flask, request
from twilio.rest import Client
import os
import boto3
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World Flask for notifications!"

@app.route("/sms", methods=['POST'])
def sms():
    hash = request.form['hash_validator']
    hash_validator=os.environ.get("hash_validator")
    if(hash == hash_validator):
        destination = request.form['destination']
        message = request.form['message']
        client = "aws"
        if(client == "aws"):
            # Create an SNS client
            client = boto3.client(
                "sns",
                aws_access_key_id=os.environ.get("aws_access_key_id"),
                aws_secret_access_key=os.environ.get("aws_secret_access_key"),
                region_name="us-east-1"
            )

            # Send your sms message.
            client.publish(
                PhoneNumber=destination,
                Message=message
            )
        else:
            try:
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


if __name__ == '__main__':
    app.run()