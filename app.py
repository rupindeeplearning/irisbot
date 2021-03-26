import numpy as np
from flask import Flask, request, make_response, jsonify
from flask import render_template, redirect, url_for
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
filename = 'description.pkl'
filename1 = 'parameters.pkl'
@app.route('/')
def index():
    return render_template('index.html')

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
    return r #make_response(jsonify(res[0])) #render_template('webhook.html')


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
        
    outfile = open(filename1,'wb')   
    pickle.dump(int_features,outfile)
    outfile.close()
    
    final_features = [np.array(int_features)]
	 
    intent = result.get("intent").get('displayName')
    
    
    
    
    
    
    
    
    
    
    
    if (intent=='IrisData'):
    
        flowr = "You noticed {} committing the infraction of {} at {}. The condition was {}. The issue resolution was {}. If this is correct click update below and then submit the form.".format(atFault, fault, location, condition, issueNotAddressed)
        print(flowr)
        fulfillmentText= flowr
        flowr_1 = "You noticed {} committing the infraction of {} at {}. The condition was {}. The issue resolution was {}.".format(atFault, fault, location, condition, issueNotAddressed)
        outfile = open(filename,'wb')   
        pickle.dump(flowr_1,outfile)
        outfile.close()        
        #log.write_log(sessionID, "Bot Says: "+fulfillmentText)
        #returnlist = ["If the following form is correct, click submit to send. Otherwise, either use the chatbot to enter values again or manually enter data in the form.", oic_date]        
                
        return {"fulfillmentText": fulfillmentText}
        '''{
            "fulfillmentText": fulfillmentText
        }'''
        
               
    #else:
    #    log.write_log(sessionID, "Bot Says: " + result.fulfillmentText)

#if __name__ == '__main__':
    #app.run()
@app.route('/formupdate')
def formupdate():
    print("Update works so far")
    infile = open(filename,'rb')
    new_dict = pickle.load(infile)
    infile.close()
    print(new_dict)
    infile = open(filename1,'rb')
    new_dict_1 = pickle.load(infile)
    infile.close()
    print(new_dict_1)
    oic_date = datetime.today().strftime('%Y-%m-%d')    
    
        
    
    
    
    



    return render_template('index.html',bot_message="If the form is correct, submit the form.",oic_date=oic_date, oic_latitude="51.4568", oic_longitude="-77.7895",  oic_atfault = new_dict_1[4], oic_addressed = new_dict_1[3], oic_condition = new_dict_1[2], oic_description = new_dict, oic_location = new_dict_1[0])       
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
        
