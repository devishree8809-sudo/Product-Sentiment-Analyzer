const API_URL = "http://127.0.0.1:5000";

export async function fetchSentimentData(productName) {
  const response = await fetch(
    `${API_URL}/analyze/${encodeURIComponent(productName)}`
  );

  if (!response.ok) {
    let errorMessage = "Product not found";

    try {
      const errorData = await response.json();
      errorMessage = errorData.message || errorData.error || errorMessage;
    } catch {
      errorMessage = response.statusText || errorMessage;
    }

    throw new Error(errorMessage);
  }

  return await response.json();
}
