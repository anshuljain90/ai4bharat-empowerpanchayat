import React, { useState, useRef } from 'react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
const MOM_API_URL = `${BACKEND_URL}/mom-api`;

/**
 * ReadAloudButton - Accessibility component for TTS using Amazon Polly.
 * Usage: <ReadAloudButton text="Text to read" language="hi" />
 */
const ReadAloudButton = ({ text, language = 'hi', size = 'small', label }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const audioRef = useRef(null);

  const handleSpeak = async () => {
    if (isPlaying && audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setIsPlaying(false);
      return;
    }

    if (!text || !text.trim()) return;

    setIsLoading(true);
    try {
      const response = await fetch(`${MOM_API_URL}/tts/speak`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text.substring(0, 3000), language }),
      });

      if (!response.ok) throw new Error('TTS failed');

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);

      if (audioRef.current) {
        audioRef.current.pause();
      }

      const audio = new Audio(url);
      audioRef.current = audio;

      audio.onended = () => {
        setIsPlaying(false);
        URL.revokeObjectURL(url);
      };

      audio.onerror = () => {
        setIsPlaying(false);
        URL.revokeObjectURL(url);
      };

      await audio.play();
      setIsPlaying(true);
    } catch (error) {
      console.error('TTS error:', error);
      setIsPlaying(false);
    } finally {
      setIsLoading(false);
    }
  };

  const buttonStyle = {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '4px',
    padding: size === 'small' ? '4px 8px' : '8px 16px',
    fontSize: size === 'small' ? '12px' : '14px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    background: isPlaying ? '#e8f5e9' : '#fff',
    cursor: isLoading ? 'wait' : 'pointer',
    opacity: isLoading ? 0.7 : 1,
  };

  return (
    <button
      onClick={handleSpeak}
      disabled={isLoading || !text}
      style={buttonStyle}
      title={isPlaying ? 'Stop' : 'Read aloud'}
      aria-label={isPlaying ? 'Stop reading' : 'Read aloud'}
    >
      {isLoading ? '...' : isPlaying ? '⏹' : '🔊'}
      {label && <span>{label}</span>}
    </button>
  );
};

export default ReadAloudButton;
