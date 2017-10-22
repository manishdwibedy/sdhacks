'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

from flask import Flask, render_template, request
import json
import requests
from config import Config
from esign import sign
from random import randint 
from twilio.rest import Client


# Elastic Beanstalk initalization
app = Flask(__name__)
app.debug=True

# change this to your own value
@app.route("/")
def result():
    return render_template('index.html'); 

@app.route("/sign")
def signup():
    return render_template('signup.html');


@app.route('/code')
def code():
    user_code = request.args.get('code')
    Config.code = str(user_code)
    return 'Got the code = ' + user_code

@app.route('/access_token')
def access_token():
    url = 'https://genomelink.io/oauth/token'

    '''
    curl -X POST -d "client_id=PftOLTI13hNYN9gl2UOJKzcNTalDBSbPv8ceTevm&client_secret=gZj2dfZLoQ9my9Ycss21TQXBnRZSizj3EfOtILu2V4wSBmofvlGejc6I22j4lbMwfkREbivpHG4qU4y6wt2N3Dh1LpozHGhrV3g4ElZYH23xWeWf2LG9OgpAA2t94nqi&grant_type=authorization_code&code=zbnHZECvb88GJaWfJ5j6F5b9kUEzuo&redirect_uri=http://127.0.0.1:5000/code" https://genomelink.io/oauth/token

    '''

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-DocuSign-Authentication': '{ "Username":"8df3037b-aa57-4e00-9c87-58479196d233","Password":"liferocks",   "IntegratorKey":"cdd05311-7fe2-40fe-b71b-9c7da37a8bad"}'
    }

    # grant_type = password & client_id = {IntegratorKey} & username = {email} & password = {password} & scope = api
    payload = {
        'client_id': 'cdd05311-7fe2-40fe-b71b-9c7da37a8bad',
        'grant_type': 'password',
        'username': 'manish.dwibedy@gmail.com',
        'password': 'liferocks',
        'scope': 'api',

    }

    print payload
    r = requests.post(url, headers = headers, data= payload)

    return r.text


@app.route('/eye-color')
def eye_color():
    url = 'https://genomelink.io/v1/reports/eye-color?population=european'

    '''
    curl -X POST -d "client_id=PftOLTI13hNYN9gl2UOJKzcNTalDBSbPv8ceTevm&client_secret=gZj2dfZLoQ9my9Ycss21TQXBnRZSizj3EfOtILu2V4wSBmofvlGejc6I22j4lbMwfkREbivpHG4qU4y6wt2N3Dh1LpozHGhrV3g4ElZYH23xWeWf2LG9OgpAA2t94nqi&grant_type=authorization_code&code=zbnHZECvb88GJaWfJ5j6F5b9kUEzuo&redirect_uri=http://127.0.0.1:5000/code" https://genomelink.io/oauth/token

    '''

    headers = {
        'Authorization': 'Bearer D0YTHy2JTVM1an0MNLAqgYmDJXYL8f',
    }

    r = requests.get(url, headers = headers)
    output = json.loads(r.text)
    return output['summary']['text']

@app.route('/sign-doc')
def signDoc():
    # return 'Hello World!'
    # curl - i - k - X
    # POST - d @ payload.json \
    # - H
    # "Accept: application/json" \
    # - H
    # "Content-Type: application/json" \
    # - H
    # 'X-DocuSign-Authentication: { "Username":"8df3037b-aa57-4e00-9c87-58479196d233",
    # "Password":"liferocks",
    # "IntegratorKey":"cdd05311-7fe2-40fe-b71b-9c7da37a8bad"}' \
    #               https://demo.docusign.net/restapi/v2/accounts/3915659/envelopes

    # sign()
    url = 'https://demo.docusign.net/restapi/v2/accounts/3915659/envelopes'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-DocuSign-Authentication': '{ "Username":"8df3037b-aa57-4e00-9c87-58479196d233","Password":"liferocks",   "IntegratorKey":"cdd05311-7fe2-40fe-b71b-9c7da37a8bad"}'
    }

    r = requests.post(url, headers=headers, data= open('payload.json', 'rb'))

    return r.text

@app.route('/index.html')
def goHome():
	return render_template('index.html')

@app.route('/about.html')
def goAbout():
	return render_template('about.html')


@app.route('/signup2.html')
def goSignUp2():
    return render_template('signup2.html')

@app.route('/signup3.html')
def goSignUp3():
    return render_template('signup3.html')

@app.route('/signup1.html')
def authCode():

    codeSent = "Your authentification code has been sent."
    authenCode = randint(1001, 9999)
    account_sid = "AC46ae6f5c92b0b000a82a98a92e1cbb82"
    auth_token = "a9e06fb944cc75071253f9cb0d0b6cde"
    client = Client(account_sid, auth_token)
    client.api.account.messages.create(
		to="+14083488437",
		from_="+14158818917",
		body="Thank you for signing up for blujeans! Your authentification code is " + str(authenCode))

    return render_template('signup1.html', codeS = codeSent)

@app.route('/otp.html')
def authCode():


if __name__ == '__main__':
    app.run(host='0.0.0.0')
