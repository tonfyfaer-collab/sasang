# -*- coding: utf-8 -*-
import streamlit as st
from core.questionnaire import QUESTIONS
from core.scoring import calculate_scores

def render_symptoms():
    st.subheader("🚨 Step 4. 특이 병증 및 냉열 감각 진단")
    st.write("마지막 단계로, 몸이 지치거나 급성 병증이 유발되었을 때의 고유 자각 증상과 냉열감을 정밀하게 확인합니다. (가중치 1.5배 적용)")
    st.divider()
    
    # Q4, Q13, Q14, Q15
    target_q_ids = [4, 13, 14, 15]
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
            st.session_state.step = "physiology"
            st.rerun()
    with col_next:
        if st.button("🔮 최종 결과지 판정하기", type="primary", use_container_width=True):
            # Calculate final results
            scores = calculate_scores(st.session_state.answers)
            winner = max(scores, key=scores.get)
            st.session_state.constitution_result = winner
            st.session_state.step = "result"
            st.rerun()
