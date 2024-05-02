const description_container = document.getElementById('set-image');
const piece_container = document.getElementById('piece-image');
const tag_container =  document.querySelector('.explore-set-tag-row');
const text_container = document.getElementById('explore-set-description-text');
const like_bt = document.getElementById('like-bt');
const like_label = document.getElementById('like-label');
const loading_container = document.getElementById('loading');

loading_container.style.display = 'flex';

console.log('get from explore',JSON.parse(localStorage.getItem('exploreSelectedSetFilename')),
JSON.parse(localStorage.getItem('exploreSelectedSetStyle')),
JSON.parse(localStorage.getItem('exploreSelectedSetdescription')));

// const data = {
//     filename: ['zhong0/02.jpg', 'zhong0/04.jpg'],
//     style: ['casuel', 'simple'],
//     description:'this is a simple style clothes.'
// };
const data = {
  filename: JSON.parse(localStorage.getItem('exploreSelectedSetFilename')),
  style: JSON.parse(localStorage.getItem('exploreSelectedSetStyle')),
  description: JSON.parse(localStorage.getItem('exploreSelectedSetdescription'))
};

// const pieceRecommend = ['zhong0/12.jpg', 'zhong0/13.jpg'];
const pieceRecommend = [];
let pieces_recommend_by = {};
let pieces_display_list = [];

text_container.textContent = data.description;

