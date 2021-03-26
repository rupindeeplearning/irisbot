import numpy as np
from flask import Flask, request, make_response, render_template
import json
import pickle
from flask_cors import cross_origin
import os
import sklearn

import urllib.parse
import urllib.request
from urllib.request import urlopen


from datetime import datetime




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
    location=parameters.get("location")
    fault = parameters.get("fault")
    condition=parameters.get("condition")
    issueNotAddressed=parameters.get("issueNotAddressed")
    atFault=parameters.get("atfault")
    int_features = [location,fault,condition,issueNotAddressed,atFault]
    
    final_features = [np.array(int_features)]
	 
    intent = result.get("intent").get('displayName')
    
    
    
    
    
    
    
    
    
    
    
    if (intent=='IrisData'):
    
        flowr = "You noticed {} committing the infraction {} at {}. The condition was a/an {}. The issue resolution was {}. If this is correct click submit on the form. If you have to make any changes, use the other chatbot.".format(atFault, fault, location, condition, issueNotAddressed)
       
        fulfillmentText= flowr
        #log.write_log(sessionID, "Bot Says: "+fulfillmentText)
        return render_template("index.html", bot-message = "If the following form is correct, click submit to send. Otherwise, either use the chatbot to enter values again or manually enter data in the form.", oic-date=datetime.today().strftime('%Y-%m-%d'))
        '''{
            "fulfillmentText": fulfillmentText
        }'''
        
               
    #else:
    #    log.write_log(sessionID, "Bot Says: " + result.fulfillmentText)

#if __name__ == '__main__':
    #app.run()
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
        
