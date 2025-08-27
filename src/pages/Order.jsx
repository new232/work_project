import React, { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import Voicein from "../Voicein";

const Order = () => {
  const [roadAddress, setRoadAddress] = useState("");
  const [detailAddress, setDetailAddress] = useState("");
  const [voiceText, setVoiceText] = useState(""); // 음성 텍스트
  const [isListening, setIsListening] = useState(false);

  const voiceRef = useRef();
  const navigate = useNavigate();

  // TTS 실행 함수
  const speak = (text) => {
    if (!text) return;
    window.speechSynthesis.cancel(); // 이전 음성 중단
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "ko-KR";
    window.speechSynthesis.speak(utterance);
  };

  // voiceText가 바뀔 때마다 바로 TTS 실행
  useEffect(() => {
    if (voiceText) {
      speak(voiceText);
    }
  }, [voiceText]);

  const handleNext = () => {
    navigate("/goodmenu", { state: { roadAddress, detailAddress } });
  };

  const handleStartRecording = () => {
    voiceRef.current?.startListening();
  };

  const handleVoiceResult = (text) => {
    setVoiceText(text); // 텍스트 업데이트 → TTS 자동 실행
    console.log("받은 텍스트:", text);
  };

  const handleListeningChange = (listening) => {
    setIsListening(listening);
  };

  return (
    <div
      style={{
        width: "375px",
        height: "812px",
        margin: "0 auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "42px",
        padding: "50px 23px",
        textAlign: "center",
        border: "1px solid #000",
        boxSizing: "border-box",
        position: "relative",
        fontFamily: "'Noto Sans KR', sans-serif",
        backgroundColor: "#CDE5F9",
      }}
    >
      <div
        style={{
          color: "#000",
          fontFamily: "'Noto Sans KR', sans-serif",
          fontWeight: 400,
          fontSize: 24,
          lineHeight: "31px",
          alignSelf: "flex-start",
          textAlign: "left",
        }}
      >
        아래 버튼을 누르고
        <br />
        원하시는 메뉴를 말씀해주세요
      </div>

      {isListening && (
        <p
          style={{
            fontFamily: "'Noto Sans KR', sans-serif",
            color: "#2139ED",
            fontWeight: "bold",
            fontSize: "24px",
            marginBottom: "-30px",
          }}
        >
          🎙 녹음 중입니다...
        </p>
      )}

      <p style={{ marginTop: "20px", color: "#333", fontSize: "24px" }}>
        내용: {voiceText}
      </p>

      <button
        onClick={handleStartRecording}
        style={{
          position: "relative",
          marginTop: "36px",
          width: "335px",
          height: "224px",
          borderRadius: "30px",
          border: "5px solid #0017C8",
          background: "#2139ED",
          boxShadow: "0 4px 4px rgba(0, 0, 0, 0.25)",
          color: "#FFF",
          textAlign: "center",
          fontFamily: "Inter, sans-serif",
          fontSize: "60px",
          fontWeight: "400",
          lineHeight: "normal",
        }}
      >
        <img src="/mike.svg" alt="마이크 아이콘" style={{ marginBottom: "10px" }} />
        <br />
        주문하기
      </button>

      <div className="buttons" style={{ display: "flex", gap: 20, marginTop: 20 }}>
        <button
          className="btn btn-no"
          style={{
            fontFamily: "'Noto Sans KR', sans-serif",
            width: 122,
            height: 76,
            flexShrink: 0,
            backgroundColor: "#CDE5F9",
            border: "none",
            borderRadius: 8,
            fontSize: 30,
            color: "#CDE5F9",
            cursor: "pointer",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            gap: 4,
            fontWeight: 400,
          }}
        >
          <br />
          <span style={{ fontSize: 17, fontWeight: 400 }}>다시 말하기</span>
        </button>

        <button
          className="btn btn-yes"
          onClick={handleNext}
          style={{
            fontFamily: "'Noto Sans KR', sans-serif",
            width: 122,
            height: 76,
            flexShrink: 0,
            backgroundColor: "#ff3b30",
            border: "none",
            borderRadius: 8,
            fontSize: 30,
            color: "#fff",
            cursor: "pointer",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            gap: 4,
            fontWeight: 400,
          }}
        >
          다음
          <br />
        </button>
      </div>

      <img
        src="call.svg"
        alt="로고"
        style={{
          position: "absolute",
          bottom: "40px",
          left: "50%",
          transform: "translateX(-50%)",
          width: "36px",
          height: "38px",
        }}
      />

      <Voicein
        ref={voiceRef}
        onResult={handleVoiceResult}
        onListeningChange={handleListeningChange}
      />
    </div>
  );
};

export default Order;




