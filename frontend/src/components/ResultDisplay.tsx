// src/components/ResultDisplay.tsx
import React from 'react';

interface Result {
  transcribed_text: string;
  emotion: string;
  confidence?: number;
  corrected_text?: string;
  translated_text?: string;
  model_used?: string;
}

interface Props {
  result: Result | null;
}

const getEmotionColor = (emotion: string) => {
  const lower = emotion.toLowerCase();
  if (lower.includes('joy') || lower.includes('love')) return 'text-green-600 dark:text-green-400';
  if (lower.includes('sadness')) return 'text-blue-600 dark:text-blue-400';
  if (lower.includes('anger')) return 'text-red-600 dark:text-red-400';
  if (lower.includes('fear')) return 'text-orange-600 dark:text-orange-400';
  if (lower.includes('surprise')) return 'text-purple-600 dark:text-purple-400';
  return 'text-gray-800 dark:text-gray-200';
};

export const ResultDisplay: React.FC<Props> = ({ result }) => {
  if (!result) return null;

  return (
    <div className="results grid grid-cols-1 md:grid-cols-2 gap-6 mt-10 animate-fade-in">
      {/* Transcribed Text Card */}
      <div className="card bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-all">
        <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-3">Transcribed Text</h3>
        <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap min-h-[80px]">
          {result.transcribed_text || '—'}
        </p>
      </div>

      {/* Detected Emotion Card */}
      <div className="card bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-all">
        <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-3">Detected Emotion</h3>
        <p className={`text-4xl font-extrabold ${getEmotionColor(result.emotion)}`}>
          {result.emotion}
          {result.confidence !== undefined && (
            <span className="text-2xl ml-3 opacity-80">
              ({(result.confidence * 100).toFixed(1)}%)
            </span>
          )}
        </p>
      </div>

      {/* Corrected Text (if exists) */}
      {result.corrected_text && (
        <div className="card bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-all md:col-span-2">
          <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-3">Grammar Corrected</h3>
          <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
            {result.corrected_text}
          </p>
        </div>
      )}

      {/* Translated Text */}
      {result.translated_text && (
        <div className="card bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-all md:col-span-2">
          <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100 mb-3">Translated</h3>
          <p className="text-gray-700 dark:text-gray-300 whitespace-pre-line leading-relaxed">
            {result.translated_text}
          </p>
        </div>
      )}

      {/* Model Used */}
      {result.model_used && (
        <div className="card bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-gray-800 dark:to-gray-700 p-5 rounded-2xl shadow-md border border-indigo-100 dark:border-gray-600 text-center">
          <h4 className="text-lg font-semibold text-indigo-700 dark:text-indigo-300">Model used</h4>
          <p className="text-xl font-bold text-indigo-800 dark:text-indigo-200 uppercase tracking-wide">
            {result.model_used}
          </p>
        </div>
      )}
    </div>
  );
};