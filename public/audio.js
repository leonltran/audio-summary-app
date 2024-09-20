const record = document.getElementById('startButton');
const stop = document.getElementById('stopButton');
const recordedAudio = document.getElementById('recordedAudio');

// Disable stop button while not recording
stop.disabled = true;

// Main block for doing the audio recording
if (navigator.mediaDevices.getUserMedia) 
    {
    console.log("The mediaDevices.getUserMedia() method is supported.");

    const constraints = { audio: true };
    let chunks = [];

    let onSuccess = function (stream) {
        const mediaRecorder = new MediaRecorder(stream);

        // start recording
        record.onclick = function () {
            navigator.mediaDevices.getUserMedia;
            mediaRecorder.start();
            stop.disabled = false;
            record.disabled = true;
        };

        // stop recording
        stop.onclick = function () {
            mediaRecorder.stop();
            stop.disabled = true;
            record.disabled = false;
        };

        mediaRecorder.onstop = function (e) {
            console.log("Last data to read (after MediaRecorder.stop() called).");

            // create Blob using data
            const blob = new Blob(chunks, { type: mediaRecorder.mimeType });
            chunks = [];
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

    record.onclick = function () {
        // record.onclick gets overwritten once onSuccess fires
        navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);
    };
    
} 
else 
{
    console.log("MediaDevices.getUserMedia() not supported on your browser!");
}