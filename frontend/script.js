// Use relative URL since frontend is served by FastAPI
const API = ""; // Empty string for same-origin requests

async function uploadImage() {
  const fileInput = document.getElementById("imageUpload");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select an image first!");
    return;
  }

  // Check if user is logged in
  const token = localStorage.getItem('access_token');

  if (!token) {
    const userConfirmed = confirm("You need to log in to analyze images. Would you like to go to the login page?");
    if (userConfirmed) {
      window.location.href = '/static/login.html';
    }
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  const resultBox = document.getElementById("result");
  resultBox.textContent = "Analyzing image... ⏳";

  try {
    console.log('Token found:', token ? 'Yes' : 'No');
    console.log('Token preview:', token ? token.substring(0, 20) + '...' : 'null');

    console.log('Sending request to:', `${API}/upload`);
    console.log('Authorization header:', `Bearer ${token.substring(0, 20)}...`);

    // Call /upload directly with auth token
    const response = await fetch(`${API}/upload`, {
      method: "POST",
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData,
    });

    console.log('Response status:', response.status);

    if (response.status === 401) {
      resultBox.textContent = "❌ Session expired. Please login again";
      localStorage.removeItem('access_token');
      setTimeout(() => {
        window.location.href = '/static/login.html';
      }, 2000);
      return;
    }

    if (!response.ok) throw new Error("Upload or analysis failed");
    const data = await response.json();
    console.log("Server response:", data);

    // Show the JSON response
    resultBox.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    resultBox.textContent = `❌ Error: ${error.message}`;
  }
}
