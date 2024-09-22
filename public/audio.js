const recordedAudio = document.getElementById('recordedAudio'); 

const record = document.getElementById('startButton');
const stop = document.getElementById('stopButton');

const upload = document.getElementById('fileUpload');
const send = document.getElementById('sendButton');
const summarize = document.getElementById('summaryButton');


// Disable stop button while not recording
stop.disabled = true;
summarize.disabled = true;
var apiUrl = "http://127.0.0.1:5000/upload"

// Main block for doing the audio recording
if (navigator.mediaDevices.getUserMedia) 
{
    console.log("The mediaDevices.getUserMedia() method is supported.");
    const constraints = { audio: true };
    let chunks = [];

    let onSuccess = function (stream) {
        const options = {
            audioBitsPerSecond: 16000 // 16kbps is the amt Gemini downsamples to
        }
        const mediaRecorder = new MediaRecorder(stream, options)
        // start recording
        record.onclick = function () {
            console.log("recorder started");
            navigator.mediaDevices.getUserMedia;
            mediaRecorder.start();
            stop.disabled = false;
            summarize.disabled = false;
            record.disabled = true;
        };

        // stop recording
        stop.onclick = function () {
            apiUrl = "http://127.0.0.1:5000/upload"
            
            stop.disabled = true;
            summarize.disabled = true;
            record.disabled = false;

            mediaRecorder.stop();
        };

        // stop recording 2
        summarize.onclick = function () {
            apiUrl = "http://127.0.0.1:5000/summarize"
            
            stop.disabled = true;
            summarize.disabled = true;
            record.disabled = false;

            mediaRecorder.stop();
        };

        var audioBlob; // variable to store recording or file upload
        mediaRecorder.onstop = function (e) {
            audioBlob = new Blob(chunks, { type: mediaRecorder.mimeType });
            chunks = [];

            const audioURL = window.URL.createObjectURL(audioBlob);
            recordedAudio.src = audioURL;
            recordedAudio.load();
            recordedAudio.play();
            console.log("recorder stopped");
        };
 
        upload.onchange = function (e) {
            audioBlob = e.target.files[0];
            recordedAudio.src = window.URL.createObjectURL(audioBlob);;
        }

        send.onclick = function () {
            // Prepare the fetch request
            const formData = new FormData();
            formData.append("audio", audioBlob, "recording");

            fetch(apiUrl, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log("Server response:", data);
                resultsTextarea.innerHTML=data.message;
            })
            .catch(error => {
                console.error("Error sending audio:", error);
            });
        }

        mediaRecorder.ondataavailable = function (e) {
            chunks.push(e.data);
        };
    };

    let onError = function (err) {
        console.log("The following error occured: " + err);
    };

    
    navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);
} 
else 
{
    console.log("MediaDevices.getUserMedia() not supported on your browser!");
}