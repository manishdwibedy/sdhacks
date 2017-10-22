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
    '''
    https://genomelink.io/oauth/authorize?redirect_uri=http://127.0.0.1:5000/code&client_id=PftOLTI13hNYN9gl2UOJKzcNTalDBSbPv8ceTevm&response_type=code&scope=report:childhood-intelligence report:hearing-function report:word-reading-ability report:reading-and-spelling-ability report:eye-color

    :return:
    '''
    user_code = request.args.get('code')
    Config.code = str(user_code)
    return 'Got the code = ' + user_code

@app.route('/access_token')
def access_token():
    # token = request.args.get('token')
    # Config.access_token = token
    url = 'https://genomelink.io/oauth/token'
    #
    # '''
    # curl -X POST -d "client_id=PftOLTI13hNYN9gl2UOJKzcNTalDBSbPv8ceTevm&client_secret=gZj2dfZLoQ9my9Ycss21TQXBnRZSizj3EfOtILu2V4wSBmofvlGejc6I22j4lbMwfkREbivpHG4qU4y6wt2N3Dh1LpozHGhrV3g4ElZYH23xWeWf2LG9OgpAA2t94nqi&grant_type=authorization_code&code=cfyAnQfFsqRlHxkynZO37NjjoGr5Ml&redirect_uri=http://127.0.0.1:5000/code" https://genomelink.io/oauth/token

    # curl -X POST -d "client_id=PftOLTI13hNYN9gl2UOJKzcNTalDBSbPv8ceTevm&client_secret=gZj2dfZLoQ9my9Ycss21TQXBnRZSizj3EfOtILu2V4wSBmofvlGejc6I22j4lbMwfkREbivpHG4qU4y6wt2N3Dh1LpozHGhrV3g4ElZYH23xWeWf2LG9OgpAA2t94nqi&grant_type=authorization_code&code=lvqrfIbDFTKDbXeHXtAl7lN0Vpw9Ji&redirect_uri=http://127.0.0.1:5000/code" https://genomelink.io/oauth/token

    #
    # '''
    #
    # headers = {
    #     'Accept': 'application/json',
    #     'Content-Type': 'application/json',
    #     'X-DocuSign-Authentication': '{ "Username":"8df3037b-aa57-4e00-9c87-58479196d233","Password":"liferocks",   "IntegratorKey":"cdd05311-7fe2-40fe-b71b-9c7da37a8bad"}'
    # }
    #
    # grant_type = password & client_id = {IntegratorKey} & username = {email} & password = {password} & scope = api

    payload = {
        'client_id': 'PftOLTI13hNYN9gl2UOJKzcNTalDBSbPv8ceTevm',
        'client_secret': 'gZj2dfZLoQ9my9Ycss21TQXBnRZSizj3EfOtILu2V4wSBmofvlGejc6I22j4lbMwfkREbivpHG4qU4y6wt2N3Dh1LpozHGhrV3g4ElZYH23xWeWf2LG9OgpAA2t94nqi',
        'grant_type': 'authorization_code',
        'code': Config.code,
        'redirect_uri': 'http://127.0.0.1:5000/code'
    }

    print payload
    r = requests.post(url, data= payload)

    return r.text
    return 'Done '


@app.route('/eye-color')
def eye_color():
    url = 'https://genomelink.io/v1/reports/eye-color?population=european'

    '''
    curl -X POST -d "client_id=PftOLTI13hNYN9gl2UOJKzcNTalDBSbPv8ceTevm&client_secret=gZj2dfZLoQ9my9Ycss21TQXBnRZSizj3EfOtILu2V4wSBmofvlGejc6I22j4lbMwfkREbivpHG4qU4y6wt2N3Dh1LpozHGhrV3g4ElZYH23xWeWf2LG9OgpAA2t94nqi&grant_type=authorization_code&code=zbnHZECvb88GJaWfJ5j6F5b9kUEzuo&redirect_uri=http://127.0.0.1:5000/code" https://genomelink.io/oauth/token

    '''

    headers = {
        'Authorization': 'Bearer ' + Config.access_token,
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
    output = json.loads(r.text)

    if output['status'] == 'sent':
        return render_template('sign-waiver.html')
    return r.text


if __name__ == '__main__':
    app.run(host='0.0.0.0')