like_bt.addEventListener('click', function() {
  console.log(this.checked)
  if (this.checked) {
      //prepare FormData
      const form_data = new FormData();
      form_data.append('username', localStorage.getItem('username'));
      form_data.append('description', JSON.parse(localStorage.getItem('exploreSelectedSetdescription')));
      JSON.parse(localStorage.getItem('exploreSelectedSetStyle')).forEach(style =>{
          form_data.append('style', style);
      });
      JSON.parse(localStorage.getItem('exploreSelectedSetFilename')).forEach(filename=>{
          form_data.append('filename_list', filename);
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
      form_data.append('username', localStorage.getItem('username'));
      JSON.parse(localStorage.getItem('exploreSelectedSetFilename')).forEach(filename=>{
          form_data.append('filename_list', filename);
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

like_bt.addEventListener('change', function() {
    if (this.checked) {
        like_label.style.backgroundImage = "url('../resource/liked_bt.png')";
      } else {
        like_label.style.backgroundImage = "url('../resource/like_bt.png')";
      }
});


function change_display_list(filename_list ,is_display){
  if(is_display === true){
    filename_list.forEach((ele)=>{
      pieces_display_list.push(ele);
    });
  } else {
    filename_list.forEach((ele)=>{
      let index = pieces_display_list.indexOf(ele);
      if(index !== -1){
        pieces_display_list.splice(index, 1);
      }
    });
  }
  let image_wrappers = document.getElementsByClassName('image-wrapper');
  if(pieces_display_list.length === 0){
    //display all
    for(let i=0; i<image_wrappers.length; i++){
      //avoid pin clothes
      if(image_wrappers[i].querySelector('input')===null){
        image_wrappers[i].style.display = '';
      }
    }
  } else {
    //hide all
    for(let i=0; i<image_wrappers.length; i++){
      if(image_wrappers[i].querySelector('input')===null){
        console.log('in0');
        image_wrappers[i].style.display = 'none';
      }
    }
    //only display included in pieces_display_list
    for(let i=0; i<image_wrappers.length; i++){
      if(image_wrappers[i].querySelector('input')===null){
        let img_src = image_wrappers[i].querySelector('img').getAttribute('src');
        if(pieces_display_list.includes(img_src.replace('../upload/', ''))){
          image_wrappers[i].style.display = '';
        }
      }
    }
    
  }
}

data.style.forEach((ele) => {
    const tag = document.createElement('div');
    tag.classList.add('explore-set-tag');
    tag.textContent = ele;
    tag_container.appendChild(tag);
});

data.filename.forEach((ele)=> {
  const imageWrapper = document.createElement('div');
  imageWrapper.classList.add('image-wrapper');

  // 創建 input 元素
  const toggle = document.createElement('input');
  toggle.setAttribute('type', 'checkbox');
  toggle.id = 'pin-bt-' + ele; // 每個 input 元素的 id 需要唯一
  toggle.classList.add('pin-toggle-btn');

  // 創建 label 元素
  const label = document.createElement('label');
  label.setAttribute('for', 'pin-bt-' + ele); // 將 label 連接到對應的 input 元素
  label.classList.add('pin-toggle-label');

  toggle.addEventListener('click', function(){
    if(this.checked){
      change_display_list(pieces_recommend_by[ele], true);
    } else {
      change_display_list(pieces_recommend_by[ele], false);
    }
  });

  // 創建 img 元素
  const img = document.createElement('img');
  img.src = `../upload/${ele}`; // 圖片路徑根據索引 i 設置
  img.alt = 'Image ' + ele;

  // 添加 hover 效果
  img.addEventListener('mouseover', function() {
    imageWrapper.classList.add('hovered');
  });
  img.addEventListener('mouseout', function() {
    imageWrapper.classList.remove('hovered');
  });

  img.addEventListener('click', function() {
    showPieceInfo(img);
  });

  // 將 input、label 和 img 元素添加到 imageWrapper 中
  imageWrapper.appendChild(toggle);
  imageWrapper.appendChild(label);
  imageWrapper.appendChild(img);

  // 將 imageWrapper 添加到父容器中
  description_container.appendChild(imageWrapper);
});

function showMessage(message) {
  const alertBox = document.createElement('div');
  alertBox.textContent = message;
  alertBox.style.backgroundColor = '#000000';
  alertBox.style.color = 'white';
  alertBox.style.padding = '10px 20px';
  alertBox.style.borderRadius = '10px';
  alertBox.style.position = 'fixed';
  alertBox.style.top = '50%';
  alertBox.style.left = '50%';
  alertBox.style.transform = 'translate(-50%, -50%)';
  alertBox.style.zIndex = '9999';
  alertBox.style.animation = 'fadeOut 3s linear infinite';

  document.body.appendChild(alertBox);

  setTimeout(function() {
      document.body.removeChild(alertBox);
  }, 3000); // 2秒后移除提示框
}

function showPieceInfo (img) {
  searchUsername = img.src.split('/').slice(-2)[0];
  const filename = img.src.split('/').slice(-2).join('/');
  localStorage.setItem('search_piece_clothes_filename', filename);
  // if (searchUsername !== localStorage.getItem('username')) {
      // now is searching a user
      loading_container.style.display = 'flex';
      const form_data = new FormData();
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
              if (data) {
                  if (data.url) {
                      // if this clothe is sold by a brand
                      window.open(data.url, '_blank');
                      loading_container.style.display = 'none';
                  } else {
                      // if this clothe is sold by a user
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
                  }
              } else {
                loading_container.style.display = 'none';
                showMessage('This is in your closet');
              }
          })
          .catch(error => {
              console.error('Fetch error:', error);
          });
      
  // } else {
  //     //now is user by himself
  //     fetch('/store', { method: 'GET' })
  //     .then(response => {
  //         if (response.ok) {
  //             window.location.href = '/store';
  //         } else {
  //             console.error('Error:', response.statusText);
  //         }
  //     })
  //     .catch(error => {
  //         console.error('Error:', error);
  //     });
  // }
}


function prepare_piece_recommend_data(response_data){

  for(const combo in response_data.recommend_results){
    console.log(combo);
    response_data.recommend_results[combo].forEach(ele =>{
      if(!pieceRecommend.includes(ele)){
        pieceRecommend.push(ele);
      }
    });
  }

  console.log(pieceRecommend);

  pieceRecommend.forEach((ele) => {
    const imageWrapper = document.createElement('div');
    imageWrapper.classList.add('image-wrapper');
    //imageWrapper.style.display = 'none';
  
    const img = document.createElement('img');
    img.src = `../upload/${ele}`; // 圖片路徑根據索引 i 設置
    img.alt = 'Image ' + ele;
  
      // 添加 hover 效果
    img.addEventListener('mouseover', function() {
      imageWrapper.classList.add('hovered');
    });
    img.addEventListener('mouseout', function() {
      imageWrapper.classList.remove('hovered');
    });
    
  
    img.addEventListener('click', function() {
      showPieceInfo(img);
    });
  
    imageWrapper.appendChild(img);
    piece_container.appendChild(imageWrapper);
  });
}

function fetch_explore_piece_recommend_data(){
  const payload_data = {
      username:localStorage.getItem('username'),
      style: JSON.parse(localStorage.getItem('exploreSelectedSetStyle')),
      specific_clothes: JSON.parse(localStorage.getItem('exploreSelectedSetFilename')),
      recommend_count:10
  }

  const request_options = {
      method:'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body:JSON.stringify(payload_data)
  }

  fetch('/recommend/explore-pieces-recommendation', request_options)
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          console.log(data)
          prepare_piece_recommend_data(data);
          pieces_recommend_by = data.recommend_results;
          console.log(pieces_recommend_by);
          loading_container.style.display = 'none';
      })
      .catch(error => {
          console.error('Fetch error:', error);
      });
}

document.addEventListener('DOMContentLoaded', ()=>{
  //should use fetch check whether this set is favorite
  // if(localStorage.getItem('isFavoriteSet') === true){
  //   const change_event = new Event('change');
  //   toggleBtn.checked = false;
  //   toggleBtn.dispatchEvent(change_event);
  // }
  //fetch api
  fetch_explore_piece_recommend_data();

});