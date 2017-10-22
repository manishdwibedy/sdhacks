'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

from flask import Flask, render_template, request, redirect, url_for
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
    return render_template('signup1.html');


@app.route('/code')
def code():
    '''
    https://genomelink.io/oauth/authorize?redirect_uri=http://127.0.0.1:5000/code&client_id=PftOLTI13hNYN9gl2UOJKzcNTalDBSbPv8ceTevm&response_type=code&scope=report:childhood-intelligence report:hearing-function report:word-reading-ability report:reading-and-spelling-ability report:eye-color

    :return:
    '''
    user_code = request.args.get('code')
    Config.code = str(user_code)
    return redirect(url_for('access_token'))

@app.route('/access_token')
def access_token():
    url = 'https://genomelink.io/oauth/token'

    payload = {
        'client_id': 'PftOLTI13hNYN9gl2UOJKzcNTalDBSbPv8ceTevm',
        'client_secret': 'gZj2dfZLoQ9my9Ycss21TQXBnRZSizj3EfOtILu2V4wSBmofvlGejc6I22j4lbMwfkREbivpHG4qU4y6wt2N3Dh1LpozHGhrV3g4ElZYH23xWeWf2LG9OgpAA2t94nqi',
        'grant_type': 'authorization_code',
        'code': Config.code,
        'redirect_uri': 'http://127.0.0.1:5000/code'
    }

    print payload
    r = requests.post(url, data= payload)
    output = r.text
    json_output = json.loads(output)
    access_token = json_output['access_token']
    Config.access_token = access_token
    return render_template('access-granted.html')


@app.route('/eye-color')
def eye_color():
    url = 'https://genomelink.io/v1/reports/morning-person?population=european'

    '''
    curl -X POST -d "client_id=PftOLTI13hNYN9gl2UOJKzcNTalDBSbPv8ceTevm&client_secret=gZj2dfZLoQ9my9Ycss21TQXBnRZSizj3EfOtILu2V4wSBmofvlGejc6I22j4lbMwfkREbivpHG4qU4y6wt2N3Dh1LpozHGhrV3g4ElZYH23xWeWf2LG9OgpAA2t94nqi&grant_type=authorization_code&code=zbnHZECvb88GJaWfJ5j6F5b9kUEzuo&redirect_uri=http://127.0.0.1:5000/code" https://genomelink.io/oauth/token

    '''

    headers = {
        'Authorization': 'Bearer ' + Config.access_token,
    }

    if len(Config.access_token) == 0:
        return redirect(
            'https://genomelink.io/oauth/authorize?redirect_uri=http://127.0.0.1:5000/code&client_id=PftOLTI13hNYN9gl2UOJKzcNTalDBSbPv8ceTevm&response_type=code&scope=report:morning-person report:weight report:longevity report:male-pattern-baldness-aga report:freckles report:agreeableness report:neuroticism report:openness report:anger')

    r = requests.get(url, headers = headers)

    if str(r.status_code)[0] == '4':
        return redirect(
            'https://genomelink.io/oauth/authorize?redirect_uri=http://127.0.0.1:5000/code&client_id=PftOLTI13hNYN9gl2UOJKzcNTalDBSbPv8ceTevm&response_type=code&scope=report:morning-person report:weight report:longevity report:male-pattern-baldness-aga report:freckles report:agreeableness report:neuroticism report:openness report:anger')

    output = json.loads(r.text)

    parameters = []
    response = []
    html = '<table><tr><th>Parameter</th><th>Value</th></tr>'


    if 'summary' in output:
        for parameter in ['morning-person', 'weight', 'longevity','male-pattern-baldness-aga', 'freckles', 'agreeableness', 'neuroticism', 'openness', 'anger']:
            headers = {
                'Authorization': 'Bearer ' + Config.access_token,
            }
            r = requests.get(url, headers=headers)
            output = json.loads(r.text)
            html += '<tr><td>' + parameter + '</td><td>' + output['summary']['text'] + '</td></tr>'
            parameters.append(parameter);
            response.append(output['summary']['text']);
        html += '</table>'
        return render_template('reports.html', parameters = parameters, output = response)


@app.route('/sign-doc')
def signDoc():
    url = 'https://demo.docusign.net/restapi/v2/accounts/3915659/envelopes'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-DocuSign-Authentication': '{ "Username":"8df3037b-aa57-4e00-9c87-58479196d233","Password":"liferocks",   "IntegratorKey":"cdd05311-7fe2-40fe-b71b-9c7da37a8bad"}'
    }

    r = requests.post(url, headers=headers, data= open('payload.json', 'rb'))
    output = json.loads(r.text)

    if output['status'] == 'sent':
        return render_template('sign-waiver.html')
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

@app.route('/signup-sms')
def authCode():
    codeSent = "Your authentification code has been sent."
    authenCode = randint(1001, 9999)
    account_sid = "AC46ae6f5c92b0b000a82a98a92e1cbb82"
    auth_token = "a9e06fb944cc75071253f9cb0d0b6cde"
    client = Client(account_sid, auth_token)
    client.api.account.messages.create(to="+14083488437",
        from_="+14158818917",
        body="Thank you for signing up for blujeans! Your authentification code is " + str(authenCode))
    return render_template('signup1.html', codeS = str(authenCode))



if __name__ == '__main__':
    app.run(host='0.0.0.0')
