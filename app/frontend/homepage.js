const fittingNow_button = document.getElementById('fitting-bt');
const explore_button = document.querySelector('.explore-button-container');
fittingNow_button.addEventListener('click', () => {
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

explore_button.addEventListener('click', () => {
    fetch('/explore', { method: 'GET' })
        .then(response => {
            if (response.ok) {
                window.location.href = '/explore';
            } else {
                console.error('Error:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});