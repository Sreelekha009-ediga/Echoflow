import React, { useState } from 'react';
import { AudioRecorder } from './components/AudioRecorder';
import { ResultDisplay } from './components/ResultDisplay';
import { analyzeAudio } from './api';
import './App.css';

function App() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAudioReady = async (audioBlob: Blob) => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyzeAudio(audioBlob);
      setResult(data);
    } catch (err) {
      setError('Failed to analyze audio. Is backend running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>ECHOFLOW</h1>
      <p>Speech → Text → Emotion → Grammar & Translation</p>

      <AudioRecorder onAudioReady={handleAudioReady} disabled={loading} />

      {loading && <div className="loading">Analyzing...</div>}
      {error && <div className="error">{error}</div>}

      {result && <ResultDisplay result={result} />}
    </div>
  );
}

export default App;