const account_input = document.getElementById('account-input-text');
const pwd_input = document.getElementById('pwd-input-text');
const login_button = document.getElementById('login-bt');


login_button.addEventListener('click', () => {
    let account = account_input.value;
    let pwd = pwd_input.value; 
    let payload_data = {
        "username":account,
        "password":pwd
    }

    let request_options = {
        method:'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body:JSON.stringify(payload_data)
    }
    
    console.log(account);
    console.log(pwd);

    fetch('/auth/register', request_options)
    .then(response => {
        if (!response.ok) {
            // registered return 400
            if(response.status!==400){
                throw new Error('Network response was not ok');
            }
        }
        return response.json();
    })
    .then(data =>{
        console.log('h',data);
        //register successfully and already registered return different key
        if(data.detail==='Username already registered' || data.message==='User registered successfully'){
            // if registered try login
            fetch('/auth/login', request_options)
                .then(login_response => {
                    if (!login_response.ok) {
                        throw new Error('Login failed: '+data.detail);
                    }
                    return login_response.json();
                })
                .then(login_data => {
                    //login successfully, store username and go to homepage
                    console.log(login_data)
                    localStorage.setItem('username', account);
                    window.location.href = '/';
                })
                .catch(login_error =>{
                    console.log(login_error)
                });
        } else {
            throw new Error('Login network response was not ok');
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
    });
});