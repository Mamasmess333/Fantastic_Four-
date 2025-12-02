const API_BASE = "http://127.0.0.1:8000";

let loggedInUser = null;

function login() {
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const statusEl = document.getElementById("loginStatus");

  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();

  if (!email || !password) {
    statusEl.textContent = "Please enter email and password.";
    return;
  }
  loggedInUser = email;
  statusEl.textContent = `Logged in as ${email}`;
}

async function uploadImage() {
  const resultBox = document.getElementById("result");

  if (!loggedInUser) {
    alert("Please log in first.");
    return;
  }

  const fileInput = document.getElementById("imageUpload");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select an image first!");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  resultBox.textContent = "Analyzing image... ⏳";

  try {
    const response = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`Server error ${response.status}: ${text}`);
 }

    const data = await response.json();

    // Pretty-print whatever backend returns (status, labels, s3_url, etc.)
    resultBox.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    resultBox.textContent = `❌ Error: ${err.message}`;
  }
}

