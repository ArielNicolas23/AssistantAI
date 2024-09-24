from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from project.models import Integration
from project.integrations.forms import IntegrationForm
from project import db, TOKEN
import json
import hmac
import hashlib
import requests
import os


webhook_bp = Blueprint('webhooks', __name__)


@webhook_bp.route('/webhook', methods=['GET', 'POST'])
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
                    #verifica si el evento se ejecuto por el mismo sistema
                    if senderPsid == '432389276616406' or senderPsid == '423507407513443':
                        return 'EVENT_RECEIVED', 200
                    #inicia proceso de respuesta
                    handleMessage(senderPsid, webhookEvent['message'], entry['id'], body['object'])
                return 'EVENT_RECEIVED', 200
        elif 'object' in body and body['object'] == 'instagram':
            entries = body['entry']
            for entry in entries:
                print(entries)
                webhookEvent = entry['messaging'][0]
                senderPsid = webhookEvent['sender']['id']
                if 'message' in webhookEvent:
                    #verifica si el evento se ejecuto por el mismo sistema
                    if senderPsid == '17841409065001655':
                        return 'EVENT_RECEIVED', 200
                    #inicia proceso de respuesta
                    handleMessage(senderPsid, webhookEvent['message'], entry['id'], body['object'])
                return 'EVENT_RECEIVED', 200
            return 'ERROR', 404

@webhook_bp.route('/igwebhook', methods=['GET', 'POST'])
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
        if signature != expected_signature:
            #error en la firma
            print("Signature hash does not match")
        body = json.loads(payload.decode('utf-8'))
        if 'object' in body and body['object'] == 'instagram':
            entries = body['entry']
            for entry in entries:
                print(entries)
                webhookEvent = entry['messaging'][0]
                senderPsid = webhookEvent['sender']['id']
                if 'message' in webhookEvent:
                    #verifica si el evento se ejecuto por el mismo sistema
                    if senderPsid == '17841409065001655':
                        return 'EVENT_RECEIVED', 200
                    #inicia proceso de respuesta
                    handleMessage(senderPsid, webhookEvent['message'], entry['id'], body['object'])
                return 'EVENT_RECEIVED', 200
        else:
            return 'ERROR', 404
