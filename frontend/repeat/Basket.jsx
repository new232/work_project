import React, { useEffect, useState } from "react";

const OrderSummary = () => {
  const [orders, setOrders] = useState([]); // 주문 데이터 배열
  const [total, setTotal] = useState(0);   // 총 금액

  useEffect(() => {
    // 백엔드에서 주문 데이터 받아오기
    /*
    const fetchOrders = async () => {
      try {
        const response = await fetch("/api/orders"); // 백엔드 주문 API
        const data = await response.json();

        setOrders(data);

        // 총 금액 계산
        const totalAmount = data.reduce(
          (sum, order) => sum + order.price * order.quantity,
          0
        );
        setTotal(totalAmount);
      } catch (err) {
        console.error("주문 데이터를 가져오는데 실패했습니다.", err);
      }
    };

    fetchOrders();
    */

    // ✅ 더미 데이터 (UI 확인용)
    const dummyOrders = [
      { storeName: "김밥천국", menu: "김밥", quantity: 2, price: 3000 },
      { storeName: "버거킹", menu: "와퍼", quantity: 1, price: 6500 },
    ];
    setOrders(dummyOrders);
    setTotal(dummyOrders.reduce((sum, order) => sum + order.price * order.quantity, 0));
  }, []);

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
        주문하신 내용은
        <br />
        다음과 같습니다
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
            gridTemplateRows: `repeat(${orders.length}, 1fr)`,
            height: "256px",
            backgroundColor: "#CDE5F9",
          }}
        >
          {orders.map((order, index) => (
            <React.Fragment key={index}>
              <div style={{ border: "0.5px solid #2139ED", display: "flex", alignItems: "center", justifyContent: "center" }}>
                {order.storeName}
              </div>
              <div style={{ border: "0.5px solid #2139ED", display: "flex", alignItems: "center", justifyContent: "center" }}>
                {order.menu}
              </div>
              <div style={{ border: "0.5px solid #2139ED", display: "flex", alignItems: "center", justifyContent: "center" }}>
                {order.quantity}
              </div>
              <div style={{ border: "0.5px solid #2139ED", display: "flex", alignItems: "center", justifyContent: "center" }}>
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

      <img
        src="call.svg"
        alt="로고 이미지"
        style={{
          position: "absolute",
          top: "670px",
          left: "50%",
          transform: "translateX(-50%)",
          width: "36px",
          height: "38px",
        }}
      />
    </div>
  );
};

export default OrderSummary;