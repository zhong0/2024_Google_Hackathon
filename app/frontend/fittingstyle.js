const style_container = document.getElementById('style-toggle-btn');
const occasion_container = document.getElementById('occasion-toggle-btn');
const addStyle_button = document.getElementById('add-style-bt');
const addOccasion_button = document.getElementById('add-occasion-bt');

const styleBtn = [
    { id: 'toggle1', text: 'Toggle 1', checked: true },
    { id: 'toggle2', text: 'Toggle 2', checked: false },
    { id: 'toggle3', text: 'Toggle 3', checked: true },
    { id: 'toggle4', text: 'Toggle 4', checked: false },
    { id: 'toggle5', text: 'Toggle 5', checked: true }
];

// choose style
styleBtn.forEach(params => {
    // create input element
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = params.id;
    checkbox.checked = params.checked;

    // create label element
    const label = document.createElement('label');
    label.htmlFor = params.id;
    label.textContent = params.text;

    // append to container
    style_container.appendChild(checkbox);
    style_container.appendChild(label);
    style_container.appendChild(document.createElement('br'));
});

const occasionBtn = [
    { id: 'toggle6', text: 'Toggle 1', checked: true },
    { id: 'toggle7', text: 'Toggle 2', checked: false },
    { id: 'toggle8', text: 'Toggle 3', checked: true },
    { id: 'toggle9', text: 'Toggle 4', checked: false },
    { id: 'toggle10', text: 'Toggle 5', checked: true }
];

// choose occasion
occasionBtn.forEach(params => {
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = params.id;
    checkbox.checked = params.checked;

    const label = document.createElement('label');
    label.htmlFor = params.id;
    label.textContent = params.text;

    occasion_container.appendChild(checkbox);
    occasion_container.appendChild(label);
    occasion_container.appendChild(document.createElement('br'));
});


