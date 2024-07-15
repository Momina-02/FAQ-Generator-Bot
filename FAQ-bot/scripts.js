document.getElementById('submitBtn').addEventListener('click', async () => {
    const query = document.getElementById('queryInput').value;
    const outputDiv = document.getElementById('output');
    
    if (query.trim() === '') {
        outputDiv.innerHTML = 'Please enter a query.';
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/api/query', {  // Ensure this URL matches your Flask backend URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });

        const data = await response.json();
        if (data.error) {
            outputDiv.innerHTML = 'Error: ' + data.error;
        } else {
            outputDiv.innerHTML = data.answer;
        }
    } catch (error) {
        outputDiv.innerHTML = 'Error: ' + error.message;
    }
});
