import os
from flask import Flask
import json
import config
import requests
from flask import Flask, request
from GoogleDrive import GoogleDriveManager

app = Flask(__name__)
file_manager = GoogleDriveManager()

THREADING = False
FLASK_DEBUG = True


def _load_atlas():
    atlas_file = file_manager.find_existing_file(query_title=config.ATLAS)
    if atlas_file:
        atlas_string = atlas_file.GetContentString()
        
        return atlas_file
    print("Error loading Atlas File")
    return False


def _convert_email_to_title(email):
    title = email.replace('@', '')
    # Addtional changes here
    return title


def check_for_existing(email, qr):

    atlas_file = _load_atlas()

    title = _convert_email_to_title(email)
        

    def check_for_existing_qr(qr):
        

@app.route('/', methods=['POST'])
def handle_post_request():
    print("Recieved web request.")

    try:
        json_body = request.get_json()
    except Exception("error"):
        return 500

    if None in (json_body['email'], json_body['qr']):
        print("Bad Formating")
        return 500
    else:


    return 200


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))
    app.run(
        port=port,
        debug=FLASK_DEBUG,
        threaded=THREADING
    )
