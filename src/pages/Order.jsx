import React, { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import Voicein from "../Voicein";

const Order = () => {
  const voiceRef = useRef();
  const navigate = useNavigate(); // ✅ navigate 정의
  const [isListening, setIsListening] = useState(false);
  const [voiceText, setVoiceText] = useState(""); // ✅ voiceText 정의


  const handleNext = () => {
    navigate("/location"); // ✅ Complete.jsx 라우트로 이동
  };


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
    flexDirection: "column",     // 세로로 쌓기
    alignItems: "center",
    justifyContent: "center",    // 중앙 정렬
    gap: 4,
    fontWeight: 400,                     // 텍스트 사이 간격
            }}
          >
        
            <br/>
            <span style={{ fontSize: 17, fontWeight: 400 }}>다시 말하기</span>
          </button>
          
          
          
          <button
            className="btn btn-yes"
            onClick={handleNext}   // ✅ 예 버튼 클릭 시 실행
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
    flexDirection: "column",     // 세로로 쌓기
    alignItems: "center",
    justifyContent: "center",    // 중앙 정렬
    gap: 4,
    fontWeight: 400, 
            }}
          >
            다음
            <br/>
      
          </button>


         
        </div>


     <img
  src="call.svg"
  alt="로고"
  style={{
    position: "absolute",
    bottom: "40px", // ✅ 박스 안쪽에서 40px 띄우기
    left: "50%",
    transform: "translateX(-50%)",
    width: "36px",   // 필요시 크기 고정
    height: "38px",  // 필요시 크기 고정
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



