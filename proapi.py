import google.oauth2.credentials
import google_auth_oauthlib.flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from flask import Flask, request, session, redirect
from googleapiclient.discovery import build
import os
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)
app.secret_key = os.urandom(24)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #ativo apenas para o ambiente de teste.

@app.route('/iniciar')
def inicio():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',
    scopes=['https://www.googleapis.com/auth/youtube',
            'https://www.googleapis.com/auth/youtube.readonly'])

    flow.redirect_uri = 'http://127.0.0.1:5000/id'

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    session['state'] = state
    return redirect(authorization_url)


@app.route('/id')
def id():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/youtube',
                'https://www.googleapis.com/auth/youtube.readonly'],
        state=session.get('state')  # Pegando o estado salvo na sessão
    )
    flow.redirect_uri = 'http://127.0.0.1:5000/id'

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'granted_scopes': credentials.granted_scopes
    }

    return redirect('http://127.0.0.1:5000/pega')

@app.route('/pega')
def pega():
    credentials = Credentials(**session['credentials'])
    youtube = build('youtube', 'v3', credentials=credentials)
    
    recurso  = youtube.subscriptions().list(
            part='id',
            mine=True,
            maxResults=50,
    ).execute()

    item =  recurso['items']
    tam = len(item)

    while tam >= 1:
        resposta = youtube.subscriptions().delete(
            id = recurso['items'][tam-1]['id']
        ).execute()
        tam = tam - 1

    return redirect("http://localhost:3000/final")
app.run()