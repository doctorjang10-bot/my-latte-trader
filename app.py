import streamlit as st

# 1. 페이지 기본 설정 및 트레이더 테마
st.set_page_config(page_title="공모주 트레이더 분석기", layout="centered")

# 커스텀 스타일 (냉혹한 시장 분위기 반영)
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #1f77b4; color: white; }
    .latte-box { background-color: #ffffff; padding: 20px; border-radius: 10px; border-left: 5px solid #6f4e37; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 공모주 실전 분석 시스템")
st.write("시장은 감정을 보상하지 않습니다. 오로지 데이터와 결과로만 승부하십시오.")
st.markdown("---")

# 2. 데이터 입력 섹션
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        stock_name = st.text_input("종목명", placeholder="ex) 덕양에너젠")
        listing_price = st.number_input("공모가 (원)", value=10000, step=500)
    with col2:
        dist_amount_raw = st.number_input("유통가능금액 (표 기준/억)", value=700)
        lock_up_rate = st.slider("기관확약률 (%)", 0, 100, 15)

# 3. 트레이더의 독자적 분석 엔진 (로직)
def analyze_stock(name, price, dist, lockup):
    # 로직 1: 최종 유통가능금액 가중치 산출 (확약률에 따른 실질 물량 계산)
    final_dist = dist * (1 - (lockup / 100) * 1.2) # 확약의 실제 영향력 가중치 적용
    
    # 로직 2: 예상 균등 수량 산출 (보수적 접근)
    # 실제로는 API 연동이 필요하나, 현재는 입력값 기반 시뮬레이션
    expected_shares = 2.1 if name == "덕양에너젠" else 1.5 
    
    # 로직 3: 라떼 지수 산출 (잔당 5,000원 기준)
    # 가격대와 유통물량 압박을 고려한 독보적 수익률 예측
    profit_rate = 1.2 if final_dist < 500 else 0.8
    expected_profit = (price * expected_shares) * profit_rate
    latte_count = round(expected_profit / 5000, 1)
    
    return final_dist, expected_shares, latte_count

# 4. 결과 출력
if st.button("데이터 분석 실행"):
    if stock_name:
        f_dist, e_shares, l_count = analyze_stock(stock_name, listing_price, dist_amount_raw, lock_up_rate)
        
        st.markdown(f"### ## {stock_name} 분석 보고서")
        
        # 주요 수치 카드 형식
        st.markdown(f"""
        <div class="latte-box">
            <h4>📈 분석 데이터 및 배정 예측</h4>
            <ul>
                <li><b>최종 유통가능금액</b>: 약 {f_dist:.1f}억 (확약 가중치 반영)</li>
                <li><b>예상 균등 수량</b>: 약 {e_shares}주</li>
                <li><b>수익 효율</b>: {e_shares}주당 라떼 {l_count}잔</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### ☕ 최종 예상 수익 (균등 청약 시)")
        st.success(f"예상 수익금: **라떼 {l_count}잔**")
        
        st.info("※ 본 수치는 트레이더의 독자적 알고리즘으로 산출되었습니다. 시장의 변동성에 주의하십시오.")
    else:
        st.warning("종목명을 입력하십시오.")
