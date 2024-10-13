function analyze(fileName) {
    fetch('/analyze/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ file_name: fileName }),
    })
    .then(response => response.json())
    .then(data => {
        alert(`Analysis started for: ${fileName}`);
        console.log(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function preprocessing() {
    fetch('/preprocessing/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sound_level: 10, frequency: 20 })
    })
    .then(response => response.json())
    .then(() => {
        alert(`Processing started!`);
    })
    .catch((error) => {
        console.error('Error: ', error)
    })
}