import React, { useState, useRef } from 'react';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';
import { ReactMic } from 'react-mic';

interface AudioRecorderProps {
  onAudioReady: (blob: Blob) => void;
  disabled?: boolean;
}

export const AudioRecorder: React.FC<AudioRecorderProps> = ({ onAudioReady, disabled }) => {
  const [recording, setRecording] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);

  const onStop = (recordedBlob: { blob: Blob }) => {
    const url = URL.createObjectURL(recordedBlob.blob);
    setAudioUrl(url);
    onAudioReady(recordedBlob.blob);
  };

  return (
    <div className="recorder">
      <ReactMic
        record={recording}
        className="sound-wave"
        onStop={onStop}
        strokeColor="#000000"
        backgroundColor="#FF4081"
      />

      {!recording ? (
        <button onClick={() => setRecording(true)} disabled={disabled}>
          <MicIcon /> Start Recording
        </button>
      ) : (
        <button onClick={() => setRecording(false)}>
          <StopIcon /> Stop & Analyze
        </button>
      )}

      {audioUrl && (
        <audio controls src={audioUrl}>
          Your browser does not support the audio element.
        </audio>
      )}
    </div>
  );
};