import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS
from flask import json
import config
import requests
from flask import Flask, request
from GoogleDrive import GoogleDriveManager
from JsonConfig import JsonConfig as jsConf

app = Flask(__name__)
CORS(app)
file_manager = GoogleDriveManager()

FLASK_DEBUG = True

def _convert_email_to_title(email):
    # title = email.replace('@', '')
    # Addtional changes here
    return email

def update_or_create(email, qr, notes, priority):

    # So we can see it in the console
    print("Email: %s, QR: %s" % (email, qr))
    print("Notes: %s, P: %s" % (notes, priority))
    sys.stdout.flush()

    # Create or find the file
    user_file = file_manager.search_first(query_title=_convert_email_to_title(email))
    if not user_file:
        return jsonify({'drive_status': '500'})

    user_dict = {}

    # Load the file
    if not user_file.GetContentString() or user_file.GetContentString() == "":
        user_dict["email"] = email
        user_dict["scans"] = []
    else:
        user_dict = json.loads(user_file.GetContentString())

    print("`user_dict`: %s" % str(user_dict))
    sys.stdout.flush()

    # Create the scan object, which we will upload.
    scan = {}
    scan['qr'] = qr
    scan['notes'] = notes
    scan['priority'] = priority

    # Add the object to the dictionary
    user_dict['scans'].append(scan)

    print(user_dict)
    sys.stdout.flush()

    print(json.dumps(user_dict))
    sys.stdout.flush()

    # Set the contents of dictionary as the content and upload
    file_manager.write_to_file(user_file, json.dumps(user_dict), upload=True)
    # user_file.SetContentString(json.dumps(user_dict))
    # file_manager.upload_file(user_file)

    # For the user
    response = jsonify({'drive_status': '200'})
    return response

@app.route('/', methods=['POST'])
def handle_post_request():
    print("Recieved web request.")
    sys.stdout.flush()

    response = jsonify({'drive_status': '200'})

    try:
        json_body = request.get_json()

        if None in (json_body['email'], json_body['qr'], json_body['notes'], json_body['priority']):
            print("Bad Formating")
            sys.stdout.flush()

            response = jsonify({'drive_status': '400'})
            return response
        else:
            return update_or_create(json_body['email'], json_body['qr'],
                                    json_body['notes'], json_body['priority'])
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
