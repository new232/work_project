import React, { useState, useRef, forwardRef, useImperativeHandle } from "react";

const Voicein = forwardRef((props, ref) => {
  const recognitionRef = useRef(null);

  useImperativeHandle(ref, () => ({
    startListening: () => {
      if (recognitionRef.current) {
        recognitionRef.current.start();
      } else {
        handleVoice();
      }
    },
  }));

  const handleVoice = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("이 브라우저는 음성 인식을 지원하지 않습니다.");
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "ko-KR";
    recognition.interimResults = false;

    recognition.onstart = () => {
      props.onListeningChange?.(true);
    };

    recognition.onend = () => {
      props.onListeningChange?.(false);
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      props.onResult?.(transcript);
    };

    recognition.onerror = (event) => {
      console.error("❌ 오류 발생:", event.error);
      alert("음성 인식 중 오류가 발생했습니다.");
      props.onListeningChange?.(false);
    };

    recognition.start();
    recognitionRef.current = recognition;
  };

  return null; // 아무것도 렌더링하지 않음!
});

export default Voicein;




