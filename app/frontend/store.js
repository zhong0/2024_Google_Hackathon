const clothestype_dropdown = document.getElementById("clothestype-dropdown");
const store_container = document.getElementById('store-container');
const choice_list = document.getElementById('choice-list');
const remove_button =  document.getElementById('remove-bt');
const modification_button =  document.getElementById('modification-bt');
const clothesDetail_input = document.getElementById('add-store-detail');
const favorite_button =  document.getElementById('favorite-bt');
const store_button =  document.getElementById('store-bt');

let price_input = document.getElementById('price-input');
let size_input = document.getElementById('size-input');
let brand_input = document.getElementById('brand-input');
let detail_input = document.getElementById('detail-input');

price_input.value = '10';
size_input.value = 'M';
brand_input.value = 'nike';
detail_input.value = 'This is a sports style shorts.';

// myUsername from localStorage; nowUsername from api
const myUsername = 'zhong0';
const nowUsername = 'zhong0';

let selectedImage = null;
let previousSelected = null;

let options = ["Top", "Bottom", "Shoes", "Clothes"];
let data = [
    { id: 1, filename: "../upload/zhong0/01.jpg", 'category': 'Bottom'},
    { id: 2, filename: "../upload/zhong0/02.jpg", 'category': 'Bottom'},
    { id: 3, filename: "../upload/zhong0/03.jpg", 'category': 'Bottom'},
    { id: 4, filename: "../upload/zhong0/04.jpg", 'category': 'Top'},
    { id: 5, filename: "../upload/zhong0/05.jpg", 'category': 'Bottom'}
];

function clotheChosen(imageList) {
    imageList.forEach((ele) => {
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
            if (nowUsername !== myUsername) {
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
            } else {
                if (selectedImage) {
                    selectedImage.classList.remove('selected');
                    document.querySelectorAll('.image-wrapper.clicked').forEach((image) => {
                        image.classList.remove('clicked');
                        image.classList.remove('hovered');
                    });
                    choice_list.style.display = 'none';
                    clothesDetail_input.style.display = 'none';
                }
                if (img === selectedImage) {
                    selectedImage = null;
                } else {
                    img.classList.add('selected');
                    selectedImage = img;
                    imageWrapper.classList.add('clicked');
                    choice_list.style.display = 'block';
                }
            }
            
        });
        // 將 input、label 和 img 元素添加到 imageWrapper 中
        imageWrapper.appendChild(img);
        // 將 imageWrapper 添加到父容器中
        store_container.appendChild(imageWrapper);
    })

}

clotheChosen(data);

options.forEach(option => {
    const optionElement = document.createElement("option");
    optionElement.text = option;
    optionElement.value = option;
    clothestype_dropdown.appendChild(optionElement);
});

clothestype_dropdown.addEventListener("change", function() {
    selectedValue = clothestype_dropdown.value;
    store_container.innerHTML = "";
    let filterImage = []
    if (selectedValue !== "") {
        filterImage = data.filter((ele) => (ele.category === selectedValue));
    } else {
        filterImage = data.filter((ele) => (!chosenList.includes(ele.id)));
    }
    clotheChosen(filterImage)
    
});

remove_button.addEventListener('click', () => {
    
});

modification_button.addEventListener('click', () => {
    if(clothesDetail_input.style.display === 'none') {
        clothesDetail_input.style.display = 'block';
    } else {
        clothesDetail_input.style.display === 'none'
    }
    
});

clothesDetail_input.addEventListener('click', () => {
    
});

favorite_button.addEventListener('click', () => {
    fetch('/favorite_set', { method: 'GET' })
    .then(response => {
        if (response.ok) {
            window.location.href = '/favorite_set';
        } else {
            console.error('Error:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

store_button.addEventListener('click', () => {
    fetch('/store', { method: 'GET' })
    .then(response => {
        if (response.ok) {
            window.location.href = '/store';
        } else {
            console.error('Error:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});