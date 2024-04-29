const clothestype_dropdown = document.getElementById("clothestype-dropdown");
const store_container = document.getElementById('store-container');
const choice_list = document.getElementById('choice-list');
const remove_button =  document.getElementById('remove-bt');
const modification_button =  document.getElementById('modification-bt');
const clothesDetail_container = document.getElementById('add-store-detail');
const favorite_button =  document.getElementById('favorite-bt');
const submit_button =  document.getElementById('submit-bt');
const searched_username_text =  document.getElementById('searched-username-text');

const username_input =  document.getElementById('username-input');
const search_button =  document.getElementById('search-bt');

let price_input = document.getElementById('price-input');
let size_input = document.getElementById('size-input');
let brand_input = document.getElementById('brand-input');
let detail_input = document.getElementById('detail-input');

const loading_container = document.getElementById('loading');

// myUsername from localStorage; nowUsername from api
const myUsername = 'zhong0';
let searchUsername = '';

let selectedImage = null;
let previousSelected = null;

let imageListData = [];
let options = [];

// init dropdown options
function createInitOptions() {
    const option = document.createElement('option');
    option.value = '';
    option.text = 'Please select an option';
    option.selected = true;

    clothestype_dropdown.appendChild(option);
}

// get original sale information of clothe
function getSaleInfo() {
    loading_container.style.display = 'flex';
    const form_data = new FormData();
    const filename = `${myUsername}/${selectedImage.src.split("/").slice(-1)[0]}`;
    form_data.append('username', searchUsername);
    form_data.append('filename', filename);

    const request_options = {
        method:'POST',
        body:form_data
    }
    
    fetch('/shop/clothes-sale-info-by-filename', request_options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            price_input.value = data.sale_info.price;
            size_input.value = data.sale_info.size;
            brand_input.value = data.sale_info.brand;
            detail_input.value = data.sale_info.owner_description;
            loading_container.style.display = 'none';
            
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });

}

// get all clothes on sale
function getSellClothes() {
    loading_container.style.display = 'flex';
    const form_data = new FormData();
    form_data.append('username', searchUsername);

    const request_options = {
        method:'POST',
        body:form_data
    }
    
    fetch('/shop/file-path-group-by-category', request_options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if(!data) {
                console.log(`No ${searchUsername} username`);
            } else {
                let idex = 1;
                let file_path = '../upload/';

                // set init
                imageListData = [];
                options = [];
                clothestype_dropdown.innerHTML = ""; 
                store_container.innerHTML = "";
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
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
}

// get selected clothe
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
            if (searchUsername !== myUsername) {
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
            }
            
        });
        // 將 input、label 和 img 元素添加到 imageWrapper 中
        imageWrapper.appendChild(img);
        // 將 imageWrapper 添加到父容器中
        store_container.appendChild(imageWrapper);
    })

}

// dropdown change
clothestype_dropdown.addEventListener("change", function() {
    selectedValue = clothestype_dropdown.value;
    choice_list.style.display = 'none';
    clothesDetail_container.style.display = 'none';
    store_container.innerHTML = "";
    let filterImage = [];
    if (selectedValue !== "") {
        filterImage = imageListData.filter((ele) => (ele.category === selectedValue));
    } else {
        filterImage = imageListData;
    }
    clotheChosen(filterImage)
    
});

// remove from sale list
remove_button.addEventListener('click', () => {
    const filename = `${myUsername}/${selectedImage.src.split("/").slice(-1)[0]}`;
    const form_data = new FormData();
    
    form_data.append('username',myUsername);
    form_data.append('filename',filename);

    const request_options = {
        method:'POST',
        body:form_data
    }
    
    fetch('/shop/remove-clothes-from-shop', request_options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            choice_list.style.display = 'none';
            clothesDetail_container.style.display = 'none';
            getSellClothes(myUsername);
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
    
});

// expect to modifying
modification_button.addEventListener('click', () => {
    if(clothesDetail_container.style.display === 'none') {
        clothesDetail_container.style.display = 'block';
    } else {
        clothesDetail_container.style.display === 'none'
    }
    getSaleInfo();
    
});

submit_button.addEventListener('click', () => {
    loading_container.style.display = 'flex';
    const price =  parseFloat(price_input.value);
    const size = size_input.value;
    const brand = brand_input.value;
    const details = detail_input.value;

    const payload_data = {
        username: myUsername,
        filename: `${myUsername}/${selectedImage.src.split("/").slice(-1)[0]}`,
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

    fetch('/shop/update-sale-info', request_options)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        choice_list.style.display = 'none';
        clothesDetail_container.style.display = 'none';
        loading_container.style.display = 'none';
        getSellClothes();
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
   
    
});

search_button.addEventListener('click', () => {
    searchUsername = username_input.value;
    if(searchUsername) {
        choice_list.style.display = 'none';
        clothesDetail_container.style.display = 'none';
        searched_username_text.textContent = searchUsername;
        getSellClothes();
        username_input.value = '';
    }
    
});

// page init - get all clothes
document.addEventListener('DOMContentLoaded', function() {
    if (searchUsername == '') {
        searchUsername = myUsername;
    }
    getSellClothes();
});