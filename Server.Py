
from urllib import request
from flask import Flask 
app = Flask(__name__) #s used to create a Flask application object. This object is used to create and manage the web application.

@app.route('/') #is used to define a route for the web application. This route is used to handle requests to the root URL of the application.
def globalRoute(): #It is used to define a function that is called when a request is made to the root URL of the application. The function can be used to handle the request and return a response.
    return "ALL OK"
@app.route('/telemetrysink', methods = ['POST']) #is used to define a route for the web application. This route is used to handle POST requests to the /telemetrysink URL of the application.				
def telemtrySink(): #It is used to define a function that is called when a POST request is made to the /telemetrysink URL of the application. The function can be used to handle the request and return a response.
    params=request.json #is used to extract the JSON data from a request. The JSON data contains the parameters that were sent in the request.
    return params

if __name__=='__main__':
    app.run() #is used to start the web application. This will start the web server and make the application available to handle requests.