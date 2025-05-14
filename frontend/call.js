const endCallButton = document.getElementById('endCall');
const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');
const startCallButtons = document.querySelectorAll('.start-call-btn');

let localStream;
let peerConnection;
let selectedDoctor = null;

startCallButtons.forEach(button => {
    button.addEventListener('click', async () => {
        selectedDoctor = button.getAttribute('data-doctor');
        console.log(`Starting call with ${selectedDoctor}...`);
        await startCall();
    });
});

endCallButton.addEventListener('click', endCall);

async function startCall() {
    try {
        // Request access to video and audio from the user's device
        localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        localVideo.srcObject = localStream;

        // Initialize the peer connection for WebRTC
        peerConnection = new RTCPeerConnection();

        // Add local tracks (audio/video) to the peer connection
        localStream.getTracks().forEach(track => {
            peerConnection.addTrack(track, localStream);
        });

        // Set up remote stream when it arrives
        peerConnection.ontrack = event => {
            remoteVideo.srcObject = event.streams[0];
        };

        // Handle ICE candidates (network traversal)
        peerConnection.onicecandidate = function(event) {
            if (event.candidate) {
                console.log("New ICE candidate:", event.candidate);
            }
        };

        // Create and send an offer (you would normally signal to the other peer here)
        const offer = await peerConnection.createOffer();
        await peerConnection.setLocalDescription(offer);
        console.log(`Offer created for ${selectedDoctor}:`, offer);

        // In a real application, you would send the offer to the remote doctor through signaling.

        // Disable the start button and enable the end call button
        endCallButton.disabled = false;

        console.log("Call started with doctor:", selectedDoctor);

    } catch (error) {
        console.error('Error starting call:', error);
    }
}

function endCall() {
    if (localStream) {
        localStream.getTracks().forEach(track => track.stop());
    }
    if (peerConnection) {
        peerConnection.close();
    }
    localVideo.srcObject = null;
    remoteVideo.srcObject = null;
    endCallButton.disabled = true;
    console.log("Call ended.");
}
