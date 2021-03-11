import numpy as np
from flask import Flask, request, make_response
import json
import pickle
from flask_cors import cross_origin
import os
import sklearn

import smtplib
import time
import urllib.parse
import urllib.request
from urllib.request import urlopen
import requests




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
    Petal_length=parameters.get("number")
    Petal_width = parameters.get("number1")
    Sepal_length=parameters.get("number2")
    Sepal_width=parameters.get("number3")
    int_features = [Petal_length,Petal_width,Sepal_length,Sepal_width]
    
    final_features = [np.array(int_features)]
	 
    intent = result.get("intent").get('displayName')
    
    
    
    
    
    
    
    
    
    
    
    if (intent=='IrisData'):
    
        url = 'https://jaqjv6q0bb.execute-api.us-east-2.amazonaws.com/invoke_endpoint/invoke'  # localhost and the defined port + endpoint
        body = {
                "day": np.random.randint(1, 8),
                "month": np.random.randint(1, 13),
                "location": np.random.randint(1, 6),
                "contract": np.random.randint(1, 4),
                "activity": np.random.randint(1, 3),
                "building_story": np.random.randint(1, 15),
                "construction_type": np.random.randint(1, 5),
                "assigned_task": np.random.randint(1, 3),
                "lighting_conditions": np.random.randint(1, 51),
                "atmospheric_conditions": np.random.randint(-15, 36),
                "surface_conditions": np.random.randint(1, 5),
                "worker_age": np.random.randint(18, 58),
                "ppe": np.random.randint(0, 2),
                "safety_training": np.random.randint(0, 2),
                "specific_experience": np.random.randint(0, 40),
                "experience": np.random.randint(0, 40)
            }
        values = body		
        url_values = urllib.parse.urlencode(values)
        print("Values from PACE inputs: ")
        for n in values:
            print("{} -> {}".format(n, str(values[n])))    
        print("...")
        # print("..")
        # print("...")
        full_url = url + '?' + url_values
        data = urllib.request.urlopen(full_url)
        string = data.read().decode('utf-8')
        json_obj = json.loads(string)
        if json_obj['incidenttype'] == "ALL CLEAR":
            body["incident"]=2
        elif json_obj['incidenttype'] == "ALERT: There is a chance of an accident":
            body["incident"]=0
        else:
            body["incident"]=1    
                        
        prediction = body["incident"]
    
        output = round(prediction[0], 2)
    
    	
        if(output==0):
            flowr = 'Accident'
    
        if(output==1):
            flowr = 'Minor Incident'
        
        if(output==2):
            flowr = 'Major Incident'
       
        fulfillmentText= "The incident type seems to be..  {} !".format(flowr)
        #log.write_log(sessionID, "Bot Says: "+fulfillmentText)
        return {
            "fulfillmentText": fulfillmentText
        }
    #else:
    #    log.write_log(sessionID, "Bot Says: " + result.fulfillmentText)

#if __name__ == '__main__':
    #app.run()
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
        
