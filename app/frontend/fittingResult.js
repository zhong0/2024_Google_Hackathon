const toggleBtn = document.getElementById('like-bt');
const toggleLabel = document.querySelector('.like-toggle-label');
const recommend_container = document.getElementById("recommend-scroll-container-wrapper");
const description_text = document.getElementById("description-text");
const home_button = document.getElementById("home-bt");
const refresh_button = document.getElementById("refresh-bt");

console.log('styleToggle:', JSON.parse(localStorage.getItem('styleToggleSelected')))
console.log('occasionToggle:', JSON.parse(localStorage.getItem('occasionToggleSelected')))
console.log('specific_clothes:', JSON.parse(localStorage.getItem('specific_clothes')))

// from API
/*let imageListData = [
    { id: 1, filename: "zhong0/01.jpg", "chosen": false, 'category': 'Bottom'},
    { id: 2, filename: "zhong0/04.jpg", "chosen": false, 'category': 'Top'},
];*/
let imageListData = [];
let description = "This is a casual style."
let style = [];



toggleBtn.addEventListener('click', function() {
    console.log(this.checked)
    if (this.checked) {
        //prepare FormData
        const form_data = new FormData();
        form_data.append('username', 'chiPi_data');
        form_data.append('description', description);
        style.forEach(ele =>{
            form_data.append('style', ele);
        });
        imageListData.forEach(image_data=>{
            form_data.append('filename_list', image_data.filename);
        });
        
        const request_options = {
            method:'POST',
            body:form_data
        }

        fetch('/clothes/add-favorite-set', request_options)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('response:',data);
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
      } else {
        //delete favorite set
        const form_data = new FormData();
        form_data.append('username', 'chiPi_data');
        imageListData.forEach(image_data=>{
            form_data.append('filename_list', image_data.filename);
        });
        
        const request_options = {
            method:'POST',
            body:form_data
        }

        fetch('/clothes/remove-favorite-set', request_options)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('response:',data);
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });
      }
});

toggleBtn.addEventListener('change', (event)=>{
    let is_checked = event.target.checked;
    if(is_checked){
        toggleLabel.style.backgroundImage = "url('../resource/liked_bt.png')";
    } else {
        toggleLabel.style.backgroundImage = "url('../resource/like_bt.png')";
    }
});



home_button.addEventListener('click', () => {
    fetch('/', { method: 'GET' })
        .then(response => {
            if (response.ok) {
                localStorage.removeItem('styleToggleSelected');
                localStorage.removeItem('occasionToggleSelected');
                localStorage.removeItem('specific_clothes');
                window.location.href = '/';
            } else {
                console.error('Error:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

function remove_all_child_in_scroll_container_wrapper(){
    console.log(recommend_container);
    let container_childs = document.getElementsByClassName('image-scroll-container')
    console.log(container_childs, container_childs.length);
    while(container_childs.length>0){
        recommend_container.removeChild(container_childs[0]);
    }
}

refresh_button.addEventListener('click', ()=>{
    console.log('refreshing...')
    //clean imageListData
    imageListData.length = 0;
    remove_all_child_in_scroll_container_wrapper();
    description_text.textContent = '';
    //reset like-btn
    toggleBtn.checked = false;
    console.log(toggleBtn.checked)


    fetch_recommend(true);
});

function fetch_recommend(isRefresh){
    const payload_data = {
        username: 'chiPi_data',
        style: JSON.parse(localStorage.getItem('styleToggleSelected')),
        occasion: JSON.parse(localStorage.getItem('occasionToggleSelected')),
        specific_clothes: JSON.parse(localStorage.getItem('specific_clothes')),
        isRefresh: isRefresh
    }

    const request_options = {
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body:JSON.stringify(payload_data)
    }

    fetch('/recommend/recommend-by-text', request_options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            let idex = 1;
            let file_path = '../upload/';
            console.log(data.recommend_result)
            //set imageListData
            let filenames = data.recommend_result['recommend_set'];
            filenames.forEach( (filename) =>{
                imageListData.push({ id: idex, filename: filename});
                idex += 1;
            });
            imageListData.forEach(function(imageSrc) {
                const imageContainer = document.createElement("div");
                imageContainer.className = "image-scroll-container";
                
                const imageElement = document.createElement("img");
                imageElement.src = file_path+imageSrc.filename;
                imageElement.alt = "Image";
                imageElement.id = imageSrc.id;
                imageElement.style.height = '200px';
                imageContainer.appendChild(imageElement);
                    
                recommend_container.appendChild(imageContainer);
            });
            //set style
            style = data.recommend_result['style'];
            //set description text
            description = data.recommend_result['description'];
            description_text.textContent = description;
            //check is already in favorite set
            if(data.recommend_result['is_favorite_set']==false){
                toggleBtn.checked = false;
            } else {
                toggleBtn.checked = true;
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
}

document.addEventListener('DOMContentLoaded', function() {
    
    fetch_recommend(false);
    
});