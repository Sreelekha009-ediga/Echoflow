import React, { useState, useRef } from 'react';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';

interface AudioRecorderProps {
  onAudioReady: (blob: Blob) => void;
  disabled?: boolean;
}

export const AudioRecorder: React.FC<AudioRecorderProps> = ({ onAudioReady, disabled }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<BlobPart[]>([]);
  const streamRef = useRef<MediaStream | null>(null);

  const startRecording = async () => {
    try {
      setErrorMsg(null);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        onAudioReady(blob);
        audioChunksRef.current = []; // reset for next recording
        if (streamRef.current) {
          streamRef.current.getTracks().forEach(track => track.stop());
        }
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err: any) {
      console.error('Start failed:', err);
      setErrorMsg(
        err.name === 'NotAllowedError'
          ? 'Microphone permission denied. Allow it in browser settings.'
          : 'Failed to access microphone: ' + err.message
      );
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    setIsRecording(false);
  };

  return (
    <div className="recorder flex flex-col items-center gap-6 mt-6">
      {errorMsg && (
        <p className="text-red-600 bg-red-50 px-6 py-3 rounded-xl text-center max-w-md shadow">
          {errorMsg}
        </p>
      )}

      {isRecording ? (
        <div className="flex flex-col items-center gap-3">
          <div className="w-20 h-20 rounded-full bg-red-500 animate-pulse flex items-center justify-center shadow-lg">
            <MicIcon className="text-white text-5xl" />
          </div>
          <button
            onClick={stopRecording}
            className="px-10 py-5 bg-red-600 hover:bg-red-700 text-white font-bold text-xl rounded-full shadow-xl hover:shadow-2xl transition-all"
          >
            <StopIcon className="inline mr-3 text-2xl" />
            Stop & Analyze
          </button>
        </div>
      ) : (
        <button
          onClick={startRecording}
          disabled={disabled}
          className="px-10 py-5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-bold text-xl rounded-full shadow-xl hover:shadow-2xl transition-all disabled:opacity-50"
        >
          <MicIcon className="inline mr-3 text-2xl" />
          Start Recording
        </button>
      )}

      {/* Optional preview after stop - add if needed */}
    </div>
  );
};