import paho.mqtt.client as mqtt
import json	
import requests

mqtt_sub_topic="mqtt/avirup171/#"                   #is a subscription topic for the MQTT protocol. It is used to subscribe to all topics under the mqtt/avirup171/ path.
client=mqtt.Client()                                #is used to create an MQTT client object. This object can be used to connect to an MQTT broker and publish or subscribe to topics.
edgeDeviceSendTopic="mqtt/avirup171/edgeDevice"     #is a topic for the MQTT protocol. It is used to publish messages to the edgeDevice topic under the mqtt/avirup171/ path.
edgeDeviceReceiveTopicBase="mqtt/avirup171/"        #is a base topic for the MQTT protocol. It is used to subscribe to all topics under the mqtt/avirup171/ path.
serverUrl="http://127.0.0.1:5000/telemetrysink"     #is a URL for a web server. It is used to send telemetry data to the server at the specified address.
headers =  {"Content-Type":"application/json"}      #is a dictionary of headers for an HTTP request. It is used to specify the content type of the request as application/json.	

def on_connect(client, userdata, flags, rc):    #is a function definition. It is used to define a callback function that is called when the client connects to an MQTT broker.		
    client.connected_flag=True                  #is used to set a flag indicating that the client is connected to an MQTT broker. This flag can be used to check if the client is connected or not.
    client.disconnect_flag=False				#is used to set a flag indicating that the client is not disconnected from an MQTT broker. This flag can be used to check if the client is disconnected or not.						
    client.subscribe(mqtt_sub_topic)            # is used to subscribe to a topic on an MQTT broker. It is used to receive messages published to the specified topic.
    print("Connected")                          #in ra màn hình Connected
    print("rc: " + str(rc))                     #is used to print the return code of an MQTT operation. The return code indicates the success or failure of the operation.


def on_subscribe(client, userdata, mid, granted_qos):  #is a function definition. It is used to define a callback function that is called when the client successfully subscribes to a topic on an MQTT broker.
    print("Subscribed: " + str(mid) + " " + str(granted_qos)+" "+"Topic: "+mqtt_sub_topic)  #is used to print the details of a successful subscription to a topic on an MQTT broker. It prints the message ID, granted QoS, and the topic that was subscribed to.

def on_disconnect(client, userdata, rc):        #is a function definition. It is used to define a callback function that is called when the client disconnects from an MQTT broker.
    print("disconnecting reason  "  +str(rc))   #is used to print the reason for a client disconnecting from an MQTT broker. The return code indicates the reason for the disconnection.
    client.connected_flag=False                 #is used to set a flag indicating that the client is disconnected from an MQTT broker. This flag can be used to check if the client is disconnected or not.
    client.disconnect_flag=True                 #is used to set a flag indicating that the client is disconnected from an MQTT broker. This flag can be used to check if the client is disconnected or not.

def on_message(client, userdata, message):              #is a function definition. It is used to define a callback function that is called when the client receives a message from an MQTT broker.
    print("message received  ",str(message.payload))    #is used to print the payload of a message received from an MQTT broker. The payload contains the data that was sent in the message.
    print("message topic  ",str(message.topic))         #is used to print the topic of a message received from an MQTT broker. The topic indicates which topic the message was sent to.
    rawPayloadData= message.payload.decode('UTF-8')     #is used to decode the payload of a message received from an MQTT broker. The payload is decoded from its binary form into a string.
    topic = str(message.topic)                          #is used to convert the topic of a message received from an MQTT broker to a string. This is necessary in order to use the topic in string operations.
    print(topic)                                        #in ra bản tin topic nhận được
    if(topic=="mqtt/avirup171/edgeDevice"):             # is used to check if the topic of a message received from an MQTT broker is equal to a specific topic. If the topic matches, then the code inside the if statement will be executed.
        jsonData=json.dumps(rawPayloadData)             #is used to convert a string into a JSON object. This is necessary in order to use the data in JSON operations.
        response=requests.post(serverUrl,jsonData,headers=headers) #is used to send a POST request to a web server. The request contains the JSON data and the specified headers.
        responseData=response.json()                    #is used to convert the response from a web server into a JSON object. This is necessary in order to use the data in JSON operations.
        device_id=responseData["device_id"]             #is used to extract the device_id from the response data. The device_id is used to identify the device that sent the request.
        pubTopic=edgeDeviceReceiveTopicBase+device_id   #is used to construct a topic for publishing messages to an MQTT broker. The topic is constructed by combining the base topic and the device_id.
        client.publish(pubTopic,str(responseData))      #is used to publish a message to an MQTT broker. The message contains the response data from the web server.
        print(responseData)                             #in ra Data phản hồi


def init_mqtt(client,mqtt_host,mqtt_port):  #It is used to define a function that initializes an MQTT client and connects it to an MQTT broker.
    mqtt.Client.connected_flag=False #is used to set a flag indicating that the client is not connected to an MQTT broker. This flag can be used to check if the client is connected or not.

    client.on_connect = on_connect #is used to set a callback function that is called when the client connects to an MQTT broker. The callback function is defined by the on_connect function. 
    client.on_subscribe=on_subscribe #is used to set a callback function that is called when the client successfully subscribes to a topic on an MQTT broker. The callback function is defined by the on_subscribe function.
    client.on_message=on_message # is used to set a callback function that is called when the client receives a message from an MQTT broker. The callback function is defined by the on_message function.
    client.connect(mqtt_host, int(mqtt_port)) #is used to connect an MQTT client to an MQTT broker. The host and port of the broker are specified as parameters.

def handler(): #It is used to define a function that is called when the program is started. The function can be used to initialize the program and set up any necessary connections.
    mqtt_host="broker.hivemq.com"
    mqtt_port="1883"
    #Connection initiated
    init_mqtt(client,mqtt_host,mqtt_port) # is used to initialize an MQTT client and connect it to an MQTT broker. The host and port of the broker are specified as parameters.
    client.loop_forever() #is used to start an infinite loop that listens for messages from an MQTT broker. The loop will continue until the client is disconnected from the broker.

if __name__ == "__main__": #is used to check if the program is being run as the main program. If it is, then the code inside the if statement will be executed.
    handler() # is used to call the handler function when the program is started. The handler function can be used to initialize the program and set up any necessary connections.

