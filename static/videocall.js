var mediaConstraints = {
    audio: true,            // We want an audio track
    video: {
      aspectRatio: {
        ideal: 1.333333     // 3:2 aspect is preferred
      }
    }
  };
var myUsername = null;
var targetUsername = null;      // To store username of other peer
var myPeerConnection = null;    // RTCPeerConnection
var transceiver = null;         // RTCRtpTransceiver
var webcamStream = null;   
var caller_name
function sendToServer(msg) {
  msg.type='videocall'
    msg.dname=userid
    msg.name='user_'+userid
    msg.username='user_'+caller_name
    
    socket.send(JSON.stringify(msg));
}
function call(){
    caller_name=user
    
    $('#wrapper').hide()
    document.getElementById("video-call-div")
.style.display = "inline"
    
    
sendToServer({'vtype':'call'})

}
function log(text) {
  var time = new Date();

  console.log("[" + time.toLocaleTimeString() + "] " + text);
}
function log_error(text) {
  var time = new Date();

  console.trace("[" + time.toLocaleTimeString() + "] " + text);
}
function handlevidata(msg){
    
    switch (msg.vtype){
        case 'call':
            caller_name=msg.dname
            document.getElementById('call').style.display='block';
            document.getElementById('wrapper').style.display='none';
            break
        case 'accepted':
            accep()
            break
        case "video-offer":
        // Invitation and offer to chat
        handleVideoOfferMsg(msg);
        
        break;

      case "video-answer": 
      // Callee has answered our offer
        handleVideoAnswerMsg(msg);
      
        break;

      case "new-ice-candidate": // A new ICE candidate has been received
     
        handleNewICECandidateMsg(msg);
      
        break;

      case "hang-up": // The other peer has hung up the call
     
        handleHangUpMsg(msg);
      
        break;
        case "rej":
          closeVideoCall()
          alert('call rejected !')
          break
    }
}

async function accepted(){
    createPeerConnection()
    try {
      webcamStream = await navigator.mediaDevices.getUserMedia(mediaConstraints);
      document.getElementById("local_video").srcObject = webcamStream;
    } catch(err) {
      handleGetUserMediaError(err);
      return;
    }

    

    try {
      webcamStream.getTracks().forEach(
        transceiver = track => myPeerConnection.addTransceiver(track, {streams: [webcamStream]})
      );
    } catch(err) {
      handleGetUserMediaError(err);
    }
    document.getElementById("call").style.display = "none"
    document.getElementById("video-call-div").style.display = "inline"
    sendToServer({'vtype':'accepted'})
}
async function createPeerConnection() {


  

  myPeerConnection = new RTCPeerConnection({
    iceServers: [
            {
                "urls": ["stun:stun.l.google.com:19302", 
                "stun:stun1.l.google.com:19302", 
                "stun:stun2.l.google.com:19302"]
            }
        ]
  });
  myPeerConnection.onicecandidate = handleICECandidateEvent;
  myPeerConnection.oniceconnectionstatechange = handleICEConnectionStateChangeEvent;
  myPeerConnection.onicegatheringstatechange = handleICEGatheringStateChangeEvent;
  myPeerConnection.onsignalingstatechange = handleSignalingStateChangeEvent;
  myPeerConnection.onnegotiationneeded = handleNegotiationNeededEvent;
  myPeerConnection.ontrack = handleTrackEvent;
}
async function handleNegotiationNeededEvent() {


  try {
    
    const offer = await myPeerConnection.createOffer();

    // If the connection hasn't yet achieved the "stable" state,
    // return to the caller. Another negotiationneeded event
    // will be fired when the state stabilizes.

    if (myPeerConnection.signalingState != "stable") {
    
      return;
    }

    // Establish the offer as the local peer's current
    // description.

    
    await myPeerConnection.setLocalDescription(offer);

    // Send the offer to the remote peer.

    
    sendToServer({
     vtype: "video-offer",
      sdp: myPeerConnection.localDescription
    });
  } catch(err) {
   
    reportError(err);
  };
}
function handleTrackEvent(event) {

  document.getElementById("received_video").srcObject = event.streams[0];
 
}
function handleICECandidateEvent(event) {
  if (event.candidate) {
    

    sendToServer({
      type: "new-ice-candidate",
      candidate: event.candidate
    });
  }
}
function handleICEConnectionStateChangeEvent(event) {
 

  switch(myPeerConnection.iceConnectionState) {
    case "closed":
    case "failed":
    case "disconnected":
      closeVideoCall();
      break;
  }
}
function handleSignalingStateChangeEvent(event) {
 
  switch(myPeerConnection.signalingState) {
    case "closed":
      closeVideoCall();
      break;
  }
}
function handleICEGatheringStateChangeEvent(event) {
 
}
function closeVideoCall() {
  var localVideo = document.getElementById("local_video");

  

  // Close the RTCPeerConnection

  if (myPeerConnection) {
   

    // Disconnect all our event listeners; we don't want stray events
    // to interfere with the hangup while it's ongoing.

    myPeerConnection.ontrack = null;
    myPeerConnection.onnicecandidate = null;
    myPeerConnection.oniceconnectionstatechange = null;
    myPeerConnection.onsignalingstatechange = null;
    myPeerConnection.onicegatheringstatechange = null;
    myPeerConnection.onnotificationneeded = null;

    // Stop all transceivers on the connection

    myPeerConnection.getTransceivers().forEach(transceiver => {
      transceiver.stop();
    });

    // Stop the webcam preview as well by pausing the <video>
    // element, then stopping each of the getUserMedia() tracks
    // on it.

    if (localVideo.srcObject) {
      localVideo.pause();
      localVideo.srcObject.getTracks().forEach(track => {
        track.stop();
      });
    }

    // Close the peer connection

    myPeerConnection.close();
    myPeerConnection = null;
    webcamStream = null;
  }

  // Disable the hangup button


 
  document.getElementById('video-call-div').style.display='none'
document.getElementById('wrapper').style.display='block'
}



