import React, { useState, useEffect, useRef } from "react";

const AddressConfirm = () => {
  const [roadAddress, setRoadAddress] = useState("");
  const [detailAddress, setDetailAddress] = useState("");

  const recognitionRef = useRef(null);
  const micIconRef = useRef(null);

  // 음성인식 초기화
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      if (micIconRef.current) {
        micIconRef.current.style.opacity = 0.3;
        micIconRef.current.style.cursor = "default";
        micIconRef.current.title = "음성 인식 미지원 브라우저";
      }
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = "ko-KR";
    recognition.interimResults = false;

    recognition.onresult = (event) => {
      const detail = event.results[0][0].transcript;
      setDetailAddress(detail);
      alert(`🎤 인식된 상세 주소: ${detail}`);
    };

    recognition.onerror = (e) => {
      alert("음성 인식 오류: " + e.error);
    };

    recognitionRef.current = recognition;
  }, []);

  const getCurrentLocation = () => {
    if (!navigator.geolocation) {
      alert("GPS를 지원하지 않는 브라우저입니다.");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;

        try {
          const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`
          );
          const data = await response.json();

          const address = data.display_name;
          if (address) {
            setRoadAddress(address);
            alert("✅ 도로명 주소 입력 완료!");
          } else {
            alert("주소를 찾을 수 없습니다.");
          }
        } catch (err) {
          alert("API 호출 실패: " + err.message);
        }
      },
      (err) => {
        alert("위치 정보 오류: " + err.message);
      }
    );
  };

  const startRecognition = () => {
    if (recognitionRef.current) {
      recognitionRef.current.start();
    }
  };

  return (
    <div
      style={{
        margin: 0,
        fontFamily: "'Noto Sans KR', sans-serif",
        backgroundColor: "#cde5f9",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        paddingTop: 40,
        height: "812px",
        boxSizing: "border-box",
      }}
    >
      <div
        className="container"
        style={{
          width: 375,
          border: "1px solid #000",
          padding: 23,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
          margin: "0 auto",
          height: "100%",
        }}
      >
        <h2
          style={{
            fontSize: 26,
            fontWeight: 500,
            marginBottom: 20,
            textAlign: "left",
            alignSelf: "flex-start",
          }}
        >
          말씀하신 주소가
          <br />
          맞으신가요?
        </h2>

        {/* 주소 입력 */}
        <div
          className="input-wrapper"
          style={{ width: 300, marginBottom: 12, position: "relative" }}
        >
          <div
            className="input-box"
            style={{
              position: "relative",
              display: "flex",
              alignItems: "center",
              padding: "0 10px",
              gap: 8,
              boxSizing: "border-box",
              height: 40,
              border: "2px solid #0017C8",
              borderRadius: 8,
              color: "#0017C8",
              fontSize: 15,
              backgroundColor: "#fff",
            }}
          >
            <span
              className="input-label"
              style={{
                flexShrink: 0,
                userSelect: "none",
                color: "#0017C8",
                fontSize: 15,
                fontWeight: 400,
                lineHeight: "40px",
                width: 70,
              }}
            >
              주소
            </span>
            <input
              type="text"
              id="roadAddress"
              placeholder="도로명 주소"
              readOnly
              value={roadAddress}
              style={{
                flexGrow: 1,
                border: "none",
                outline: "none",
                fontSize: 15,
                color: "#0017C8",
                background: "transparent",
                paddingRight: 40,
                paddingLeft: 0,
                margin: 0,
              }}
            />
            <img
              src="https://img.icons8.com/ios-filled/50/0017C8/marker.png"
              alt="주소 아이콘"
              className="input-icon"
              id="getLocationIcon"
              title="현재 위치 주소 가져오기"
              onClick={getCurrentLocation}
              style={{
                position: "absolute",
                right: 10,
                width: 24,
                height: 24,
                cursor: "pointer",
              }}
            />
          </div>
        </div>

        {/* 상세주소 입력 */}
        <div
          className="input-wrapper"
          style={{ width: 300, marginBottom: 12, position: "relative" }}
        >
          <div
            className="input-box"
            style={{
              position: "relative",
              display: "flex",
              alignItems: "center",
              padding: "0 10px",
              gap: 8,
              boxSizing: "border-box",
              height: 40,
              border: "2px solid #0017C8",
              borderRadius: 8,
              color: "#0017C8",
              fontSize: 15,
              backgroundColor: "#fff",
            }}
          >
            <span
              className="input-label"
              style={{
                flexShrink: 0,
                userSelect: "none",
                color: "#0017C8",
                fontSize: 15,
                fontWeight: 400,
                lineHeight: "40px",
                width: 70,
              }}
            >
              상세주소
            </span>
            <input
              type="text"
              id="detailAddress"
              placeholder="상세 주소"
              value={detailAddress}
              onChange={(e) => setDetailAddress(e.target.value)}
              style={{
                flexGrow: 1,
                border: "none",
                outline: "none",
                fontSize: 15,
                color: "#0017C8",
                background: "transparent",
                paddingRight: 40,
                paddingLeft: 0,
                margin: 0,
              }}
            />
            <img
              src="https://img.icons8.com/ios-filled/50/0017C8/microphone.png"
              alt="마이크 아이콘"
              className="input-icon"
              id="micIcon"
              title="상세 주소 말하기"
              onClick={startRecognition}
              ref={micIconRef}
              style={{
                position: "absolute",
                right: 10,
                width: 24,
                height: 24,
                cursor: "pointer",
              }}
            />
          </div>
        </div>

        <div className="buttons" style={{ display: "flex", gap: 20, marginTop: 20 }}>
          <button
            className="btn btn-yes"
            style={{
              width: 122,
              height: 76,
              flexShrink: 0,
              backgroundColor: "#00b32d",
              border: "none",
              borderRadius: 8,
              fontSize: 30,
              fontWeight: "bold",
              color: "#fff",
              cursor: "pointer",
            }}
          >
            예
            <br />
            <span style={{ fontSize: 17, fontWeight: 400 }}>주문 완료하기</span>
          </button>
          <button
            className="btn btn-no"
            style={{
              width: 122,
              height: 76,
              flexShrink: 0,
              backgroundColor: "#ff3b30",
              border: "none",
              borderRadius: 8,
              fontSize: 30,
              fontWeight: "bold",
              color: "#fff",
              cursor: "pointer",
            }}
          >
            아니오
            <br />
            <span style={{ fontSize: 17, fontWeight: 400 }}>다시 말하기</span>
          </button>
        </div>

        <div className="mic-footer" style={{ marginTop: 40 }}>
          <img src="call.svg" alt="전화 아이콘" style={{ width: 30, height: 30, opacity: 0.6 }} />
        </div>
      </div>
    </div>
  );
};

export default AddressConfirm;
