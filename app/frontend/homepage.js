const fittingNow_button = document.getElementById('fitting-bt');
const upload_button = document.getElementById('upload-bt');
const upload_file_input = document.getElementById('input_file');
const piece_container = document.getElementById('homepage-piece-gallery');
const explore_button = document.querySelector('.explore-button-container');
const closet_button = document.getElementById('selfclothes-bt');

const data = [
    {id: 1, filename: 'zhong0/23.jpg'},
    {id: 2, filename: 'zhong0/22.jpg'},
    {id: 3, filename: 'zhong0/21.jpg'},
];
console.log('username:', localStorage.getItem('username'));
//localStorage.removeItem('username');

function showMessage(message) {
    const alertBox = document.createElement('div');
    alertBox.textContent = message;
    alertBox.style.backgroundColor = '#000000';
    alertBox.style.color = 'white';
    alertBox.style.padding = '10px 20px';
    alertBox.style.borderRadius = '10px';
    alertBox.style.position = 'fixed';
    alertBox.style.top = '50%';
    alertBox.style.left = '50%';
    alertBox.style.transform = 'translate(-50%, -50%)';
    alertBox.style.zIndex = '9999';

    document.body.appendChild(alertBox);

    setTimeout(function() {
        document.body.removeChild(alertBox);
    }, 2000); // 2秒后移除提示框
}

data.forEach((ele) => {
    const imageWrapper = document.createElement('div');
    imageWrapper.classList.add('image-wrapper');
    // 創建 img 元素
    const img = document.createElement('img');
    img.src = `../upload/${ele.filename}`; // 圖片路徑根據索引 i 設置
    img.id = ele.id;
    img.alt = 'Image ' + ele.id;

    // 添加 hover 效果
    img.addEventListener('mouseover', function() {
        imageWrapper.classList.add('hovered');
    });
    img.addEventListener('mouseout', function() {
        imageWrapper.classList.remove('hovered');
    });

    img.addEventListener('click', function() {
        fetch('/piece_info', { method: 'GET' })
        .then(response => {
            if (response.ok) {
                window.location.href = '/piece_info';
            } else {
                console.error('Error:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // 將 input、label 和 img 元素添加到 imageWrapper 中
    imageWrapper.appendChild(img);

    // 將 imageWrapper 添加到父容器中
    piece_container.appendChild(imageWrapper);
})

fittingNow_button.addEventListener('click', () => {
    fetch('/fitting_style', { method: 'GET' })
        .then(response => {
            if (response.ok) {
                if(localStorage.getItem('username')){
                    window.location.href = '/fitting_style';
                } else {
                    window.location.href = '/login';
                }
                
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
    if(localStorage.getItem('username')){
        upload_file_input.click();
    } else {
        window.location.href = '/login';
    }
});

closet_button.addEventListener('click', () => {
    fetch('/closet', { method: 'GET' })
        .then(response => {
            if (response.ok) {
                window.location.href = '/closet';
            } else {
                console.error('Error:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
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