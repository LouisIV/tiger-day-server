import os
import sys
from flask import Flask
from flask_cors import CORS
import json
import config
import requests
from flask import Flask, request
from GoogleDrive import GoogleDriveManager
from JsonConfig import JsonConfig as jsConf

app = Flask(__name__)
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
file_manager = GoogleDriveManager()

THREADING = False
FLASK_DEBUG = True

'''
def _load_atlas():
    atlas_file = file_manager.find_existing_file(query_title=config.ATLAS)
    if atlas_file:
        atlas_string = atlas_file.GetContentString()
        
        return atlas_file
    print("Error loading Atlas File")
    return False
'''


def _convert_email_to_title(email):
    # title = email.replace('@', '')
    # Addtional changes here
    return email


def update_or_create(email, qr):

    # So we can see it in the console
    print("Email: %s, QR: %s" % (email, qr))
    sys.stdout.flush()

    # Write to google drive
    user_file = file_manager.search_first(query_title=_convert_email_to_title(email))
    user_file.SetContentString(user_file.GetContentString() + "," + qr)
    file_manager.upload_file(user_file)

    # For the user
    response = flask.jsonify({'drive_status': '200'})
    return response
'''
@app.after_request
def after_request(response):
    header = response.headers
    header.add('Access-Control-Allow-Origin','*')
    header.add('Content-Type','application/json')
    return response
'''

@app.route('/', methods=['POST'])
def handle_post_request():
    print("Recieved web request.")
    sys.stdout.flush()

    response = flask.jsonify({'drive_status': '200'})

    try:
        json_body = request.get_json()

        if None in (json_body['email'], json_body['qr']):
            print("Bad Formating")
            sys.stdout.flush()

            response = flask.jsonify({'drive_status': '400'})
            return response
        else:
            return update_or_create(json_body['email'], json_body['qr'])
    except:
        return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=FLASK_DEBUG,
    )
    print("App started")
    sys.stdout.flush()
