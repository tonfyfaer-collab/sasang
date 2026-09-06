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
    
    # 두 개의 열 구성 (왼쪽: 정밀 진단 시작, 오른쪽: 이미 체질을 아는 사용자용 지름길)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 15문항 정밀 진단 코스")
        st.write("나의 체형, 성격, 평소 소증을 고루 분석하여 가장 정확한 사상체질을 판정해 드립니다.")
        st.write("")
        if st.button("🔮 체질 자가 진단 시작하기", type="primary", use_container_width=True):
            st.session_state.step = "bodyshape"
            st.rerun()
            
    with col2:
        st.markdown("### ⚡ 이미 본인의 체질을 아시나요?")
        st.write("따로 설문조사를 거치지 않고, 관심 있는 체질의 양생법과 5대 증상 홈케어를 즉시 확인합니다.")
        direct_const = st.selectbox(
            "구경하고 싶은 체질을 선택하세요:",
            ["태음인", "소음인", "소양인", "태양인"],
            key="direct_const_select"
        )
        if st.button("🎯 맞춤 홈케어 바로 보러 가기", use_container_width=True):
            st.session_state.constitution_result = direct_const
            st.session_state.step = "result"
            st.rerun()
