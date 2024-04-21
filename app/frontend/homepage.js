const nextPageButton = document.getElementById('fitting-bt');

nextPageButton.addEventListener('click', () => {
    fetch('/fitting_style', { method: 'GET' })
        .then(response => {
            if (response.ok) {
                window.location.href = '/fitting_style';
            } else {
                console.error('Error:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});