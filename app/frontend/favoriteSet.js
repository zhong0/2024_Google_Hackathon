const explore_container = document.getElementById('favorite-set-container');
const search_button = document.getElementById('search-bt');
const username_input = document.getElementById('username-input');
//from API
// const data = [{
//     filename: ['zhong0/02.jpg', 'zhong0/04.jpg'],
//     style: ['casuel', 'simple'],
//     description:'this is a simple style clothes'
// }, {
//     filename: ['zhong0/22.jpg', 'zhong0/23.jpg'],
//     style: ['casuel', 'sports'],
//     description:'this is a sports style clothes'
// }]
const data = [];

search_button.addEventListener('click', ()=>{
    let username = username_input.value;

    //remove explore container child
    remove_all_child_in_explore_container();
    //remove data
    data.length = 0;
    //clean text input
    username_input.value = '';
    
    fetch_favorite_set_data(username);
});

function remove_all_child_in_explore_container(){
    let cards = document.getElementsByClassName('explore-set-card');
    while(cards.length>0){
        explore_container.removeChild(cards[0]);
    }
    console.log('explore_container length:',explore_container.length);
}

function prepare_data(response_data){
    for(favorite_set of response_data.favorite_set){
        data.push({'filename':favorite_set.clothes_list, 'style':favorite_set.style, 'description':favorite_set.description});
    }

    data.forEach((ele) => {
        // 根據提供的 data 數據創建 explore-set-card 元素
        const card = document.createElement("div");
        card.classList.add("explore-set-card");
    
        // 創建 explore-set-image-gallery 元素
        const imageGallery = document.createElement("div");
        imageGallery.classList.add("explore-set-image-gallery");
        ele.filename.forEach(function(imageSrc) {
            const img = document.createElement("img");
            img.src = `../upload/${imageSrc}`;
            imageGallery.appendChild(img);
        });
    
        // 創建 explore-set-tag-row 元素
        const tagRow = document.createElement("div");
        tagRow.classList.add("explore-set-tag-row");
        ele.style.forEach(function(tagText) {
            const tag = document.createElement("div");
            tag.classList.add("explore-set-tag");
            tag.textContent = `#${tagText}`;
            tagRow.appendChild(tag);
        });
    
        // 創建 explore-set-description-text 元素
        const description = document.createElement("p");
        description.classList.add("explore-set-description-text");
        description.textContent = ele.description;
    
        // 將創建的元素添加到 card 元素中
        card.appendChild(imageGallery);
        card.appendChild(tagRow);
        card.appendChild(description);
    
        // 將 card 元素添加到 container 元素中
        explore_container.appendChild(card);
    
        card.addEventListener('click', () => {
            fetch('/explore_intro', { method: 'GET' })
                .then(response => {
                    if (response.ok) {
                        window.location.href = '/explore_intro';
                    } else {
                        console.error('Error:', response.statusText);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    
    })
}

function fetch_favorite_set_data(username){
    let form_data = new FormData();
    form_data.append('username',username);

    const request_options = {
        method:'POST',
        body:form_data
    }

    fetch('/clothes/favorite-set', request_options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            //set toggle button by data 
            console.log(data)
            prepare_data(data);
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
}

document.addEventListener('DOMContentLoaded', function(){
    //fetch own favorite set
    fetch_favorite_set_data('chiPi_data');
});
