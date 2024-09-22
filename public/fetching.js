const getButton = document.getElementById('getButton');
const resultsTextarea = document.getElementById('dbContent');

getButton.onclick = function () {
    fetch("http://127.0.0.1:5000/contacts")
    .then(response => response.json())
    .then(data => {
        console.log("Server response:", data);
        var pretty = JSON.stringify(data, undefined, 4);
        resultsTextarea.innerHTML = pretty;
    })
    .catch(error => {
        console.error("Error getting database data:", error);
    });
};