function handleLogin(event) {
    event.preventDefault();
    var statusP = document.getElementById('status')

    // Fetch the login endpoint
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: document.getElementById('username').value,
            password: document.getElementById('password').value,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            statusP.classList.remove('error','success')
            // Redirect to the dashboard on successful login
            statusP.classList.add('success');
            statusP.textContent = "login Successfull!";
            setTimeout(function(){
                window.location.href = '/';
            },1000);

        } else {
            statusP.classList.remove('error','success')
            // Display an alert for unsuccessful login
            statusP.classList.add('error')
            statusP.textContent = "Username/Password Error"
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Display an alert for general errors
        statusP.classList.add('error')
        statusP.textContent = ("Server" + error)
    });
}