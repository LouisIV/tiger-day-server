import os
from flask import Flask
app = Flask(__name__)

THREADING = False
FLASK_DEBUG = True


@app.route('/', methods=['POST'])
def handle_post_request():
    print("Recieved web request.")
    return 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        port=port,
        debug=FLASK_DEBUG,
        threaded=THREADING
    )
