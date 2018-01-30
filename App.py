import os
import sys
from flask import Flask
import json
import config
import requests
from flask import Flask, request
from GoogleDrive import GoogleDriveManager
from JsonConfig import JsonConfig as jsConf

app = Flask(__name__)
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

    # atlas_file = _load_atlas()
    user_file = file_manager.search_first(query_title=_convert_email_to_title(email))
    json_conf = jsConf(json=json.load(user_file.GetContentString()))
    
    qr_codes = json_conf.get(config.QR_COL)
    if qr not in qr_codes:
        if not json_conf.append(config.QR_COL, qr):
            print("Something went wrong")
            sys.stdout.flush()
        else:
            user_file.SetContentString(json_conf.dump())
            file_manager.upload_file(user_file)
    else:
        print("You already scanned that qr code!")
        sys.stdout.flush()

@app.route('/', methods=['POST'])
def handle_post_request():
    print("Recieved web request.")
    sys.stdout.flush()

    try:
        json_body = request.get_json()
    except Exception("error"):
        return 500

    if None in (json_body['email'], json_body['qr']):
        print("Bad Formating")
        sys.stdout.flush()
        return 500
    else:
        return update_or_create(json_body['email'], json_body['qr'])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=FLASK_DEBUG,
        threaded=THREADING
    )
    print("App started")
    sys.stdout.flush()
