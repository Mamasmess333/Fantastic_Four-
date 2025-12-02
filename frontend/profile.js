async function loadProfile() {
  const token = localStorage.getItem('access_token');
  const profileContent = document.getElementById('profileContent');

  if (!token) {
    window.location.href = '/static/login.html';
    return;
  }

  try {
    const response = await fetch('/auth/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.ok) {
      const user = await response.json();
      displayProfile(user);
    } else {
      localStorage.removeItem('access_token');
      window.location.href = '/static/login.html';
    }
  } catch (error) {
    profileContent.innerHTML = `
      <p style="color: #ff0033;">Error loading profile: ${error.message}</p>
    `;
  }
}

function displayProfile(user) {
  const profileContent = document.getElementById('profileContent');

  // Get the first letter of username for the icon
  const initial = user.username.charAt(0).toUpperCase();

  // Format the date
  const joinDate = user.created_at
    ? new Date(user.created_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    : 'Unknown';

  profileContent.innerHTML = `
    <div class="profile-icon">${initial}</div>

    <div class="info-group">
      <div class="info-label">Username</div>
      <div class="info-value">${user.username}</div>
    </div>

    <div class="info-group">
      <div class="info-label">Email</div>
      <div class="info-value">${user.email}</div>
    </div>

    <div class="info-group">
      <div class="info-label">User ID</div>
      <div class="info-value">#${user.id}</div>
    </div>

    <div class="info-group">
      <div class="info-label">Member Since</div>
      <div class="info-value">${joinDate}</div>
    </div>
  `;
}

function logout() {
  if (confirm('Are you sure you want to logout?')) {
    localStorage.removeItem('access_token');
    window.location.href = '/static/login.html';
  }
}

// Load profile when page loads
window.addEventListener('DOMContentLoaded', loadProfile);
