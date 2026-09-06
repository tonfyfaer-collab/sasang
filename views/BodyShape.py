# -*- coding: utf-8 -*-
import streamlit as st
from core.questionnaire import QUESTIONS

def render_body_shape():
    st.subheader("🧍 Step 1. 체형 및 외모 진단")
    st.write("첫 번째 영역은 체형과 살집, 골격 상태를 통해 타고난 장부의 기상을 판별합니다.")
    st.divider()
    
    # Q1 and Q5
    target_q_ids = [1, 5]
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
        selected_option["weight"] = q["weight"] # Ensure weight passes along
        st.session_state.answers[q_id] = selected_option
        st.write("")

    col_back, col_next = st.columns(2)
    with col_back:
        if st.button("⬅️ 이전 화면으로", use_container_width=True):
            st.session_state.step = "intro"
            st.rerun()
    with col_next:
        if st.button("다음 단계로 이동 ➡️", type="primary", use_container_width=True):
            st.session_state.step = "personality"
            st.rerun()
