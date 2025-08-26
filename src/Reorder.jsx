import React from 'react';

const Reorder = () => {
  return (
    <div
      style={{
        margin: 0,
        fontFamily: "'Noto Sans KR', sans-serif",
        backgroundColor: '#CDE5F9',
        width: '375px',
        height: '812px',
        marginLeft: 'auto',
        marginRight: 'auto',
        paddingTop: '80px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '42px',
        padding: '294px 23px 303px 23px',
        boxSizing: 'border-box',
        border: '1px solid #000',
        textAlign: 'center',
      }}
    >
      <span
        style={{
          fontSize: '26px',
          fontWeight: 500,
          color: '#000000',
          marginBottom: '60px',
        }}
      >
        <span style={{ fontWeight: 500 }}>
          다시 한 번 버튼을 누르고
          <br />
          메뉴를 말씀해주세요
        </span>
      </span>

      <button
        style={{
          marginTop: '60px',
          width: '335px',
          height: '224px',
          borderRadius: '30px',
          border: '5px solid #0017C8',
          background: '#2139ED',
          boxShadow: '0 4px 4px 0 rgba(0, 0, 0, 0.25)',
          color: '#FFF',
          textAlign: 'center',
          fontFamily: 'Inter, sans-serif',
          fontSize: '60px',
          fontStyle: 'normal',
          fontWeight: 400,
          lineHeight: 'normal',
          marginBottom: '38px',
        }}
      >
        <img
          src="mike.svg"
          alt="마이크 아이콘"
          style={{
            marginBottom: '10px',
          }}
        />
        <br />
        주문하기
      </button>

      <img
        src="call.svg"
        alt="전화 아이콘"
        style={{
          width: '36px',
          height: '38px',
          flexShrink: 0,
        }}
      />
    </div>
  );
};

export default Reorder;

