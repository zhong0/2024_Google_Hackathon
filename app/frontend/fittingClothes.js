
const clothestype_dropdown = document.getElementById("clothestype-dropdown");
const pickclothes_container = document.getElementById("pickclothes-scroll-container-wrapper");
const chosen_container = document.getElementById("chosen-scroll-container-wrapper");
const next_button = document.getElementById("next-bt");

console.log('styleToggle:', JSON.parse(localStorage.getItem('styleToggleSelected')))
console.log('occasionToggle:', JSON.parse(localStorage.getItem('occasionToggleSelected')))

// 從 API 拿
let options = ["Top", "Bottom", "Shoes", "Clothes"];
let imageListData = [
    { id: 1, filename: "../upload/zhong0/01.jpg", "chosen": false, 'category': 'Bottom'},
    { id: 2, filename: "../upload/zhong0/02.jpg", "chosen": false, 'category': 'Bottom'},
    { id: 3, filename: "../upload/zhong0/03.jpg", "chosen": false, 'category': 'Bottom'},
    { id: 4, filename: "../upload/zhong0/04.jpg", "chosen": false, 'category': 'Top'},
    { id: 5, filename: "../upload/zhong0/05.jpg", "chosen": false, 'category': 'Bottom'}
];
let chosenList = [];
let selectedValue = "";

function clotheChosen(imageList) {
    imageList.forEach(function(imageSrc) {
        const imageContainer = document.createElement("div");
        imageContainer.className = "image-scroll-container";
    
        const imageElement = document.createElement("img");
        imageElement.src = imageSrc.filename;
        imageElement.alt = "Image";
        imageElement.id = imageSrc.id;
        imageContainer.appendChild(imageElement);
        
        imageContainer.addEventListener("click", function() {
            if (!imageSrc.chosen) { // 沒被選變成被選
                imageSrc.chosen = true;
                chosenList.push(imageSrc.id);
                chosen_container.appendChild(imageContainer);
            } else { // 被選變成沒被選
                imageSrc.chosen = false;
                chosenList.splice(chosenList.indexOf(imageSrc.id), 1);
                if(imageSrc.category !== selectedValue && selectedValue !== "") { // 不在同一頁的話
                    chosen_container.removeChild(imageContainer)
                } else {
                    pickclothes_container.appendChild(imageContainer);
                }      
            }
        });
        pickclothes_container.appendChild(imageContainer);
    });
}


options.forEach(option => {
    const optionElement = document.createElement("option");
    optionElement.text = option;
    optionElement.value = option;
    clothestype_dropdown.appendChild(optionElement);
});

clotheChosen(imageListData);

clothestype_dropdown.addEventListener("change", function() {
    selectedValue = clothestype_dropdown.value;
    pickclothes_container.innerHTML = "";
    let filterImage = []
    if (selectedValue !== "") {
        filterImage = imageListData.filter((ele) => (ele.category === selectedValue && !chosenList.includes(ele.id)));
    } else {
        filterImage = imageListData.filter((ele) => (!chosenList.includes(ele.id)));
    }
    clotheChosen(filterImage)
    
});

const nextPageButton = document.getElementById('fitting-bt');

next_button.addEventListener('click', () => {
    fetch('/fitting_result', { method: 'GET' })
        .then(response => {
            if (response.ok) {
                window.location.href = '/fitting_result';
            } else {
                console.error('Error:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});