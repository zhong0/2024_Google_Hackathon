let piece_image = document.getElementById('piece-pic');
let piece_name = document.getElementById('piece-name');
let owner_name = document.getElementById('owner-username');
let brand_text = document.getElementById('brand-text');
let size_text = document.getElementById('size-text');
let detail_text = document.getElementById('detail-text');
let price_text = document.getElementById('price-text');

// from API

const data = {
    filename: 'zhong0/22.jpg',
    name: 'Tempo Running Shorts',
    price: '10',
    brand: 'nike',
    size: 'M',
    detail: 'This is a sports style shorts.'
}
piece_image.src = `../upload/${data.filename}`;
piece_name.textContent = data.name;
price_text.textContent = `$ ${data.price}`;
owner_name.textContent = data.filename.split('/')[0];
brand_text.textContent = data.brand;
size_text.textContent = data.size;
detail_text.textContent = data.detail;

