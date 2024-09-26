from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from project.models import Integration
from project.integrations.forms import IntegrationForm,IntegrationUpdateForm
from project import db, TOKEN, IGTOKEN, IGCLIENTID, METACLIENTID, IGSECRET, METASECRET, ACCESS_TOKEN
import json
import hmac
import hashlib
import requests

integration_bp = Blueprint('integration', __name__)

@integration_bp.route('/integration/new', methods=['GET', 'POST'])
@login_required
def new_integration():
    form = IntegrationForm()
    if form.validate_on_submit():
        integration = Integration(
            OwnerID=current_user.id,
            Type=form.Type.data,
            # MetaUserToken = form.MetaUserToken.data,
            # MetaUserID = form.MetaUserID.data,
            # MetaPageID = form.MetaPageID.data,
            # MetaPageName = form.MetaPageName.data,
            # AssistantID = form.AssistantID.data,
            IsTest = form.IsTest.data,
        )
        db.session.add(integration)
        db.session.commit()
        flash('Integration created successfully!', 'success')
        return redirect(url_for('integration.list_integrations'))
    return render_template('new_integration.html', form=form)

@integration_bp.route('/integration/update/<integration_id>', methods=['GET', 'POST'])
@login_required
def update_integration(integration_id):
    integration = Integration.query.get_or_404(integration_id)
    form = IntegrationUpdateForm(obj=integration)
    if form.validate_on_submit():
        integration.Type=form.Type.data
        integration.MetaUserToken = form.MetaUserToken.data
        integration.MetaUserID = form.MetaUserID.data
        integration.MetaPageID = form.MetaPageID.data
        integration.MetaPageName = form.MetaPageName.data
        integration.AssistantID = form.AssistantID.data
        integration.IsTest = form.IsTest.data
        db.session.commit()
        flash('Integration updated successfully!', 'success')
        return redirect(url_for('integration.list_integrations'))
    return render_template('update_integration.html', form=form, integration=integration)

@integration_bp.route('/integrations')
@login_required
def list_integrations():
    integrations = Integration.query.all()
    return render_template('list_integrations.html', integrations=integrations)

@integration_bp.route("/integration/generatetoken/", methods=['GET'])
def registrarIntegracion():
    args = request.args
    platform = args['state']
    token = generarToken(args['code'], platform)
    
    return args

#Recibe codigo y genera token de acceso
def generarToken(code, platform):
    if platform == 'instagram':
        params = {
        'client_id': IGCLIENTID,
        'client_secret': IGSECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': 'https://kidicai.pythonanywhere.com/',
        'code': code
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = 'https://api.instagram.com/oauth/access_token'
    elif platform == 'messenger':
        params = {
            'client_id': METACLIENTID,
            'redirect_uri':'https://kidicai.pythonanywhere.com/LoginTest/',
            'client_secret': METASECRET,
            'code':code
            }
        headers = {}
        url = 'https://graph.facebook.com/oauth/access_token?'
    r = requests.post(url, data=params, headers=headers)
    print(r)
    rJson=r.json()
    if 'error' in rJson:
        return rJson
    return (rJson['access_token'])

#Debuggear Token
def debugToken(token, accesscode, platform):
    if platform == 'Instagram':
        params = {
        'input_token': token,
        'access_token':accesscode,
        }
        url = 'graph.facebook.com/debug_token?'
    elif platform == 'Facebook':
        params = {
        'fields': 'user_id,username',
        'access_token':accesscode,
        }
        url = 'https://graph.instagram.com/v20.0/me?'
    r = requests.post(url, data=params)
    print(r)
    rJson=r.json()
    if 'error' in rJson:
        return rJson
    return rJson

#Obtiene listado de paginas y sus tokens si es que tiene acceso
def getPages(token, user_id):
    params2={
        'access_token':token
            }
    url = 'https://graph.facebook.com/'+user_id+'/accounts?'
    r = requests.get(url, params=params2)
    rJson=r.json()
    if 'error' in rJson:
        return rJson
    return rJson

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

#registra el servicio de mensajeria
def addMessageAccess(token, pageid, platform):
    print(token)
    if platform =='instagram':
        params = {
            'subscribed_fields':'messages',
            'access_token':token,
        }
        url = 'https://graph.facebook.com/'+pageid+'/subscribed_apps?'
    elif platform == 'messenger':
        params = {
            'subscribed_fields':'messages',
            'access_token':token,
        }
        url = 'https://graph.instagram.com/v20.0/'+pageid+'/subscribed_apps?'
    r = requests.post(url, params=params)
    rJson=r.json()
    if 'error' in rJson:
        return rJson
    return rJson
