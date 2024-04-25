const fittingNow_button = document.getElementById('fitting-bt');
const upload_button = document.getElementById('upload-bt');
const upload_file_input = document.getElementById('input_file');
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

upload_button.addEventListener('click', () => {

    upload_file_input.click();

    /*fetch('/upload/upload-images', { method: 'POST' })
        .then(response => {
            if (response.ok) {
                window.location.href = '/fitting_style';
            } else {
                console.error('Error:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });*/
});

upload_file_input.addEventListener('change', async() => {
    const selectedFiles = upload_file_input.files;
    var formData = new FormData();

    for (let i = 0; i < selectedFiles.length; i++) {
        formData.append('files', selectedFiles[i]);
    }
    //username need to be replaced by real data
    formData.append('username', 'chipi_js');
    
    const requestOptions = {
        method: 'POST',
        body: formData
    };
    
    fetch('/upload/upload-images', requestOptions)
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