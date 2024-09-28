document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', function() {
        const filename = this.getAttribute('data-filename');
        fetch('/api/delete_qr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename: filename })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                this.parentElement.remove();
            } else {
                alert(data.error || 'An error occurred');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

document.getElementById('back-btn').addEventListener('click', function() {
    window.location.href = '/';
});