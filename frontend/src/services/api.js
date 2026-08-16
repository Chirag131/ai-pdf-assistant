const API_BASE_URL = "http://127.0.0.1:8000";

async function handleResponse(response) {
  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Something went wrong with the server."
    );
  }

  return data;
}

export async function checkHealth() {
  const response = await fetch(
    `${API_BASE_URL}/health`
  );

  return handleResponse(response);
}

export async function uploadPdf(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  return handleResponse(response);
}

export async function askQuestion(question) {
  const response = await fetch(
    `${API_BASE_URL}/ask`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
      }),
    }
  );

  return handleResponse(response);
}