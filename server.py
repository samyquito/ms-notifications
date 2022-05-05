from flask import Flask, request
from twilio.rest import Client
import os
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World Flask"

@app.route("/sms", methods=['POST'])

def sms():
    destination = request.form['destination']
    message = request.form['message']
    print(destination)
    account_sid = os.environ.get["account_sid"]
    print(account_sid)
    auth_token = os.environ.get["auth_token"] 
    client = Client(account_sid, auth_token) 
    
    message = client.messages.create(  
                                messaging_service_sid=os.environ.get["messaging_service_sid"], 
                                body='message',      
                                to='destination' 
                            ) 
    
    print(message.sid)

    return "sending sms message!"

if __name__ == '__main__':
    app.run()