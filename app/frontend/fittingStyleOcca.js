const style_container = document.getElementById('style-toggle-btn');
const occasion_container = document.getElementById('occasion-toggle-btn');
const addStyle_button = document.getElementById('add-style-bt');
const addOccasion_button = document.getElementById('add-occasion-bt');
const addStyle_input = document.getElementById('style-input');
const addOccasion_input = document.getElementById('occasion-input');
const nextPage_button = document.getElementById('next-bt');
const loading_container = document.getElementById('loading');

loading_container.style.display = 'flex';

// from API
/*let styleToggle = [
    { id: 1, text: 'Toggle 1', checked: false },
    { id: 2, text: 'Toggle 2', checked: false },
    { id: 3, text: 'Toggle 3', checked: false },
    { id: 6, text: 'Toggle 4', checked: false },
    { id: 9, text: 'Toggle 5', checked: false }
];

let occasionToggle = [
    { id: 4, text: 'Toggle 1', checked: false },
    { id: 7, text: 'Toggle 2', checked: false },
    { id: 8, text: 'Toggle 3', checked: false },
    { id: 5, text: 'Toggle 4', checked: false },
    { id: 10, text: 'Toggle 5', checked: false }
];*/
let styleToggle = [];
let occasionToggle = [];

function add_toggle(id, text, checked, container) {
    // create input element
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = id;
    checkbox.checked = checked;

    // create label element
    const label = document.createElement('label');
    label.htmlFor = id;
    label.textContent = text;

    // append to container
    container.appendChild(checkbox);
    container.appendChild(label);
    container.appendChild(document.createElement('br'));
}

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

    document.body.appendChild(alertBox);

    setTimeout(function() {
        document.body.removeChild(alertBox);
    }, 2000); // 2秒后移除提示框
}

// choose style
/*styleToggle.forEach(params => {
    add_toggle(params.id, params.text, params.checked, style_container);

});

// choose occasion
occasionToggle.forEach(params => {
    add_toggle(params.id, params.text, params.checked, occasion_container);
});*/

addStyle_button.addEventListener('click', () => {
    let style_input = addStyle_input.value;
    if (style_input !== "" && style_input !== null) {
        const allToggle = styleToggle.concat(occasionToggle);
        const allStyleText = styleToggle.map((ele) => ele.text);

        if (!allStyleText.includes(style_input)) {
            const id = allToggle.length + 1;
            const text = style_input;
            const checked = true;
            styleToggle.push({id: id, text: text, checked: true})
            add_toggle(id, text, checked, style_container);
        } else {
            showMessage(`${style_input} has already added.`);
        }
    }
    addStyle_input.value = '';
});

addOccasion_button.addEventListener('click', () => {
    let occasion_input = addOccasion_input.value;
    if (occasion_input !== "" && occasion_input !== null) {
        const allToggle = styleToggle.concat(occasionToggle);
        const allOccasionText = occasionToggle.map((ele) => ele.text);

        if (!allOccasionText.includes(occasion_input)) {
            const id = allToggle.length + 1;
            const text = occasion_input;
            const checked = true;
            occasionToggle.push({id: id, text: text, checked: true})
            add_toggle(id, text, checked, occasion_container);
        } else {
            showMessage(`${occasion_input} has already added.`);
        }
    }
    addOccasion_input.value = '';
});

nextPage_button.addEventListener('click', () => {
    fetch('/fitting_clothes', { method: 'GET' })
        .then(response => {
            if (response.ok) {
                //store to localstorage
                localStorage.setItem('styleToggleSelected', JSON.stringify(getCheckedToggle(styleToggle)));
                localStorage.setItem('occasionToggleSelected', JSON.stringify(getCheckedToggle(occasionToggle)));
                window.location.href = '/fitting_clothes';
                
            } else {
                console.error('Error:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

function getCheckedToggle(toggle){
    //return a list of toggle.text whick checkbox.checked is true
    let checkedToggle = [];
    toggle.forEach(t =>{
        if(document.getElementById(t.id).checked){
            checkedToggle.push(t.text);
        }
    });
    return checkedToggle;
}


function loadStyleToggleData(toggleNames){
    //get total toggle button numbers
    let allToggleLegnth = styleToggle.concat(occasionToggle).length;
    for(const toggleName of toggleNames){
        allToggleLegnth += 1;
        styleToggle.push({ id: allToggleLegnth, text: toggleName, checked: false })
    }
    styleToggle.forEach(params => {
        add_toggle(params.id, params.text, params.checked, style_container);
    
    });
}

function loadOccasionToggleData(toggleNames){
    //get total toggle button numbers
    let allToggleLegnth = styleToggle.concat(occasionToggle).length;
    for(const toggleName of toggleNames){
        allToggleLegnth += 1;
        occasionToggle.push({ id: allToggleLegnth, text: toggleName, checked: false })
    }
    occasionToggle.forEach(params => {
        add_toggle(params.id, params.text, params.checked, occasion_container);
    
    });
}
document.addEventListener('DOMContentLoaded', function() {
    const form_data = new FormData();
    form_data.append('username','chiPi_data');

    const request_options = {
        method:'POST',
        body:form_data
    }

    fetch('clothes/style', request_options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            //set toggle button by data 
            loadStyleToggleData(data.style);
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });

    fetch('clothes/occasion', request_options)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            loading_container.style.display = 'none';
            return response.json();
        })
        .then(data => {
            //set toggle button by data 
            loadOccasionToggleData(data.occasion);
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
});

