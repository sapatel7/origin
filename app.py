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

    emergency_dict = {"Heart Attack":"~A heart attack is a medical emergency. A heart attack usually occurs when a blood clot blocks blood flow to the heart. Without blood, tissue loses oxygen and dies. Checkout for Precaution and Symptom", "Paralysis":"~Paralysis is most often caused by damage in the nervous system, especially the spinal cord. Checkout for Precaution and Symptom", "Snake Bite":"~A snake bite can be life-threatening if the snake is venomous. Checkout for Precaution and Symptom", "Disease4":"s", "Disease5":"s"}

    precaution_dict = {"Heart Attack":"~Precaution for heart attack - Try to keep the person calm, and have them sit or lie down or If the person is not allergic to aspirin, have them chew and swallow a baby aspirin or If the person stops breathing, you or someone else who’s qualified should perform CPR right away.~https://drop.ndtv.com/TECH/product_database/images/952017124653PM_120_xiaomi_mi_a1.jpeg?downsize=120:90&output-quality=60&output-format=jpg", "Paralysis":"~Precaution for paralysis - If a paralytic patient had the problem of sugar from before then he should keep monitoring the blood glucose level to recover soon from paralysis or The quantity of the urine of the patient should be measured daily to know the position of kidney.~https://drop.ndtv.com/TECH/product_database/images/952017124653PM_120_xiaomi_mi_a1.jpeg?downsize=120:90&output-quality=60&output-format=jpg", "Snake Bite":"~Precaution for snake bite - Reassure the victim (70percent of all snakebites are by nonvenomous snakes and 50percent of bites by venomous species are dry bites) or Immobilize the affected limb (by bandage or clothes to hold splint, but tight arterial compression is not recommended) or Promptly transfer of victim to hospital.~https://drop.ndtv.com/TECH/product_database/images/952017124653PM_120_xiaomi_mi_a1.jpeg?downsize=120:90&output-quality=60&output-format=jpg", "Disease4":"s", "Disease5":"s"}

    symptom_dict = {"Heart Attack":"~Symptoms for heart attack are - Chest discomfort that feels like pressure, fullness, or a squeezing pain or Pain and discomfort that go beyond your chest to other parts of your upper body or Unexplained shortness of breath", "Paralysis":"~Symptoms for paralysis are - Be alert when you feel such symptom as that of an intense and sudden unexplainable headache or feeling of sudden emptiness or weakness in any part of body", "Snake Bite":"~Symptoms for snake bite are - pain at the snake bite or difficulty in breathing or low blood pressure", "Disease4":"s", "Disease5":"s"}

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