// Handle the "hang-up" message, which is sent if the other peer
// has hung up the call or otherwise disconnected.

function handleHangUpMsg(msg) {


  closeVideoCall();
}
function rec(){
  sendToServer({'vtype':'rej'})
  document.getElementById('call').style.display='none'
  document.getElementById('wrapper').style.display='block'
}

// Hang up the call by closing our end of the connection, then
// sending a "hang-up" message to the other peer (keep in mind that
// the signaling is done on a different connection). This notifies
// the other peer that the connection should be terminated and the UI
// returned to the "no call in progress" state.

function hangUpCall() {
  closeVideoCall();

  sendToServer({
    
    vtype: "hang-up"
  });
}

async function handleVideoOfferMsg(msg) {


  // If we're not already connected, create an RTCPeerConnection
  // to be linked to the caller.


  if (!myPeerConnection) {
    createPeerConnection();
  }

  // We need to set the remote description to the received SDP offer
  // so that our local WebRTC layer knows how to talk to the caller.

  var desc = new RTCSessionDescription(msg.sdp);

  // If the connection isn't stable yet, wait for it...

  if (myPeerConnection.signalingState != "stable") {
  

    // Set the local and remove descriptions for rollback; don't proceed
    // until both return.
    await Promise.all([
      myPeerConnection.setLocalDescription({type: "rollback"}),
      myPeerConnection.setRemoteDescription(desc)
    ]);
    return;
  } else {
 
    await myPeerConnection.setRemoteDescription(desc);
  }

  // Get the webcam stream if we don't already have it

  if (!webcamStream) {
    try {
      webcamStream = await navigator.mediaDevices.getUserMedia(mediaConstraints);
    } catch(err) {
      handleGetUserMediaError(err);
      return;
    }

    document.getElementById("local_video").srcObject = webcamStream;

    // Add the camera stream to the RTCPeerConnection

    try {
      webcamStream.getTracks().forEach(
        transceiver = track => myPeerConnection.addTransceiver(track, {streams: [webcamStream]})
      );
    } catch(err) {
      handleGetUserMediaError(err);
    }
  }

  

  await myPeerConnection.setLocalDescription(await myPeerConnection.createAnswer());

  sendToServer({
   
    vtype: "video-answer",
    sdp: myPeerConnection.localDescription
  });
}

// Responds to the "video-answer" message sent to the caller
// once the callee has decided to accept our request to talk.

async function handleVideoAnswerMsg(msg) {
  

  // Configure the remote description, which is the SDP payload
  // in our "video-answer" message.

  var desc = new RTCSessionDescription(msg.sdp);
  await myPeerConnection.setRemoteDescription(desc).catch(reportError);
}

// A new ICE candidate has been received from the other peer. Call
// RTCPeerConnection.addIceCandidate() to send it along to the
// local ICE framework.

async function handleNewICECandidateMsg(msg) {
  var candidate = new RTCIceCandidate(msg.candidate);

  
  try {
    await myPeerConnection.addIceCandidate(candidate)
  } catch(err) {
    reportError(err);
  }
}


async function accep(){
    createPeerConnection();

    
    try {
      webcamStream = await navigator.mediaDevices.getUserMedia(mediaConstraints);
      document.getElementById("local_video").srcObject = webcamStream;
    } catch(err) {
      handleGetUserMediaError(err);
      return;
    }

    

    try {
      webcamStream.getTracks().forEach(
        transceiver = track => myPeerConnection.addTransceiver(track, {streams: [webcamStream]})
      );
    } catch(err) {
      handleGetUserMediaError(err);
    }
  }

function handleGetUserMediaError(e) {
 
  switch(e.name) {
    case "NotFoundError":
      alert("Unable to open your call because no camera and/or microphone" +
            "were found.");
      break;
    case "SecurityError":
    case "PermissionDeniedError":
     
      break;
    default:
      alert("Error opening your camera and/or microphone: " + e.message);
      break;
  }


  closeVideoCall();
}


function reportError(errMessage) {

}
    
let isAudio=true
function muteAudio() {
    var webcamStream = document.getElementById("local_video");
isAudio = !isAudio
localVideo.getAudioTracks()[0].enabled = isAudio
}
let isVideo = true
function muteVideo() {
    var localVideo = document.getElementById("local_video");
isVideo = !isVideo
webcamStream.getVideoTracks()[0].enabled = isVideo
}