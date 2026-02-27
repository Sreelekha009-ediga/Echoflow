import React from 'react';

interface Result {
  text: string;
  emotion: string;
  corrected_text?: string;
  translated_text?: string;
}

interface Props {
  result: Result;
}

export const ResultDisplay: React.FC<Props> = ({ result }) => {
  return (
    <div className="results">
      <div className="card">
        <h3>Transcribed Text</h3>
        <p>{result.text || '—'}</p>
      </div>

      <div className="card">
        <h3>Detected Emotion</h3>
        <p className={`emotion ${result.emotion.toLowerCase()}`}>
          {result.emotion}
        </p>
      </div>

      {result.corrected_text && (
        <div className="card">
          <h3>Grammar Corrected</h3>
          <p>{result.corrected_text}</p>
        </div>
      )}

      {result.translated_text && (
        <div className="card">
          <h3>Translated (e.g. to Hindi)</h3>
          <p>{result.translated_text}</p>
        </div>
      )}
    </div>
  );
};