const description_container = document.getElementById('set-image');
const piece_container = document.getElementById('piece-image');
const tag_container =  document.querySelector('.explore-set-tag-row');
const text_container = document.getElementById('explore-set-description-text');
const like_bt = document.getElementById('like-bt');
const like_label = document.getElementById('like-label');

const data = {
    filename: ['zhong0/02.jpg', 'zhong0/04.jpg'],
    style: ['casuel', 'simple'],
    description:'this is a simple style clothes.'
};

const pieceRecommend = ['zhong0/12.jpg', 'zhong0/13.jpg'];

text_container.textContent = data.description;

like_bt.addEventListener('change', function() {
    if (this.checked) {
        like_label.style.backgroundImage = "url('../resource/liked_bt.png')";
      } else {
        like_label.style.backgroundImage = "url('../resource/like_bt.png')";
      }
});

data.style.forEach((ele) => {
    const tag = document.createElement('div');
    tag.classList.add('explore-set-tag');
    tag.textContent = ele;
    tag_container.appendChild(tag);
});

data.filename.forEach((ele)=> {
  const imageWrapper = document.createElement('div');
  imageWrapper.classList.add('image-wrapper');

  // 創建 input 元素
  const toggle = document.createElement('input');
  toggle.setAttribute('type', 'checkbox');
  toggle.id = 'pin-bt-' + ele; // 每個 input 元素的 id 需要唯一
  toggle.classList.add('pin-toggle-btn');

  // 創建 label 元素
  const label = document.createElement('label');
  label.setAttribute('for', 'pin-bt-' + ele); // 將 label 連接到對應的 input 元素
  label.classList.add('pin-toggle-label');

  // 創建 img 元素
  const img = document.createElement('img');
  img.src = `../upload/${ele}`; // 圖片路徑根據索引 i 設置
  img.alt = 'Image ' + ele;

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
  imageWrapper.appendChild(toggle);
  imageWrapper.appendChild(label);
  imageWrapper.appendChild(img);

  // 將 imageWrapper 添加到父容器中
  description_container.appendChild(imageWrapper);
});

pieceRecommend.forEach((ele) => {
  const imageWrapper = document.createElement('div');
  imageWrapper.classList.add('image-wrapper');

  const img = document.createElement('img');
  img.src = `../upload/${ele}`; // 圖片路徑根據索引 i 設置
  img.alt = 'Image ' + ele;

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

  imageWrapper.appendChild(img);
  piece_container.appendChild(imageWrapper);
});