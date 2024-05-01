const clothestype_dropdown = document.getElementById("clothestype-dropdown");
const closet_container = document.getElementById('closet_container');
const choice_list = document.getElementById('choice-list');
const delete_button =  document.getElementById('delete-bt');
const addStore_button =  document.getElementById('add-to-store-bt');
const clothesDetail_container = document.getElementById('add-store-detail');
const favorite_button =  document.getElementById('favorite-bt');
const store_button =  document.getElementById('store-bt');
const username_text =  document.getElementById('username-text');
const price_input = document.getElementById('price-input');
const size_input = document.getElementById('size-input');
const brand_input = document.getElementById('brand-input');
const details_input = document.getElementById('detail-input');
const sell_button = document.getElementById('add-to-sell');
const doublecheck_window_container = document.getElementById('doublecheck-window-container');

let username = '';
const loading_container = document.getElementById('loading');

let selectedImage = null;
let previousSelected = null;
let options = [];
let imageListData = [];
doublecheck_window_container.style.display = 'none';

// page init - get all clothes
document.addEventListener('DOMContentLoaded', function() {
    console.log(localStorage.getItem('username'))
    username = localStorage.getItem('username');
    username_text.textContent = username;
    getAllClothes();
});

function createInitOptions() {
    const option = document.createElement('option');
    option.value = '';
    option.text = 'Please select an option';
    option.selected = true;

    clothestype_dropdown.appendChild(option);
}

function getAllClothes() {
    loading_container.style.display = 'flex';
    const form_data = new FormData();
    form_data.append('username',username);

    const request_options = {
        method:'POST',
        body:form_data
    }
    
    fetch('/clothes/file-path-group-by-category', request_options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            let idex = 1;
            let file_path = '../upload/';

            // set init
            imageListData = [];
            options = [];
            clothestype_dropdown.innerHTML = ''; 
            closet_container.innerHTML = "";
            createInitOptions();

            // set imageListData
            for(let category in data.file_path){
                options.push(category);
                let filenames = data.file_path[category];
                filenames.forEach( (filename) =>{
                    imageListData.push({ id: idex, filename: file_path+filename, chosen: false, category: category});
                    idex += 1;
                });
            }
            clotheChosen(imageListData);
            //set dropdown by options
            options.forEach(option => {
                const optionElement = document.createElement("option");
                optionElement.text = option;
                optionElement.value = option;
                clothestype_dropdown.appendChild(optionElement);
            });
            loading_container.style.display = 'none';
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
}

// choose a clothe
function clotheChosen(imageList) {
    imageList.forEach((ele) => {
        const imageWrapper = document.createElement('div');
        imageWrapper.classList.add('image-wrapper');
        // 創建 img 元素
        const img = document.createElement('img');
        img.src = ele.filename; // 圖片路徑根據索引 i 設置
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
                clothesDetail_container.style.display = 'none';
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
    
        imageWrapper.appendChild(img);
        closet_container.appendChild(imageWrapper);
    })

}

// dropdown change
clothestype_dropdown.addEventListener("change", function() {
    selectedValue = clothestype_dropdown.value;
    choice_list.style.display = 'none';
    clothesDetail_container.style.display = 'none';
    closet_container.innerHTML = "";
    let filterImage = [];
    if (selectedValue !== "") {
        filterImage = imageListData.filter((ele) => (ele.category === selectedValue));
    } else {
        filterImage = imageListData;
    }
    clotheChosen(filterImage)
    
});

function doublcheck_window(fucntion_do){
    const alertBox = document.createElement('div');
    alertBox.textContent = 'Delete is forever';
    alertBox.id = 'doublecheck-window';
    alertBox.class = 'doublecheck-window';

    const yes_button = document.createElement('img');
    yes_button.src = '../resource/yes_bt.png';
    yes_button.style.marginRight = '10px';
    yes_button.addEventListener('click', function(){
        doublecheck_window_container.style.display = 'none';
        fucntion_do();
        doublecheck_window_container.removeChild(alertBox);
        console.log('yes');
    });


    const no_button = document.createElement('img');
    no_button.src = '../resource/no_bt.png';
    no_button.addEventListener('click', function(){
        doublecheck_window_container.style.display = 'none';
        doublecheck_window_container.removeChild(alertBox);
        console.log('no');
    });

    alertBox.appendChild(yes_button);
    alertBox.appendChild(no_button);

    //document.body.appendChild(alertBox);
    doublecheck_window_container.appendChild(alertBox);
    
}

function remove_from_closet(){
    
    console.log('removeing');
    const filename = `${username}/${selectedImage.src.split("/").slice(-1)[0]}`;
    const form_data = new FormData();
    
    form_data.append('username',username);
    form_data.append('filename',filename);

    const request_options = {
        method:'POST',
        body:form_data
    }
    
    fetch('/clothes/remove-clothes-from-wardrobe', request_options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            choice_list.style.display = 'none';
            clothesDetail_container.style.display = 'none';
            getAllClothes();
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
}

// remove from closet
delete_button.addEventListener('click', () => {
    
    if(doublecheck_window_container.children.length === 0){
        console.log(doublecheck_window_container.children.length);
        doublecheck_window_container.style.display = 'block';
        doublcheck_window(remove_from_closet);
    }
    
});

// add-to-store button
addStore_button.addEventListener('click', () => {
    if(clothesDetail_container.style.display === 'none') {
        clothesDetail_container.style.display = 'block';
    } else {
        clothesDetail_container.style.display === 'none'
    }
    
});

// sell
sell_button.addEventListener('click', () => {
    const price =  parseFloat(price_input.value);
    const size = size_input.value;
    const brand = brand_input.value;
    const details = details_input.value;

    const payload_data = {
        username: username,
        filename: `${username}/${selectedImage.src.split("/").slice(-1)[0]}`,
        size: size,
        brand: brand,
        owner_description: details,
        price: price,
    }

    const request_options = {
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload_data)
    }

    fetch('/shop/clothes-on-sale', request_options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            choice_list.style.display = 'none';
            clothesDetail_container.style.display = 'none';
            getAllClothes();
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });

});

// go to favorite set page
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

// go to store page
store_button.addEventListener('click', () => {
    localStorage.setItem('search_username', username);
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