import json

from flask import request, jsonify, make_response
from flask import Flask
from flask_cors import CORS
from flask import Response

app = Flask(__name__)
CORS(app)

from api_manager import invoke_api


@app.route('/my_webhook', methods=['POST'])
def post_webhook_dialogflow():
    body = request.get_json(silent=True)
    session_id = body['detectIntentResponseId']
    print ("responseid")
    print(session_id)
    #The tag used to identify which fulfillment is being called.
    fulfillment = body['fulfillmentInfo']['tag']
    slots = []
    for key, value in body['sessionInfo']['parameters'].items():
        slots.append({'name':key,'value':value})
       
    print (slots)
    # msg = 'hi'
    msg = invoke_api(fulfillment, slots)
    return answer_webhook(msg, session_id)


def answer_webhook(msg, session_id):
    message= {"fulfillment_response": {
      
        "messages": [
        {
          "text": {
            "text": [msg]
          }
        }
      ]
    }
    }
    return Response(json.dumps(message), 200, mimetype='application/json')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)
