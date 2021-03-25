import numpy as np
from flask import Flask, request, make_response
import json
import pickle
from flask_cors import cross_origin
import os
import sklearn

import urllib.parse
import urllib.request
from urllib.request import urlopen





app = Flask(__name__)
model = pickle.load(open('rf.pkl', 'rb'))

@app.route('/')
def hello():
    return 'Hello World'

# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():

    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):

    #sessionID=req.get('responseId')
    result = req.get("queryResult")
        
    #user_says=result.get("queryText")
    #log.write_log(sessionID, "User Says: "+user_says)
    parameters = result.get("parameters")
    location1="location 5"#parameters.get("location")
    fault = parameters.get("fault")
    condition=parameters.get("condition")
    issueNotAddressed=parameters.get("issueNotAddressed")
    atFault=parameters.get("atFault")
    issueNumber=parameters.get("issueNumber")
    if issueNumber == "":
        issueNumber = np.random.randint(10002,99999)
    int_features = [location1,fault,condition,issueNotAddressed,atFault,issueNumber]
    
    final_features = [np.array(int_features)]
	 
    intent = result.get("intent").get('displayName')
    session = req.get("session")
    
    
    
    
    
    
    
    
    
    
    if (intent=='Fault intent'):
    
        flowr = "You noticed {} committing the infraction {} at {}. The condition was a/an {}. The issue resolution was {}. The issue number is {}. If this is correct click submit on the form. If you have to make any changes, use the other chatbot.".format(atFault, fault, location1, condition, issueNotAddressed, issueNumber)
       
        fulfillmentText= flowr
        #log.write_log(sessionID, "Bot Says: "+fulfillmentText)
        return {
            "fulfillmentText": fulfillmentText,
            "outputContexts": [
                    {
                        "name": session+"/contexts/faultfinder",
                        "lifespanCount": 88,
                        "parameters": {
                            "location": location1,
                            "location.original": location1,
                            "fault":fault,
                            "condition":condition,
                            "issueNotAddressed":issueNotAddressed,
                            "atFault":atFault,
                            "issueNumber":issueNumber,
                            "issueNumber.original":issueNumber
                        }
                    },
                    {
                        "name": session+"/contexts/getfault",
                        "lifespanCount": 88,
                        "parameters": {
                            "location": location1,
                            "location.original": location1,
                            "fault":fault,
                            "condition":condition,
                            "issueNotAddressed":issueNotAddressed,
                            "atFault":atFault,
                            "issueNumber":issueNumber,
                            "issueNumber.original":issueNumber
                        }
                    }
                ],
            "followupEventInput": {
                "name": "WebhookResponse",
                "parameters": {
                    "location": location1,
                    "location.original": location1,
                    "fault":fault,
                    "condition":condition,
                    "issueNotAddressed":issueNotAddressed,
                    "atFault":atFault,
                    "issueNumber":issueNumber,
                    "issueNumber.original":issueNumber
                },
                "languageCode": "en-US"
            }
        }
        
               
    #else:
    #    log.write_log(sessionID, "Bot Says: " + result.fulfillmentText)

#if __name__ == '__main__':
    #app.run()
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
        
