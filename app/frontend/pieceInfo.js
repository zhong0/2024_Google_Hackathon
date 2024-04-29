let piece_image = document.getElementById('piece-pic');
let piece_name = document.getElementById('piece-name');
let owner_name = document.getElementById('owner-username');
let brand_text = document.getElementById('brand-text');
let size_text = document.getElementById('size-text');
let detail_text = document.getElementById('detail-text');
let price_text = document.getElementById('price-text');
const user_button = document.getElementById('user-bt');
const loading_container = document.getElementById('loading');

// from API
const search_piece_clothes_filename = localStorage.getItem('search_piece_clothes_filename');
const search_username = search_piece_clothes_filename.split("/")[0]

document.addEventListener('DOMContentLoaded', function() {
    loading_container.style.display = 'flex';
    const form_data = new FormData();
    form_data.append('username', search_username);
    form_data.append('filename', search_piece_clothes_filename);

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
            if(!data) {
                console.log(`The clothe was not found.`);
            } else {
                console.log(data);
                piece_image.src = `../upload/${search_piece_clothes_filename}`;
                piece_name.textContent = data.name;
                price_text.textContent = `$ ${data.sale_info.price}`;
                owner_name.textContent =  search_username;
                brand_text.textContent = data.sale_info.brand ? data.sale_info.brand: 'No';
                size_text.textContent = data.sale_info.size ? data.sale_info.size: 'No';
                detail_text.textContent = data.sale_info.detail ? data.sale_info.detail: 'No';
            }
            loading_container.style.display = 'none';
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
    
});

user_button.addEventListener('click', function() {
    localStorage.setItem('search_username', search_username);
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
