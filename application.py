# Import functions and objects the microservice needs.
# - Flask is the top-level application. You implement the application by adding methods to it.
# - Response enables creating well-formed HTTP/REST responses.
# - requests enables accessing the elements of an incoming HTTP/REST request.
#
import json

# Setup and use the simple, common Python logging framework. Send log messages to the console.
# The application should get the log level out of the context. We will change later.
#

import hashlib, binascii, os
import sys
import platform
import socket

from flask import Flask, Response
from flask import request, jsonify
import hashlib

cwd = os.getcwd()
sys.path.append(cwd)
jwt_key = os.environ['jwt_key']
salt = os.environ['salt'].encode('utf-8')

print("*** PYHTHONPATH = " + str(sys.path) + "***")

import logging
import dbsvc as db
from datetime import datetime, timedelta

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

import jwt


# Create the application server main class instance and call it 'application'
# Specific the path that identifies the static content and where it is.
application = Flask(__name__,
                    static_url_path='/static',
                static_folder='WebSite/static')




# 1. Extract the input information from the requests object.
# 2. Log the information
# 3. Return extracted information.
#
def log_and_extract_input(method, path_params=None):

    path = request.path
    args = dict(request.args)
    data = None
    headers = dict(request.headers)
    method = request.method

    try:
        if request.data is not None:
            data = request.json
        else:
            data = None
    except Exception as e:
        # This would fail the request in a more real solution.
        data = "You sent something but I could not get JSON out of it."

    log_message = str(datetime.now()) + ": Method " + method

    inputs =  {
        "path": path,
        "method": method,
        "path_params": path_params,
        "query_params": args,
        "headers": headers,
        "body": data
        }

    log_message += " received: \n" + json.dumps(inputs, indent=2)
    logger.debug(log_message)

    return inputs


def log_response(method, status, data, txt):

    msg = {
        "method": method,
        "status": status,
        "txt": txt,
        "data": data
    }

    logger.debug(str(datetime.now()) + ": \n" + json.dumps(msg, indent=2, default=str))


