'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

from flask import Flask, render_template, request
from application import db
from application.models import Data
from application.forms import EnterDBInfo, RetrieveDBInfo
'''import genomelink'''
from twilio.rest import Client
from random import randint



# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
@application.route("/")
def result():
    return render_template('index.html'); 



if __name__ == '__main__':
    application.run(host='0.0.0.0')
