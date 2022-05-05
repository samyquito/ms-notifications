from flask import Flask, request
from twilio.rest import Client
import os
import boto3
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World Flask"

@app.route("/sms", methods=['POST'])
def sms():
    hash = request.form['hash_validator']
    if(hash == "Admin12345@2022Ucaldas"):
        destination = request.form['destination']
        message = request.form['message']
        client = "aws"
        if(client == "aws"):
            # Create an SNS client
            client = boto3.client(
                "sns",
                aws_access_key_id=os.environ["aws_access_key_id"],
                aws_secret_access_key=os.environ["aws_secret_access_key"],
                region_name="us-east-1"
            )

            # Send your sms message.
            client.publish(
                PhoneNumber=destination,
                Message=message
            )
        else:
            try:
                account_sid = os.environ["account_sid"]
                auth_token = os.environ["auth_token"]
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    messaging_service_sid=os.environ["messaging_service_sid"],
                    body=message,
                    to=destination
                )
                print(message.sid)
                return "OK"
            except:
                return "KO"
    else:
        return "hash_error"

if __name__ == '__main__':
    app.run()