welcome = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
  <!--
    Copyright 2012 Amazon.com, Inc. or its affiliates. All Rights Reserved.

    Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

        http://aws.Amazon/apache2.0/

    or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
  -->
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>Welcome</title>
  <style>
  body {
    color: #ffffff;
    background-color: #E0E0E0;
    font-family: Arial, sans-serif;
    font-size:14px;
    -moz-transition-property: text-shadow;
    -moz-transition-duration: 4s;
    -webkit-transition-property: text-shadow;
    -webkit-transition-duration: 4s;
    text-shadow: none;
  }
  body.blurry {
    -moz-transition-property: text-shadow;
    -moz-transition-duration: 4s;
    -webkit-transition-property: text-shadow;
    -webkit-transition-duration: 4s;
    text-shadow: #fff 0px 0px 25px;
  }
  a {
    color: #0188cc;
  }
  .textColumn, .linksColumn {
    padding: 2em;
  }
  .textColumn {
    position: absolute;
    top: 0px;
    right: 50%;
    bottom: 0px;
    left: 0px;

    text-align: right;
    padding-top: 11em;
    background-color: #1BA86D;
    background-image: -moz-radial-gradient(left top, circle, #6AF9BD 0%, #00B386 60%);
    background-image: -webkit-gradient(radial, 0 0, 1, 0 0, 500, from(#6AF9BD), to(#00B386));
  }
  .textColumn p {
    width: 75%;
    float:right;
  }
  .linksColumn {
    position: absolute;
    top:0px;
    right: 0px;
    bottom: 0px;
    left: 50%;

    background-color: #E0E0E0;
  }

  h1 {
    font-size: 500%;
    font-weight: normal;
    margin-bottom: 0em;
  }
  h2 {
    font-size: 200%;
    font-weight: normal;
    margin-bottom: 0em;
  }
  ul {
    padding-left: 1em;
    margin: 0px;
  }
  li {
    margin: 1em 0em;
  }
  </style>
</head>
<body id="sample">
  <div class="textColumn">
    <h1>Congratulations</h1>
    <p>My second, modified AWS Elastic Beanstalk Python Application is now running on your own dedicated environment in the AWS Cloud</p>
  </div>

  <div class="linksColumn"> 
    <h2>What's Next?</h2>
    <ul>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/">AWS Elastic Beanstalk overview</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/index.html?concepts.html">AWS Elastic Beanstalk concepts</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Python_django.html">Deploy a Django Application to AWS Elastic Beanstalk</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Python_flask.html">Deploy a Flask Application to AWS Elastic Beanstalk</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/create_deploy_Python_custom_container.html">Customizing and Configuring a Python Container</a></li>
    <li><a href="http://docs.amazonwebservices.com/elasticbeanstalk/latest/dg/using-features.loggingS3.title.html">Working with Logs</a></li>

    </ul>
  </div>
</body>
</html>
"""

@application.route("/")
def index():

    rsp = Response(welcome, status=200, content_type="text/html")
    return rsp


# This function performs a basic health check. We will flesh this out.
@application.route("/api/health", methods=["GET"])
def health_check():

    pf = platform.system()

    rsp_data = { "status": "healthy", "time": str(datetime.now()),
                 "platform": pf,
                 "release": platform.release()
                 }

    if pf == "Darwin":
        rsp_data["note"]= "For some reason, macOS is called 'Darwin'"


    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    rsp_data["hostname"] = hostname
    rsp_data["IPAddr"] = IPAddr

    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="application/json")
    return rsp


@application.route("/demo/<parameter>", methods=["GET", "POST"])
def demo(parameter):

    inputs = log_and_extract_input(demo, { "parameter": parameter })

    msg = {
        "/demo received the following inputs" : inputs
    }

    rsp = Response(json.dumps(msg), status=200, content_type="application/json")
    return rsp

@application.route("/Users", methods=["GET"])
@application.route("/Users/<parameter>", methods=["GET"])
def getUsers(parameter=""):

    if parameter:
        sql = f"SELECT * from CatalogService.Users LIMIT {parameter};"
    else:
        sql = f"SELECT * from CatalogService.Users;"
    msg = db.getDbConnection(sql)
    print(msg)
    rsp = Response(json.dumps(msg, default=str), status=200, content_type="application/json")

    return rsp

@application.route("/Users", methods=["POST"])
def addUsers(hashed_password):
    body = json.loads(request.data.decode())
    body['hashed_Password'] = hashed_password
    names = [x for x, y in body.items()]
    values = [y for x, y in body.items()]
    values = '", "'.join(map(str, values))
    names = ', '.join(map(str, names))
    sql = f'INSERT INTO CatalogService.Users ({names}) values ("{values}");'
    print(sql)
    msg = db.getDbConnection(sql)
    print(msg)
    rsp = Response(json.dumps(msg, default=str), status=200, content_type="application/json")

    return rsp

@application.route("/Users/id/<id>", methods=["DELETE"])
def deleteUsers(id):

    sql = f'DELETE from CatalogService.Users WHERE id={id};'
    print(sql)
    msg = db.getDbConnection(sql)
    print(msg)
    rsp = Response(json.dumps(msg, default=str), status=200, content_type="application/json")

    return rsp

@application.route("/Users/id/<id>", methods=["PUT"])
def updateUsers(id):

    body = json.loads(request.data.decode())
    names = [x for x, y in body.items()]
    values = [y for x, y in body.items()]
    stringy = ''
    for i, name in enumerate(names):
        stringy += f'{name} = "{values[i]}", '
    stringy = stringy[:-2]
    print(stringy)
    sql = f'UPDATE CatalogService.Users SET {stringy} WHERE id={id};'
    print(sql)
    msg = db.getDbConnection(sql)
    print(msg)
    rsp = Response(json.dumps(msg, default=str), status=200, content_type="application/json")

    return rsp

@application.route("/Address", methods=["GET"])
@application.route("/Address/<parameter>", methods=["GET"])
def getAddresses(parameter=""):

    if parameter:
        sql = f"SELECT * from CatalogService.Address LIMIT {parameter};"
    else:
        sql = f"SELECT * from CatalogService.Address;"
    msg = db.getDbConnection(sql)
    print(msg)
    rsp = Response(json.dumps(msg, default=str), status=200, content_type="application/json")

    return rsp

@application.route("/Address", methods=["POST"])
def addAddresses():

    body = json.loads(request.data.decode())
    names = [x for x, y in body.items()]
    values = [y for x, y in body.items()]
    values = '", "'.join(map(str, values))
    names = ', '.join(map(str, names))
    sql = f'INSERT INTO CatalogService.Address ({names}) values ("{values}");'
    print(sql)
    msg = db.getDbConnection(sql)
    print(msg)
    rsp = Response(json.dumps(msg, default=str), status=200, content_type="application/json")

    return rsp
@application.route("/Address/id/<id>", methods=["DELETE"])
def deleteAddress(id):

    sql = f'DELETE from CatalogService.Address WHERE id={id};'
    print(sql)
    msg = db.getDbConnection(sql)
    print(msg)
    rsp = Response(json.dumps(msg, default=str), status=200, content_type="application/json")

    return rsp

@application.route("/Address/id/<id>", methods=["PUT"])
def updateAddress(id):

    body = json.loads(request.data.decode())
    names = [x for x, y in body.items()]
    values = [y for x, y in body.items()]
    stringy = ''
    for i, name in enumerate(names):
        stringy += f'{name} = "{values[i]}", '
    stringy = stringy[:-2]
    print(stringy)
    sql = f'UPDATE CatalogService.Address SET {stringy} WHERE id={id};'
    print(sql)
    msg = db.getDbConnection(sql)
    print(msg)
    rsp = Response(json.dumps(msg, default=str), status=200, content_type="application/json")

    return rsp

@application.route("/Registrations", methods=["POST"])
def registerUser():
    body = json.loads(request.data.decode())
    password = body['hashed_Password']
    hashed_password = hash(password)
    rsp = addUsers(hashed_password)
    token = encode_token(body['email'], 'user')
    rsp.headers['token'] = token
    return rsp

@application.route("/logins", methods=["POST"])
def login():
    body = json.loads(request.data.decode())
    password = body['hashed_Password']
    hashed_password = hash(password)
    sql = f'SELECT hashed_Password from CatalogService.Users WHERE id={body["id"]};'
    msg = db.getDbConnection(sql)
    stored_password = msg[0]['hashed_Password']
    print(stored_password)
    if password == stored_password:
        rsp = Response(json.dumps("", default=str), status=201, content_type="application/json")
        token = encode_token(body['email'], 'user')
        rsp.headers['token'] = token
        return rsp
    else:
        rsp = Response(json.dumps("", default=str), status=401, content_type="application/json")
        return rsp

def hash(password):
    res = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        password.encode('utf-8'), # Convert the password to bytes
        salt, # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
    )
    return res

def encode_token(email, role):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=7, seconds=0),
            'iat': datetime.utcnow(),
            'email': email,
            'role': role 
        }
        return jwt.encode(
            payload,
            jwt_key,
            algorithm='HS256'
            )
    except Exception as e:
        return e

def decode_token(auth_token):
    try:
        payload = jwt.decode(auth_token, Env.MOOVE_PRIVATE_KEY())
        # print(payload)
        return payload['googleId'], payload['userType']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.', None
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.', None	
	


@application.route("/boo", methods=["GET"])
def boo():
    rsp = Response("Hoo", status=200, content_type="text/plain")
    return rsp

@application.route("/hello_puppy", methods=["GET"])
def hello_puppy():
    rsp = Response("Hello_Puppy", status=200, content_type="text/plain")
    return rsp

@application.route("/hello_world", methods=["GET"])
def hello_world():
    rsp = Response("Hello_World", status=200, content_type="text/plain")
    return rsp

@application.route("/service_info", methods=["GET"])
def service_info():
    service_info_msg = """
    <html>
    <head>
    </head>
    <body>
        <h1> This is where the service info will be </h1>
    </body>
    </html>
    """
    rsp = Response(service_info_msg, status=200, content_type="text/html")
    return rsp

logger.debug("__name__ = " + str(__name__))

def myfirstmethod(verb, path, path_params, query_params, headers, body):
    pass

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.

    application.run(host='0.0.0.0', port=8000)
