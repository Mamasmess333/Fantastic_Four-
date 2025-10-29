const API = "http://127.0.0.1:8000"; // FastAPI backend

async function uploadImage() {
  const fileInput = document.getElementById("imageUpload");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select an image first!");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  const resultBox = document.getElementById("result");
  resultBox.textContent = "Analyzing image... ⏳";

  try {
    // Call /upload directly
    const response = await fetch(`${API}/upload`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Upload or analysis failed");
    const data = await response.json();
    console.log("Server response:", data);

    // Show the JSON response
    resultBox.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    resultBox.textContent = `❌ Error: ${error.message}`;
  }
}
