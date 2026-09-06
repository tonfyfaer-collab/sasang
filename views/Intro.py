# -*- coding: utf-8 -*-
import streamlit as st

def render_intro():
    st.subheader("🌿 사상의학 자가 건강 진단 시작")
    st.write("""
    본 자가 진단은 동무 이제마 선생의 『동의수세보원』 원전에 기록된 핵심 진단 지표들을 기반으로 구성되었습니다.
    총 **15개의 문항**을 거치며 여러분의 체형, 성격, 평소의 생리 지표, 그리고 아플 때 나타나는 특이 증상들을 종합 분석합니다.
    
    진단 결과에 따라 평소에 원기를 보하는 **양생 지압 및 맞춤 법제 약차 조제법**과,
    갑작스러운 불편함이 있을 때 이를 즉각 완화해 주는 **5대 증상별 정밀 치료 카드**를 제공합니다.
    """)
    st.divider()
    
    st.info("💡 **진단 안내**: 더 높은 정확도를 위해 본인의 평소 컨디션과 외형, 기질에 가장 가까운 답변을 진중하게 골라주세요.")
    st.write("")
    
    if st.button("🔮 체질 자가 진단 시작하기", type="primary", use_container_width=True):
        st.session_state.step = "bodyshape"
        st.rerun()
