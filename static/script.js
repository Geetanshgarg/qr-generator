document.getElementById('qr-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const data = document.getElementById('data').value;
    const filename = document.getElementById('filename').value;
    fetch('/api/generate_qr', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: data, filename: filename })
    })
    .then(response => response.json())
    .then(data => {
        if (data) {
            window.location.href = `/qr/${filename}.png`;
        } else {
            alert(data.error || 'An error occurred');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});