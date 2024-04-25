const fittingNow_button = document.getElementById('fitting-bt');
const piece_container = document.getElementById('homepage-piece-gallery');
const explore_button = document.querySelector('.explore-button-container');

const data = [
    {id: 1, filename: 'zhong0/23.jpg'},
    {id: 2, filename: 'zhong0/22.jpg'},
    {id: 3, filename: 'zhong0/21.jpg'},
];

console.log('joo')
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