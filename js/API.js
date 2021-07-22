let UUID = null;
let eventResponse = null;

async function generateUUId() {
    UUID = await (await fetch('/generateUUID')).text()
}

function initSSE() {
    const evtSource = new EventSource(`/stream/${UUID}`);
    evtSource.addEventListener("ping", function(event) {
        document.getElementById('textArea').value = JSON.parse(event.data).text;
    });
    return evtSource
}

function createEventListener() {
    const textArea = document.getElementById('textArea');

    function updateValue(e) {
        const data = {
            text: textArea.value,
            user: UUID
        }
        postData('/save', data)
    }

    textArea.addEventListener('keydown', updateValue);
}

function executionPress(){
    const button = document.getElementById('buttonClick')

        function exec(e){
            executePythonCode(document.getElementById('outputArea').value, document.getElementById('textArea').value)
        }

    button.addEventListener('click',exec)

}

function executePythonCode(responseArea, text) {
    const data = {
        text: text
    }
    responseArea = postData('/exec', data, 'yes')
}

async function postData(url = '', data = {}, compile) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *client
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    if(compile==='yes') {
        const text = await response.text()
        document.getElementById('outputArea').value = text
    }
}

generateUUId().then(function() {
    eventResponse = initSSE();
});

createEventListener();

executionPress();