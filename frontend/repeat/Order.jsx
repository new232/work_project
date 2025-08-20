import React, { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import Voicein from "../Voicein";

const Order = () => {
  const voiceRef = useRef();
  const navigate = useNavigate(); // ✅ navigate 정의
  const [isListening, setIsListening] = useState(false);
  const [voiceText, setVoiceText] = useState(""); // ✅ voiceText 정의

  const handleStartRecording = () => { // ✅ handleStartRecording 정의
    voiceRef.current?.startListening();
  };

  const handleVoiceResult = (text) => {
    setVoiceText(text);
    console.log("받은 텍스트:", text);
  };


// 백엔드로 전송
/*    fetch("http://localhost:5000/api/voice", { // 백엔드 주소 변경 필요//
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: text }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("서버 응답:", data);
      })
      .catch((error) => {
        console.error("전송 실패:", error);
      });
  };*/



  const handleListeningChange = (listening) => {
    setIsListening(listening);
  };

  useEffect(() => { // ✅ useEffect import 추가
    if (!isListening && voiceText) {
      navigate("/location", { state: { orderText: voiceText } });
    }
  }, [isListening, voiceText, navigate]); // ✅ 의존성 배열 수정

  return (
    <div
      style={{
        width: "375px",
        height: "812px",
        margin: "0 auto",
        textAlign: "center",
        backgroundColor: "#CDE5F9",
        fontFamily: "'Noto Sans KR', sans-serif",
        position: "relative",
        border: "1px solid #000",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "294px 23px 303px 23px",
        boxSizing: "border-box",
        gap: "42px",
      }}
    >
      <span
        style={{
          fontFamily: "'Inter', sans-serif",
          fontStyle: "normal",
          fontWeight: 400,
          fontSize: "26px",
          lineHeight: "36px",
          textAlign: "center",
          color: "#000000",
  
          margin: 0,
          textShadow: "none"
        }}
      >
        <div style={{ textAlign: "left" }}>
          아래 버튼을 누르고
          <br />
          원하시는 메뉴를 말씀해주세요
        </div>
      </span>

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

      <p style={{ marginTop: "20px", color: "#333", fontSize: "18px" }}>
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

      <img
        src="call.svg"
        alt="로고"
        style={{
          position: "absolute",
          bottom: "-0.001px",
          left: "50%",
          transform: "translateX(-50%)",
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






