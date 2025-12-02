function switchTab(tab) {
  const loginTab = document.querySelector('.tab:nth-child(1)');
  const registerTab = document.querySelector('.tab:nth-child(2)');
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');

  if (tab === 'login') {
    loginTab.classList.add('active');
    registerTab.classList.remove('active');
    loginForm.classList.add('active');
    registerForm.classList.remove('active');
  } else {
    loginTab.classList.remove('active');
    registerTab.classList.add('active');
    loginForm.classList.remove('active');
    registerForm.classList.add('active');
  }

  // Clear messages
  document.getElementById('loginMessage').className = 'message';
  document.getElementById('registerMessage').className = 'message';
}

async function handleLogin(event) {
  event.preventDefault();

  const username = document.getElementById('loginUsername').value;
  const password = document.getElementById('loginPassword').value;
  const messageDiv = document.getElementById('loginMessage');

  messageDiv.className = 'message';
  messageDiv.textContent = '';

  try {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch('/auth/login', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (response.ok) {
      messageDiv.className = 'message success';
      messageDiv.textContent = 'Login successful! Redirecting...';

      // Store the token
      localStorage.setItem('access_token', data.access_token);

      // Redirect to main app after 1 second
      setTimeout(() => {
        window.location.href = '/static/index.html';
      }, 1000);
    } else {
      messageDiv.className = 'message error';
      messageDiv.textContent = data.detail || 'Login failed';
    }
  } catch (error) {
    messageDiv.className = 'message error';
    messageDiv.textContent = 'Network error: ' + error.message;
  }
}

async function handleRegister(event) {
  event.preventDefault();

  const username = document.getElementById('registerUsername').value;
  const email = document.getElementById('registerEmail').value;
  const password = document.getElementById('registerPassword').value;
  const messageDiv = document.getElementById('registerMessage');

  messageDiv.className = 'message';
  messageDiv.textContent = '';

  try {
    const response = await fetch('/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        email: email,
        password: password,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      messageDiv.className = 'message success';
      messageDiv.textContent = 'Registration successful! Please login.';

      // Clear form
      document.getElementById('registerUsername').value = '';
      document.getElementById('registerEmail').value = '';
      document.getElementById('registerPassword').value = '';

      // Switch to login tab after 2 seconds
      setTimeout(() => {
        switchTab('login');
      }, 2000);
    } else {
      messageDiv.className = 'message error';
      messageDiv.textContent = data.detail || 'Registration failed';
    }
  } catch (error) {
    messageDiv.className = 'message error';
    messageDiv.textContent = 'Network error: ' + error.message;
  }
}

// Check if user is already logged in when accessing login page
window.addEventListener('DOMContentLoaded', () => {
  const token = localStorage.getItem('access_token');
  if (token) {
    // Verify token is still valid
    fetch('/auth/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    .then(response => {
      if (response.ok) {
        // Token is valid, redirect to main app
        window.location.href = '/static/index.html';
      }
    })
    .catch(() => {
      // Token is invalid, remove it
      localStorage.removeItem('access_token');
    });
  }
});
