//
// IMPORTANT
//
// Your use of this Software is pursuant to the Silver Peak Disclaimer - see the README file for this repository 
//
//

const WebSocket = require('ws');
process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0;
 
/**
 * Update these variables here for your Orchestrator environment
 *   ipOrDNS: ip address or FQDN of the target Orchestrator
 *   receiverId: id of websocket remote log receiver created on Orchestrator (integer)
 *   key: key that Orchestrator generates after websocket server is configured
 */
var ipOrDNS = "localhost";
var receiverId = 1;
var key = "";
 
 //modify ipOrDNS, receiverId and key for your test
const ws = new WebSocket(`wss://${ipOrDNS}/remoteLogWebSocket/${receiverId}`, null, {
    headers: {
        "X-Auth-Token": key
    }
});
 
 
ws.on('open', function open() { });
 
ws.on('message', function incoming(data) {
    console.log("WS1 GOT MESSAGE:");
    console.log(JSON.parse(data));
});

function requestActiveAlarm() {
    // The client can request current active alarms over the websocket
    if (ws != null) {
        var req = {
            action: "ACTIVE_ALARMS"
        }
        ws.send(JSON.stringify(req));
        console.log(`Send request to ws, ${JSON.stringify(req)}`);
    }
}
 
function requestAlarmByIds() {
    // The client can request specific alarms or audit log notifications based on sequence IDs
    // ids is a list of integers or integer ranges identifying the requested sequenceIds 
    var ids = ["2", "3", "4-6"];
    if (ws != null) {
        var req = {
            action: "RESUBMISSION",
            type: "SEQUENCE_ID",
            data: JSON.stringify(ids)
        }
        ws.send(JSON.stringify(req));
        console.log(`Send request to ws, ${JSON.stringify(req)}`);
     }
}
