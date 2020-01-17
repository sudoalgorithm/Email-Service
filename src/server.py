import os
import pymongo
from flask import Flask, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

SENDER: str = ''
client = pymongo.MongoClient(os.environ['MONGO_DB_HOST'], int(os.environ['MONGO_DB_PORT']))
db = client.test

@app.route("/api/v1/sendemail", method=["GET"])
def sendEmail(receiver: str, subject: str, body: str):
    message = Mail(
        from_email=SENDER,
        to_emails=receiver,
        subject=subject,
        html_content=body
    )
    try:
        sg = SendGridAPIClient(os.environ['SEND_GRID_API_KEY'])
        response = sg.send(message)
        return response.status_code
    except Exception as identifier:
        return identifier


@app.route("/api/v1/postmongodb", method=["POST"])
def addToMongoDB(message: str):
    try:
        db.my_collection.insert_one(message).inserted_id
    except Exception as identifier:
        return identifier

@app.route("/api/v1/getmongodb", method=["GET"])
def getFromMongoDB():
    try:
        db.my_collection.find_one()
        for item in db.my_collection.find():
            print(item["x"])
    except Exception as identifier:
        return identifier
