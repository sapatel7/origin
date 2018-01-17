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

    emergency_dict = {"Heart Attack":"~Heart attack is very severe. Checkout for Precaution and Symptom", "Paralysis":"~Paralysis is very severe. Checkout for Precaution and Symptom", "Snake Bite":"~Snake bite is very severe. Checkout for Precaution and Symptom", "Disease4":"s", "Disease5":"s"}

    precaution_dict = {"Heart Attack":"~1. HAP1.*2. HAP2.~https://drop.ndtv.com/TECH/product_database/images/952017124653PM_120_xiaomi_mi_a1.jpeg?downsize=120:90&output-quality=60&output-format=jpg", "Paralysis":"~1. PP1.*2. PP2.~https://drop.ndtv.com/TECH/product_database/images/952017124653PM_120_xiaomi_mi_a1.jpeg?downsize=120:90&output-quality=60&output-format=jpg", "Snake Bite":"~1. SNP1.*2. SNP2.~https://drop.ndtv.com/TECH/product_database/images/952017124653PM_120_xiaomi_mi_a1.jpeg?downsize=120:90&output-quality=60&output-format=jpg", "Disease4":"s", "Disease5":"s"}

    symptom_dict = {"Heart Attack":"~1. HAS1.*2. HAS2", "Paralysis":"~1. PS1.*2. PS2", "Snake Bite":"~1. SNS1.*2. SNS2", "Disease4":"s", "Disease5":"s"}

    if(components == ""):
        speech = str(emergency_dict[emergency])
    elif(components == "Precaution"):
        speech = str(precaution_dict[emergency])
    elif(components == "Symptom"):
        speech = str(symptom_dict[emergency])
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
