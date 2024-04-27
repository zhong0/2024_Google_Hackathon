const clothestype_dropdown = document.getElementById("clothestype-dropdown");
const closet_container = document.getElementById('closet_container');
const choice_list = document.getElementById('choice-list');
const delete_button =  document.getElementById('delete-bt');
const addStore_button =  document.getElementById('add-to-store-bt');
const clothesDetail_input = document.getElementById('add-store-detail');

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
        });
    
        // 將 input、label 和 img 元素添加到 imageWrapper 中
        imageWrapper.appendChild(img);
        
        // 將 imageWrapper 添加到父容器中
        closet_container.appendChild(imageWrapper);
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
    closet_container.innerHTML = "";
    let filterImage = []
    if (selectedValue !== "") {
        filterImage = data.filter((ele) => (ele.category === selectedValue));
    } else {
        filterImage = data.filter((ele) => (!chosenList.includes(ele.id)));
    }
    clotheChosen(filterImage)
    
});

delete_button.addEventListener('click', () => {
    
});

addStore_button.addEventListener('click', () => {
    if(clothesDetail_input.style.display === 'none') {
        clothesDetail_input.style.display = 'block';
    } else {
        clothesDetail_input.style.display === 'none'
    }
    
});

clothesDetail_input.addEventListener('click', () => {
    
});