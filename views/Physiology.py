# -*- coding: utf-8 -*-
import streamlit as st
from core.questionnaire import QUESTIONS

def render_physiology():
    st.subheader("🌡️ Step 3. 평소 생리 소증 진단")
    st.write("세 번째 영역은 한의학에서 건강 판독의 가장 중요 지표인 땀, 대소변, 소화 상태를 면밀히 분석합니다. (가중치 1.5배 적용)")
    st.divider()
    
    # Q3, Q9, Q10, Q11, Q12
    target_q_ids = [3, 9, 10, 11, 12]
    for q_id in target_q_ids:
        q = next(item for item in QUESTIONS if item["id"] == q_id)
        st.markdown(f"**Q{q['id']}. [{q['category']}] {q['question']}**")
        options_texts = [opt["text"] for opt in q["options"]]
        
        # Get previous selection if any
        prev_idx = 0
        if q_id in st.session_state.answers:
            prev_val = st.session_state.answers[q_id]["text"]
            if prev_val in options_texts:
                prev_idx = options_texts.index(prev_val)
                
        choice = st.radio(
            label=f"q_{q_id}_label",
            options=options_texts,
            index=prev_idx,
            key=f"q_{q_id}",
            label_visibility="collapsed"
        )
        selected_option = next(opt for opt in q["options"] if opt["text"] == choice)
        selected_option["weight"] = q["weight"]
        st.session_state.answers[q_id] = selected_option
        st.write("")

    col_back, col_next = st.columns(2)
    with col_back:
        if st.button("⬅️ 이전 화면으로", use_container_width=True):
            st.session_state.step = "personality"
            st.rerun()
    with col_next:
        if st.button("다음 단계로 이동 ➡️", type="primary", use_container_width=True):
            st.session_state.step = "symptoms"
            st.rerun()
