#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    result = req.get("result")
    contexts = result.get("contexts")
    parameters = contexts[0].get("parameters")
    components = parameters.get("components")
    emergency = parameters.get("emergency")

    emergency_dict = {"Heart Attack":"Heart attack is very severe", "Paralysis":"Paralysis is very severe", "Snake Bite":"Snake bite is very severe", "Disease4":"s", "Disease5":"s"}

    precaution_dict = {"Heart Attack":"1. HAP1.~2. HAP2", "Paralysis":"Paralysis is very severe", "Snake Bite":"Snake bite is very severe", "Disease4":"s", "Disease5":"s"}

    if(components == ""):
        speech = str(emergency_dict[emergency])
    else if(components == "Precaution"):
        speech = str(precaution_dict[emergency])
    else:
        speech = str("not found")

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": [],
        "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    app.run(debug=True, port=port, host='0.0.0.0')
