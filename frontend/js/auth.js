if (document.querySelector('.login-form form')) {
    document.querySelector('.login-form form').addEventListener('submit', async function(e) {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        console.log('Submitting login for:', email); 

        try {
            const response = await fetch('http://localhost:5000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

           
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json(); 
            console.log('Response status:', response.status); 

            if (data.success) {
                const { id, email, username } = data.user; 

                
                localStorage.setItem('userEmail', email); 

                
                localStorage.setItem('userId', id);

                alert('Login successful!');
                
                window.location.href = 'dashboard-user.html';
            } else {
                alert('Login failed: ' + data.message);
            }
        } catch (error) {
            console.error('Fetch error:', error);
            alert('An error occurred during login. Please try again.');
        }
    });
}



// Handle user registration
if (document.querySelector('.user-registration form')) {
    document.querySelector('.user-registration form').addEventListener('submit', function(e) {
        e.preventDefault();

        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        console.log('Submitting registration for:', username, email); // Log the submission

        fetch('http://localhost:5000/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        })
        .then(response => {
            console.log('Response status:', response.status); // Log the response status
            return response.json().catch(error => {
                console.error('Error parsing JSON:', error);
                throw new Error('Invalid JSON response');
            });
        })
        .then(data => {
            console.log('Response data:', data); 
            if (data.error) {
                alert(data.error);
            } else {
                alert('Registration successful');
                console.log('Redirecting to login page...'); 
                window.location.href = 'user-login.html';
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            alert('An error occurred during registration. Please try again.');
        });
    });
}


if (document.querySelector('.organizer-login form')) {
    document.querySelector('.organizer-login form').addEventListener('submit', function(e) {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        console.log('Submitting login for:',  email); 

        fetch('http://localhost:5000/admin_login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({  email, password })
        })
        .then(response => {
            console.log('Response status:', response.status); 
            return response.json().catch(error => {
                console.error('Error parsing JSON:', error);
                throw new Error('Invalid JSON response');
            });
        })
        .then(data => {
            console.log('Response data:', data); 
            if (data.error) {
                alert(data.error);
            } else {
                alert('Login successful');
                console.log('Redirecting to login page...'); 
                window.location.href = 'dashboard.html';
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            alert('An error occurred during registration. Please try again.');
        });
    });
}

