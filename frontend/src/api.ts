import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',   // ← most common uvicorn port
  // baseURL: 'http://localhost:8000', // alternative
  // For production later: use env variable → import.meta.env.VITE_API_URL
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export const analyzeAudio = async (audioBlob: Blob, model: string = 'cnn') => {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.webm');
  formData.append('model', model);           // ← send model choice

  try {
    const response = await api.post('/transcribe', formData);  // ← correct endpoint
    return response.data;
  } catch (error: any) {
    console.error('API error:', error.response?.data || error.message);
    throw error;
  }
};