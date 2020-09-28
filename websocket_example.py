#
# python websocket client example for subscribing to Orchstrator Notification Service
#
# Your use of this Software is pursuant to the Silver PEak Disclaimer - see the README file for this repository
#

import json
import websockets
import asyncio

async def alarm():
    # script input parameters - set these based on your needs
    #   
    #   url: URL or IP address of Orchestrator
    #   alarmkey: security key associated with websocket remote log receiver, configured to forward alarms
    #   logkey: security key associated with websocket remote log receiver, configured to forward audit log events
    #   alarmrid: remote log receiver id for alarm stream
    #   logrid: remote log receiver id for audit log stream
    #
    #   The websocket keys and remote log receiver ids can be retrieved from the
    #   Remote Log Receivers tab of Orchestrator.  Each webscoket can support
    #   at most one notification type - alarms or audit log.
    #
    #   For more documentation on websockets, see websocket-README file on SPOpenSource github
    
    # FQDN of Orchestrator (ie, URL without leading https://)
    url = "www.example.com" 

    # keys for alarm websocket and audit log websocket
    # the keys are passed by the client to Orch to validate the client request.
    alarmkey = "abc123key"
    logkey = "abc123key" 

    # remote log receiver IDs created by Orchestrator. These are positive integers.
    alarmrid = 1
    logrid = 2

    # json object for requesting active alarms
    # the alarm websocket is bidirectional and can accept requests - wee websocket-README for details
    active_alarms = {"action": "ACTIVE_ALARMS", "type": None, "data": None}

    # select whether you want to receive alarms or audit log events
    # based on selection, set the appropriate security key and remote log receiver id
    a = input("(0) alarm or (1) audit log, (q) to quit: ")
    if a not in ["0","1"]:
        return
    elif int(a) == 0:
        rid = alarmrid
        key = alarmkey
    else:
        rid = logrid
        key = logkey

    # input number of notifications to receive before exiting. For a real subscriber, this would really be a continuous loop
    # the sample code here will just receive x notifications 
    n = input("Number of notifications? ")

    # if this is an alarm websocket, ask user whether Orchestrator should send all currently active alarms
    if int(a) == 0:
        send_active_alarms = input("Send active alarms (y/n)? ")

    # connect to websocket        
    async with websockets.connect("wss://" + url + "/remoteLogWebSocket/" + str(rid) + "?key=" + key) as ws:
        # here's an example of how to send the request for all active alarms (assuming an alarm stream)
        if int(a) == 0 and send_active_alarms in ["Y","y"]:
            r = await ws.send( json.dumps(active_alarms))

        
        # receieve n messages on websocket 
        for i in range(0,int(n)):
            r = await ws.recv()
            print("message ({0}): {1}\n".format(i,r))
           
    try:
        ws.close()
    except:
        print("Exception raised on closing")
    
if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(alarm())
    except websockets.exceptions.ConnectionClosed as e:
        print("connection closed")
    except Exception as e2:
        print("other exception raised", e2.message)
