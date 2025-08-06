import React from "react";

const Home = () => {
  return (
    <div
      style={{
        fontFamily: "sans-serif",
        margin: 0,
        padding: 20,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        backgroundColor: "#f9f9f9",
        height: "100vh",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          display: "flex",
          width: 375,
          height: 812,
          padding: "294px 23px 303px 23px",
          flexDirection: "column",
          alignItems: "center",
          border: "1px solid #000",
          boxSizing: "border-box",
          backgroundColor: "white",
          // gap 대신 각 요소에 margin-bottom 줌
        }}
      >
        <h3
          style={{
            padding: "20px 40px",
            borderRadius: 12,
            color: "black",
            fontSize: "24px", // 2vw 대신 px로 고정 (vw는 반응형이라 다름)
            fontWeight: "bold",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            textAlign: "center",
            margin: 0,
            width: "50vw",
            lineHeight: 1.2,
            marginBottom: 42, // gap 대신
          }}
        >
          음성인식 자동 주문 서비스
          </br>
          114 리턴즈
        </h3>

        <img
          src="Vector.svg"
          alt="Vector"
          style={{ width: 130, height: 130 }}
        />
      </div>
    </div>
  );
};

export default Home;
