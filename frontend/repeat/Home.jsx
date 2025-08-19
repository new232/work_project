import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/order"); // 3초 뒤 자동 이동
    }, 3000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div
      style={{
        fontFamily: "sans-serif",
        margin: 0,
        padding: 20,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        backgroundColor: "#CDE5F9",
        minHeight: "100vh",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          display: "flex",
          width: "375px",
          height: "812px",
          padding: "294px 23px 303px 23px",
          flexDirection: "column",
          alignItems: "center",
          border: "1px solid #000",
          boxSizing: "border-box",
          backgroundColor: "#CDE5F9",
        }}
      >
        <h3
          style={{
            fontFamily: "'Inter', sans-serif",
            fontStyle: "normal",
            fontWeight: 400,
            fontSize: "26px",
            lineHeight: "36px",
            textAlign: "center",
            color: "#000000",
            textShadow: "-1px 2px 4px rgba(0, 0, 0, 0.25)",
            margin: 0
          }}
        >
         
          음성인식 자동 주문 서비스
          <br />
           <span className="bold-text">114리턴즈</span>
        </h3>
  


        <img
          src="/Vector.svg"
          alt="Vector"
          style={{
            width: "130px",
            height: "130px",
            backgroundColor: "#CDE5F9",
          }}
        />
      </div>
    </div>
  );
};

export default Home;


