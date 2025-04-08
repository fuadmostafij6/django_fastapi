

const API_BASE_URL = 'http://localhost:8001/api'; // Change to your Django server URL

// DOM Elements
const registerForm = document.getElementById('registerForm');
const loginForm = document.getElementById('loginForm');
const userDashboard = document.getElementById('userDashboard');
const logoutBtn = document.getElementById('logoutBtn');

// Event Listeners
// registerForm.addEventListener('submit', handleRegister);
// loginForm.addEventListener('submit', handleLogin);
// logoutBtn.addEventListener('click', handleLogout);

// Check if user is already logged in
// checkAuthStatus();

document.getElementById('registerForm').addEventListener('submit', async function(e) {
    e.preventDefault();
  const messageEl = document.getElementById('loginMessage');
    try {
        const response = await fetch('http://localhost:8001/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Include if using CSRF
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                username: document.getElementById('regUsername').value,
                email: document.getElementById('regEmail').value,
                password: document.getElementById('regPassword').value
            }),
            credentials: 'include'  // Important for cookies/session
        });
  const data = await response.json();
        if (!response.ok) {
             showMessage(messageEl, data.detail || 'Registration failed', 'error');
            throw new Error(await response.text());

        }


 showMessage(messageEl, "Registration success", 'success');
        console.log('Registration success:', data);
         setTimeout(() => {
                window.location.href = '/uni_project/front_end/login.html';  // Redirect to login page
            }, 2000);

    } catch (error) {
        console.error('Registration failed:', error);
        // Handle error
    }
});





async function handleLogout() {
    try {
        const response = await fetch(`${API_BASE_URL}/logout/`, {
            method: 'POST',
            credentials: 'include'
        });

        if (response.ok) {
            updateUIAfterLogout();
        }
    } catch (error) {
        console.error('Logout error:', error);
    }
}

async function checkAuthStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/check-auth/`, {
            credentials: 'include'
        });

        if (response.ok) {
            const userData = await response.json();
           updateUIAfterLogin(userData);
        }
    } catch (error) {
        console.error('Auth check error:', error);
    }
}

function updateUIAfterLogin(userData) {
    // document.querySelector('.auth-forms').classList.add('hidden');
    // userDashboard.classList.remove('hidden');
    document.getElementById('dashboardUsername').textContent = userData.username;
    document.getElementById('dashboardEmail').textContent = userData.email;
}

function updateUIAfterLogout() {
    userDashboard.classList.add('hidden');
    document.querySelector('.auth-forms').classList.remove('hidden');
}

function showMessage(element, message, type) {
    element.textContent = message;
    element.className = `message ${type}`;
    setTimeout(() => {
        element.textContent = '';
        element.className = 'message';
    }, 5000);
}