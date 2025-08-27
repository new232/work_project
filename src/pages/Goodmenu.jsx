import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";

const Goodmenu = () => {
  const [orders, setOrders] = useState([]);
  const [total, setTotal] = useState(0);
  const [roadAddress, setRoadAddress] = useState("");
  const [detailAddress, setDetailAddress] = useState("");
  const navigate = useNavigate();
  const location = useLocation();

  const handlePrev = () => navigate("/order"); // 이전은 Order
  const handleNext = () => {
    navigate("/basket", {
      state: {
        orders,
        totalPrice: total,
        roadAddress,
        detailAddress,
      },
    });
  };

  // Location에서 전달된 주소 가져오기
  useEffect(() => {
    if (location.state) {
      setRoadAddress(location.state.roadAddress || "");
      setDetailAddress(location.state.detailAddress || "");
    }
  }, [location.state]);

  // 백엔드에서 추천 메뉴 불러오기
  useEffect(() => {
    const fetchRecommendedMenus = async () => {
      try {
        const response = await fetch("/api/recommend", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            voiceText: location.state?.voiceText || "",
          }),
        });
        const data = await response.json();

        const recommendedOrders = data.data.items.map(item => ({
          storeName: data.data.store.name,
          menu: item.name,
          quantity: item.quantity,
          price: item.price,
        }));

        setOrders(recommendedOrders);
        setTotal(data.data.total_price);

      } catch (err) {
        console.error("추천 메뉴 불러오기 실패:", err);
      }
    };

    fetchRecommendedMenus();
  }, [location.state?.voiceText]);

// ✅ orders나 total이 바뀌면 TTS로 읽어주기
  useEffect(() => {
    if (orders.length === 0) return;

    // 읽을 내용 만들기
    let speechText = `추천 메뉴입니다. `;
    orders.forEach((order, index) => {
      speechText += `${order.storeName}에서 ${order.menu} ${order.quantity}개 ${order.price}원, `;
    });
    speechText += `총 금액은 ${total}원입니다.`;

    const utterance = new SpeechSynthesisUtterance(speechText);
    utterance.lang = "ko-KR";
    // 이전 발화가 있으면 멈추고 새로 읽기
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);

  }, [orders, total]);


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
          fontWeight: 400,
          fontSize: 24,
          lineHeight: "31px",
          alignSelf: "flex-start",
          textAlign: "left",
        }}
      >
        추천 메뉴로
        <br />
        주문할까요?
      </div>

      <div
        style={{
          width: "335px",
          height: "292px",
          border: "3px solid #2139ED",
          borderTop: "none",
          borderRadius: "20px",
          boxShadow: "0px 6px 6px rgba(0,0,0,0.25)",
          overflow: "hidden",
          backgroundColor: "#CDE5F9",
        }}
      >
        <div
          style={{
            height: "36px",
            background: "#2139ED",
            borderRadius: "20px 20px 0 0",
            display: "grid",
            gridTemplateColumns: "1.4fr 1fr 0.8fr 0.8fr",
            alignItems: "center",
            textAlign: "center",
            color: "white",
            fontSize: 17,
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
            gridTemplateRows: `repeat(${orders.length}, 1fr)`,
            height: "256px",
            backgroundColor: "#CDE5F9",
          }}
        >
          {orders.map((order, index) => (
            <React.Fragment key={index}>
              <div
                style={{
                  border: "0.5px solid #2139ED",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                {order.storeName}
              </div>
              <div
                style={{
                  border: "0.5px solid #2139ED",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                {order.menu}
              </div>
              <div
                style={{
                  border: "0.5px solid #2139ED",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                {order.quantity}
              </div>
              <div
                style={{
                  border: "0.5px solid #2139ED",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                {order.price}
              </div>
            </React.Fragment>
          ))}
        </div>
      </div>

      <div
        style={{
          width: "100%",
          height: "40px",
          display: "flex",
          border: "2px solid #0017C8",
          borderRadius: "6px",
          overflow: "hidden",
          backgroundColor: "#CDE5F9",
        }}
      >
        <div
          style={{
            backgroundColor: "#2139ED",
            color: "white",
            padding: "10px 20px",
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
        <div
          style={{
            flex: 1,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          {total}원
        </div>
      </div>

      <div className="buttons" style={{ display: "flex", gap: 20, marginTop: 20 }}>
        <button
          className="btn btn-no"
          onClick={handleNext}
          style={{
            width: 122,
            height: 76,
            backgroundColor: "#00b32d",
            border: "none",
            borderRadius: 8,
            fontSize: 30,
            color: "#fff",
            cursor: "pointer",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          예
        </button>

        <button
          className="btn btn-yes"
          onClick={handlePrev}
          style={{
            width: 122,
            height: 76,
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
          }}
        >
          아니오
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
    </div>
  );
};

export default Goodmenu;
