const record = document.getElementById('startButton');
const summarize = document.getElementById('summaryButton');
const stop = document.getElementById('stopButton');
const recordedAudio = document.getElementById('recordedAudio');

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

        mediaRecorder.onstop = function (e) {
            // create Blob using data
            
            const blob = new Blob(chunks, { type: mediaRecorder.mimeType });
            chunks = [];

            // Prepare the fetch request
            const formData = new FormData();
            formData.append("audio", blob, "recording");

            fetch(apiUrl, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log("Server response:", data);
                // Handle server response (e.g., success message)
            })
            .catch(error => {
                console.error("Error sending audio:", error);
            });

            const audioURL = window.URL.createObjectURL(blob);
            recordedAudio.src = audioURL;
            recordedAudio.load();
            recordedAudio.play();
            console.log("recorder stopped");
        };

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