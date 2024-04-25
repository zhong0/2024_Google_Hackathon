const account_input = document.getElementById('account-input-text');
const pwd_input = document.getElementById('pwd-input-text');
const login_button = document.getElementById('login-bt');


login_button.addEventListener('click', () => {
    let account = account_input.value;
    let pwd = pwd_input.value; 
    
    console.log(account);
    console.log(pwd);
});