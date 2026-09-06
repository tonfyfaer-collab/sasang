# -*- coding: utf-8 -*-
import streamlit as st
from core.questionnaire import QUESTIONS

def render_personality():
    st.subheader("🧠 Step 2. 성격 및 기질 진단")
    st.write("두 번째 영역은 대인관계 방식과 내적 감정 상태, 추진 스타일을 기반으로 장부의 심욕을 분석합니다.")
    st.divider()
    
    # Q2, Q6, Q7, Q8
    target_q_ids = [2, 6, 7, 8]
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
            st.session_state.step = "bodyshape"
            st.rerun()
    with col_next:
        if st.button("다음 단계로 이동 ➡️", type="primary", use_container_width=True):
            st.session_state.step = "physiology"
            st.rerun()
