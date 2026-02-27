import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000', // change to your backend URL / production later
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export const analyzeAudio = async (audioBlob: Blob) => {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.webm');

  try {
    const response = await api.post('/analyze', formData);
    return response.data;
  } catch (error) {
    console.error('API error:', error);
    throw error;
  }
};