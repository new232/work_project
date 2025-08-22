import React from "react";

const Complete = ({ roadAddress, detailAddress }) => {
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
        주문이
        <br />
        완료되었습니다!
      </div>

      <div
        style={{
          width: "335px",
          height: "292px",
          border: "3px solid #2139ED",
          borderTop: "none",
          borderRadius: "20px",
          boxShadow: "0px 6px 6px rgba(0, 0, 0, 0.25)",
          overflow: "hidden",
          backgroundColor: "#CDE5F9",
        }}
      >
        <div
          style={{
            height: "36px",
            background: "#2139ED",
            borderRadius: "20px 20px 0 0",
            boxShadow: "inset 1px 4px 4px 1px #0017C8",
            display: "grid",
            gridTemplateColumns: "1.4fr 1fr 0.8fr 0.8fr",
            alignItems: "center",
            textAlign: "center",
            color: "white",
            fontSize: 17,
            fontFamily: "'Inter', sans-serif",
            borderBottom: "1px solid #2139ED",
          }}
        >
          <div>가게명</div>
          <div>메뉴</div>
          <div>수량</div>
          <div>가격</div>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1.4fr 1fr 0.8fr 0.8fr",
            gridTemplateRows: `repeat(4, 64px)`,
            backgroundColor: "#CDE5F9",
          }}
        >
          {Array(16).fill("").map((_, idx) => (
            <div
              key={idx}
              style={{
                border: "0.5px solid #2139ED",
                boxSizing: "border-box",
              }}
            />
          ))}
        </div>
      </div>

      {/* 총 금액 + 주소 묶음 */}
      <div
        style={{
          width: "100%",
          display: "flex",
          flexDirection: "column",
          gap: "10px",
        }}
      >
        <div
          style={{
            width: "100%",
            height: "40px",
            display: "flex",
            border: "2px solid #0017C8",
            borderRadius: "5px",
            overflow: "hidden",
            backgroundColor: "#CDE5F9",
          }}
        >
          <div
            style={{
              backgroundColor: "#2139ED",
              color: "white",
              width: "71px",
              fontWeight: "bold",
              fontSize: 16,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              borderRight: "2px solid #0017C8",
            }}
          >
            총 금액
          </div>
          <div style={{ flex: 1 }}></div>
        </div>

        <div
          style={{
            width: "100%",
            height: "80px",
            display: "flex",
            border: "2px solid #0017C8",
            borderRadius: "5px",
            overflow: "hidden",
            backgroundColor: "#CDE5F9",
          }}
        >
          <div
            style={{
              backgroundColor: "#2139ED",
              color: "white",
              width: "71px",
              fontWeight: "bold",
              fontSize: 16,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              borderRight: "2px solid #0017C8",
            }}
          >
            주소
          </div>
          <div style={{ flex: 1, padding: "4px" }}>
            {roadAddress}
            <br />
            {detailAddress}
          </div>
        </div>
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

    </div>
  );
};

export default Complete;
