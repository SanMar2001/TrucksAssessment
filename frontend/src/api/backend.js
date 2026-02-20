const API_URL = "http://localhost:8000/api";

export async function submitInputs(data, endpoint = "calculate") {
  try {
    const url = `${API_URL}/${endpoint}/`;
    const response = await fetch(url, {
      method: 'POST',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
}

export async function testBackend() {
  try {
    const url = `${API_URL}/test/`;
    const response = await fetch(url, {
      method: 'GET',
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
}

