const addAccountBtn = document.getElementById('createAccount');
const newAccountCard = document.getElementById('0');
addAccountBtn.addEventListener("click", handleAddAccount)
const scriptRoot = SCRIPT_ROOT;
const root2 = undefined;

function handleSave(event) {
    let accountCard = document.createElement('div');
//    card align-middle m-card p-3
    accountCard.classList.add('card');
    accountCard.classList.add('align-middle');
    accountCard.classList.add('m-card');
    accountCard.classList.add('p-3');
    return
}

function handleAddAccount(event) {
    let url = root + '/manage';
    let name = document.getElementById('name').value
    let username = document.getElementById('username').value
    let email = document.getElementById('email');
    let pwd = document.getElementById('pwd')
    let account = {
        'name': name,
        'username': username,
        'email': email,
        'password': pwd
    }

}

function sendData(accountData, manageUrl) {
    let data = new FormData()
    data.append('name': accountData.['name']);
    data.append('username': accountData.['username']);
    data.append('email': accountData.['email']);
    data.append('password': accountData['password']);
    fetch(manageUrl, {
        'method': 'POST',
        'headers': {"Content-Type": "application/json"},
        'body': JSON.stringify(data),
    }).then(
        response => {
            if (response.redirected) {
                window.location = response.url;
            } else {
                // for now just log error
                console.log('unknown error as of now');
            }
        }
    )
}
