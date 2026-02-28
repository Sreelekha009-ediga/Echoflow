import React, { useState } from 'react';
import { AudioRecorder } from './components/AudioRecorder';
import { ResultDisplay } from './components/ResultDisplay';
import { analyzeAudio } from './api';
import './App.css';

function App() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedModel, setSelectedModel] = useState<'cnn' | 'lr' | 'knn'>('cnn');

  const handleAudioReady = async (audioBlob: Blob) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeAudio(audioBlob, selectedModel);
      setResult(data);
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
        'Failed to analyze audio. Check console + backend logs.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      // In App.tsx - wrap content
<div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-950 flex items-center justify-center p-6">
  <div className="w-full max-w-3xl bg-white/80 dark:bg-gray-800/80 backdrop-blur-lg rounded-3xl shadow-2xl p-10 border border-gray-200/50 dark:border-gray-700/50">
    <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-indigo-600 mb-4 text-center">
      ECHOFLOW
    </h1>
    
    <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 text-center">
      Speech → Text → Emotion Detection → Grammar & Translation
    </p>

    {/* Model selector */}
    <div className="flex justify-center mb-10">
      <div className="inline-flex items-center gap-3 bg-white dark:bg-gray-700 px-6 py-3 rounded-full shadow-md">
        <label className="font-medium text-gray-700 dark:text-gray-200">Model:</label>
        <select
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value as any)}
          disabled={loading}
          className="bg-transparent border-none focus:ring-0 text-purple-700 dark:text-purple-300 font-semibold cursor-pointer"
        >
          <option value="cnn">CNN (best accuracy)</option>
          <option value="lr">Logistic Regression (fast)</option>
          <option value="knn">KNN</option>
        </select>
      </div>
    </div>

    <AudioRecorder onAudioReady={handleAudioReady} disabled={loading} />

    {loading && (
      <div className="mt-10 flex flex-col items-center gap-4">
        <div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-lg font-medium text-purple-700 dark:text-purple-300">Analyzing your voice...</p>
      </div>
    )}

    {error && <p className="mt-6 text-red-600 text-center font-medium">{error}</p>}

    {result && (
      <div className="mt-12 animate-fade-in">
        <ResultDisplay result={result} />
      </div>
    )}
  </div>
</div>
    </div>
  );
}

export default App;