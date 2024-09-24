"""
Copyright (c) Meta Platforms, Inc. and affiliates.
All rights reserved.

This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from flask import  Blueprint,render_template, redirect, url_for, flash
from flask import Flask, request
import json
import hmac
import hashlib
import requests
import os
from openai import OpenAI

integration = Blueprint('integration', __name__)

TOKEN = "9f55bd11b125a464babf8cba2b99ff87"
PAGE_ACCESS_TOKEN = "EAAFl9QG1mt0BO4r4dBFYE1bxYobZAZCjvj1pzFL4UdCqT0rQrZCyGi6pzW69bo30F4BKWPg3tmmlVZAIZBOR3wjUjvYO39KTLvoE5CcfIUZB1ZBukStNZCWcrBAQTcc3kdeIjMNTn0wo6tQftmg6oqmGTiJLHjhn9Uk9fa0Q6noZCjKlpGkyz2NZBSeOgriEAbklHNTQZDZD"
clientid="393577946782429"

# Simulación de usuarios para autenticación
users = {"admin": "password123"}
pages = {'432389276616406':'EAAFl9QG1mt0BO4r4dBFYE1bxYobZAZCjvj1pzFL4UdCqT0rQrZCyGi6pzW69bo30F4BKWPg3tmmlVZAIZBOR3wjUjvYO39KTLvoE5CcfIUZB1ZBukStNZCWcrBAQTcc3kdeIjMNTn0wo6tQftmg6oqmGTiJLHjhn9Uk9fa0Q6noZCjKlpGkyz2NZBSeOgriEAbklHNTQZDZD',
'423507407513443':'EAAFl9QG1mt0BO7I40ZBg32skjKOFXotchA3wTfSiTcL0PYRAdrZBWNKH2lORvoTZBwXrGGpZBZBZAGiMrVwuic7QPN3kCgujNk5Oa4ZCHXc7DGTIHsmIazyYKwuXh3gLk15FFeznGkZCUjhdoPqQvGZBu7NAu29cuSOMVapuGRwSg2v7eOOT1aUrWKPwm91eRYhUllhB8yqBi',
'17841409065001655':'IGQWRPTjE3cHI4NkFESmdiZA1M0ZADhqRnhuaUNTNnhvWktER1o0UHJjQThfbXdKSGRqUkdzLTk4UmU1dmtCZAjdMeDlIdXdEbDZAGTXMydFZAnNnBScW9oMDhxYnBsUWg2X3dvZAXRGRkZAJOW5lZAwZDZD'}

# declarar llave de api
os.environ["OPENAI_API_KEY"] = "sk-AbKerk7FXFwBBBjHa-SzCxkOrFkvZr27xX5dqZCVRQT3BlbkFJBU4AyS5z0KFOYPXqkNwI1hvqqcFXMr67GWUIT_e7kA"
client = OpenAI()

@integration.route('/', methods=['GET'])
def search():
    args = request.args
    return args

#Function to get access IG Token
@integration.route("/p/<string:slug>/", methods=['GET'])
def callSendAPI(slug):
    payload = {
    'client_id': '443897407962766',
    'client_secret': '150c1f837d665954a955966e53137060',
    'grant_type': 'authorization_code',
    'redirect_uri': 'https://kidicai.pythonanywhere.com/',
    'code': slug
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    url = 'https://api.instagram.com/oauth/access_token'
    r = requests.post(url, data=payload, headers=headers)
    print(r)
    print(r.json())
    return r.json()

@integration.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # Webhook verification
    if request.method == 'GET':
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == TOKEN:
                return "Verification token mismatch", 403
            print("WEBHOOK_VERIFIED")
            return request.args["hub.challenge"], 200
    elif request.method == 'POST':
        # Validate payload
        signature = request.headers["X-Hub-Signature-256"].split('=')[1]
        payload = request.get_data()
        expected_signature = hmac.new(TOKEN.encode('utf-8'), payload, hashlib.sha256).hexdigest()
        if signature != expected_signature:
            print("Signature hash does not match")
            return 'INVALID SIGNATURE HASH', 403

        body = json.loads(payload.decode('utf-8'))
        if 'object' in body and body['object'] == 'page':
            entries = body['entry']
            for entry in entries:
                print(entries)
                webhookEvent = entry['messaging'][0]
                senderPsid = webhookEvent['sender']['id']
                if 'message' in webhookEvent:
                    if senderPsid == '432389276616406' or senderPsid == '423507407513443':
                        return 'EVENT_RECEIVED', 200
                    print(entry['id'])
                    handleMessage(senderPsid, webhookEvent['message'], entry['id'], body['object'])
                return 'EVENT_RECEIVED', 200
        else:
            return 'ERROR', 404

@integration.route('/igwebhook', methods=['GET', 'POST'])
def igwebhook():
    # Webhook verification
    if request.method == 'GET':
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == TOKEN:
                return "Verification token mismatch", 403
            print("WEBHOOK_VERIFIED")
            return request.args["hub.challenge"], 200
    elif request.method == 'POST':
        # Validate payload
        signature = request.headers["X-Hub-Signature-256"].split('=')[1]
        payload = request.get_data()
        expected_signature = hmac.new(TOKEN.encode('utf-8'), payload, hashlib.sha256).hexdigest()
        print(signature)
        print('-----------')
        print(expected_signature)
        if signature != expected_signature:
            #error en la firma
            print("Signature hash does not match")

        body = json.loads(payload.decode('utf-8'))
        print(body)
        if 'object' in body and body['object'] == 'instagram':
            entries = body['entry']
            for entry in entries:
                print(entries)
                webhookEvent = entry['messaging'][0]
                senderPsid = webhookEvent['sender']['id']
                if 'message' in webhookEvent:
                    if senderPsid == '17841409065001655':
                        return 'EVENT_RECEIVED', 200
                    print(entry['id'])
                    handleMessage(senderPsid, webhookEvent['message'], entry['id'], body['object'])
                return 'EVENT_RECEIVED', 200
        else:
            return 'ERROR', 404


#Function to access the Sender API
def callSendAPI(senderPsid, response, page_id, type):
    payload = {
    'recipient': {'id': senderPsid},
    'message': {"text":str(response)},
    'messaging_type': 'RESPONSE'
    }
    page_token = pages[page_id]
    headers = {'content-type': 'application/json'}
    if type == 'page':
        url = 'https://graph.facebook.com/v10.0/'+page_id+'/messages?access_token={}'.format(page_token)
    elif type == 'instagram':
        url = 'https://graph.instagram.com/v10.0/'+page_id+'/messages?access_token={}'.format(page_token)
    r = requests.post(url, json=payload, headers=headers)
    print(r)

#Function for handling a message from MESSENGER
def handleMessage(senderPsid, receivedMessage, page_id, type):
    #check if received message contains text
    if 'text' in receivedMessage:
        response = generateResponse(receivedMessage['text'])
        callSendAPI(senderPsid, response, page_id, type)
    else:
        response = {"text": 'This chatbot only accepts text messages'}
        callSendAPI(senderPsid, response)
#Genera respuesta de Bot
def generateResponse(receivedMessage):
    #Estructura general de conversacion
    completion = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "Eres Alanna, un asistente."},
            {"role": "user", "content": receivedMessage}
        ]
    )
    return completion.choices[0].message.content

#inicio de sesion a traves de facebook
@integration.route("/LoginTest/", methods=['GET'])
def retrieveToken():
    args = request.args
    code = args['code']
    params = {
        'client_id':clientid,
        'redirect_uri':'https://kidicai.pythonanywhere.com/LoginTest/',
        'client_secret': TOKEN,
        'code':code
    }
    url = 'https://graph.facebook.com/oauth/access_token?'
    r = requests.post(url, params=params)
    rJson=r.json()
    if 'error' in rJson:
        return rJson
    return redirect(url_for('integration.getUserToken', token=rJson['access_token']))
#obtiene el usuario
@integration.route("/getUserToken/", methods=['GET'])
def getUserToken():
    args = request.args
    token = args['token']
    params = {
        'input_token':token,
        'access_token': '393577946782429|Wb9-Tg4nJdKGNJotqoXOxxJPrKQ'
    }
    url = 'https://graph.facebook.com/debug_token'
    r = requests.get(url, params=params)
    rJson=r.json()
    if 'error' in rJson:
        return rJson
    params2={
        'access_token':token
            }
    url2 = 'https://graph.facebook.com/'+rJson['data']['user_id']+'/accounts?'
    r = requests.get(url2, params=params2)
    rJson=r.json()
    if 'error' in rJson:
        return rJson
    page_access_token=rJson['data'][0]['access_token']
    pageid = rJson['data'][0]['id']
    nombre=rJson['data'][0]['name']
    rJson = addMessageAccess(page_access_token,pageid)
    if 'success' in rJson:
        return render_template('welcome.html', username=nombre)
    return render_template('welcome.html', username='Error')

#registra el servicio de mensajeria
def addMessageAccess(page_access_token, pageid):
    print(page_access_token)
    params = {
        'subscribed_fields':'messages',
        'access_token':page_access_token,
    }
    url = 'https://graph.facebook.com/'+pageid+'/subscribed_apps?'
    r = requests.post(url, params=params)
    rJson=r.json()
    if 'error' in rJson:
        return rJson
    return rJson
