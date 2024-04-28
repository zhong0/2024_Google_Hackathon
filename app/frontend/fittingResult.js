const toggleBtn = document.getElementById('like-bt');
const toggleLabel = document.querySelector('.like-toggle-label');
const recommend_container = document.getElementById("recommend-scroll-container-wrapper");
const description_text = document.getElementById("description-text");
const home_button = document.getElementById("home-bt");

// from API
let imageListData = [
    { id: 1, filename: "../upload/zhong0/01.jpg", "chosen": false, 'category': 'Bottom'},
    { id: 2, filename: "../upload/zhong0/04.jpg", "chosen": false, 'category': 'Top'},
];
let descrption = "This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style.This is a casual style."


description_text.textContent = descrption;
toggleBtn.addEventListener('change', function() {
    console.log(this.checked)
    if (this.checked) {
        toggleLabel.style.backgroundImage = "url('../resource/liked_bt.png')";
      } else {
        toggleLabel.style.backgroundImage = "url('../resource/like_bt.png')";
      }
});

imageListData.forEach(function(imageSrc) {
    const imageContainer = document.createElement("div");
    imageContainer.className = "image-scroll-container";
    
    const imageElement = document.createElement("img");
    imageElement.src = imageSrc.filename;
    imageElement.alt = "Image";
    imageElement.id = imageSrc.id;
    imageElement.style.height = '200px';
    imageContainer.appendChild(imageElement);
        
    recommend_container.appendChild(imageContainer);
});

home_button.addEventListener('click', () => {
    fetch('/', { method: 'GET' })
        .then(response => {
            if (response.ok) {
                window.location.href = '/';
            } else {
                console.error('Error:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});