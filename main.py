# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 02:02:22 2017

@author: HARSHIT
"""

import os, sys
from flask import Flask, request
from utils import wit_response, convo
from pymessenger import Bot
from core import predict

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAbciZAO2HjsBAPKpHW3VZApW7ZANOPfipiXwYnOVTkI1oxZAQYWrFQiJzJo7StubeInHR2gaCP5MODxBaXTS3FxX2O2jfMbXPtilrqd7zjxIx2rqzTY8c41sk0KxYZAaeHWjO8oXsoX4wNQKvc23yiZBgR2qnEYDXOihvWNhkHwZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
    #Webhook Verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"],200
    return "Hello World",200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object']=='page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                
                # Sender and Recipient IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                #If message is a text or not
                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'
                    
                #ECHO
                #response = messaging_text
                response = None
                entity, value = wit_response(messaging_text)
                print(entity, value)

                if entity == 'greetings':
                    response = "Hi, Welcome to Knowmad! We will do a small survey to predict how work related stress could be affecting your mental health. Shall we begin?"
                elif entity == 'yes_no':
                    if value == 'yes':
                        convo()
                    else:
                        response = "Okay maybe next time."

    bot.send_text_message(sender_id, response)

    return "ok", 200
   
def log(message):
    print(message)
    sys.stdout.flush()    


if __name__ == "__main__":
    app.run(debug = True, port = 80)
