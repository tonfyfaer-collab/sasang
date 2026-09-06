# -*- coding: utf-8 -*-
import streamlit as st
import os
import pandas as pd
from core.questionnaire import QUESTIONS
from core.scoring import calculate_scores

# ==============================================================================
# [필독] 구글 드라이브 경혈 이미지 고유 ID 매핑 설정
# 구글 드라이브에 올린 18개 이미지 파일의 공유 링크에서 고유 ID를 가져와 아래 빈칸에 적어주세요.
# ==============================================================================
GDRIVE_FILE_IDS = {
    # 13개 기본 핵심 경혈 이미지
    "LU9.png": "1VU9zgUa_XRsTQ4YAV-JrYCmibcDH1jN1",    # 태연 (태음인 평소)
    "LU7.png": "1teSFmDtMQ8N03Oe2WbwG5h29AWkx3sQx",    # 열결 (태음인 평소)
    "LR3.png": "1WjeuZHNkp4IB7Qz0pob5TVt3GilgH9Kp",    # 태충 (태음인 치료)
    "LR2.png": "1uQ0Jkz5RwgtY_ebKSI7SEac_MBVnmMn-",    # 행간 (태음인 치료)
    "SP6.png": "1qMIcTi35Ck8km9KcehY56vCv48JloLDM",    # 삼음교 (소음인/태양인 평소)
    "CV6.png": "1xyvD-YHRHBGfq9cvJRO9DYwTJqrdRxeM",    # 기해 (소음인 평소)
    "LI4.png": "1-lk9zMhKnuOqnSGEDBHg1GPaoVnCy_mk",    # 합곡 (소음인/태양인 치료)
    "LU11.png": "11ZZu7A_YT-2iY8fNwT7hD9ghMGFOT3TQ",   # 소상 (소음인/태양인 치료)
    "SP9.png": "1g6FRjkvr4E5Z7OiZCLcwAjuEco0ic_rK",    # 음릉천 (소양인 평소)
    "PC6.png": "1rf1j8-xFurVBvw5ooqhiI5oxgo3PnzqL",    # 내관 (소양인 평소)
    "ST36.png": "15uMHdutKXVX_blowl188q56XYuHzie0m",   # 족삼리 (소양인 치료)
    "TE6.png": "1epLxmBRrBsEo1gb3nljh39xPzs7lBN19",    # 지구 (소양인 치료)
    "BL23.png": "1dUFiwR_TsTELeUZnYsGd56Hkil8UVT7a",    # 신수 (태양인 평소)
    
    # 5대 증상 확장용 추가 경혈 이미지
    "GB20.png": "1aXCkct9B0ITr7dN0mu2Egr4ieJg9ZIj2",                                  # 풍지 (태음인 두통)
    "GV20.png": "1Uw2fFJnue8Q4Ern_SmkIgP4w4YE2NheW",                                  # 백회 (소음인 두통 / 태양인 두통)
    "EXHN5.png": "1C8OBPEMATmgtM2fXwcwBKkb7DLHL3g4C",                                 # 태양 (소양인 두통)
    "ST25.png": "1J6hpGETULMqx1eD7JcBBQxsKUsU-nuaT",                                  # 천추 (태음인 변비)
    "HT7.png": "1K3d9JahX0OjA0OJoMuaefe45cREgi3yl",                                   # 신문 (태음인/소음인/소양인 두근거림)
    "BL40.png": "15Pqh2nBAPi2ZGRcfTx5Rovy7IAA5G9b2",                                  # 위중 (태음인/소음인/소양인 요통)
}

def get_gdrive_image_url(image_filename):
    "구글 드라이브 고유 파일 ID를 활용해 보안에 강한 다이렉트 이미지 URL을 생성합니다."
    file_id = GDRIVE_FILE_IDS.get(image_filename, "")
    if file_id and file_id.strip():
        return f"https://lh3.googleusercontent.com/d/{file_id.strip()}"
    return None

# Page Setup
st.set_page_config(
    page_title="사상의학 증상별 큐레이션 및 자가 홈케어 앱",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (CSS)
st.markdown(
<style>
    .main-title {
        font-size: 2.2rem;
        color: #1B5E20;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #555555;
        text-align: center;
        margin-bottom: 25px;
    }
    .result-header {
        background-color: #E8F5E9;
        padding: 20px;
        border-radius: 10px;
        border-left: 8px solid #2E7D32;
        margin-bottom: 20px;
    }
    .info-box {
        background-color: #FFF3E0;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #FF9800;
        margin-bottom: 15px;
    }
    .accent-text {
        color: #C62828;
        font-weight: bold;
    }
    .symptom-card {
        background-color: #F1F8E9;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #C5E1A5;
        margin-top: 15px;
    }
</style>
, unsafe_allow_html=True)

# Cache Symptom DB
@st.cache_data
def load_symptom_db():
    csv_filename = "sasang_symptom_db.csv"
    if os.path.exists(csv_filename):
        return pd.read_csv(csv_filename)
    elif os.path.exists(os.path.join("/workspace/artifacts", csv_filename)):
        return pd.read_csv(os.path.join("/workspace/artifacts", csv_filename))
    return None

symptom_df = load_symptom_db()

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/194/194203.png", width=80)
    st.header("🌿 사상체질 5대 증상 홈케어")
    st.write("본 서비스는 이제마 선생의 **『동의수세보원』** 원전 및 전문 한방 임상 침구학 데이터를 기반으로 작동하는 확장판 홈케어 시스템입니다.")
    st.divider()
    
    st.markdown("### ⚠️ 자가 지압 안전 주의사항")
    st.warning(\"\"\"
    1. **식후 지압 금지**: 소화기 흐름 방해 예방을 위해 식후 1시간 이내에는 강한 압박을 금합니다.
    2. **🤰 임산부 절대 기피 혈자리**: **삼음교(SP6)**와 **합곡(LI4)**은 자궁 수축 작용을 지니고 있어 임산부는 지압 및 뜸을 절대로 금지해야 합니다.
    3. **강도 조절**: 멍이 들 정도로 누르지 말고, 3~5초간 기운이 살짝 뻐근하게 득기되는 느낌(득기감) 정도로 누릅니다.
    \"\"\")
    st.divider()
    st.info("💡 **동적 DB 탑재**: 사용자가 현재 호소하는 두통, 소화불량, 변비, 두근거림, 요통의 원인 및 맞춤 치료법을 외부 한방 DB()에서 실시간으로 가져와 화면에 보여줍니다.")

# Header Titles
st.markdown('<div class="main-title">🌿 사상체질 맞춤형 5대 증상 큐레이션 시스템</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">체질 진단을 완료한 뒤, 현재 가장 불편한 증상(소화불량, 두통, 요통 등)을 선택해 원전에 입각한 체질 전용 치유법을 즉시 확인해 보세요.</div>', unsafe_allow_html=True)

# State Management
if "step" not in st.session_state:
    st.session_state.step = "intro"
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "constitution_result" not in st.session_state:
    st.session_state.constitution_result = None

# Routing Steps
if st.session_state.step == "intro":
    from views.Intro import render_intro
    render_intro()
elif st.session_state.step == "bodyshape":
    from views.BodyShape import render_body_shape
    render_body_shape()
elif st.session_state.step == "personality":
    from views.Personality import render_personality
    render_personality()
elif st.session_state.step == "physiology":
    from views.Physiology import render_physiology
    render_physiology()
elif st.session_state.step == "symptoms":
    from views.Symptoms import render_symptoms
    render_symptoms()
elif st.session_state.step == "result":
    from views.Result import render_result
    render_result(symptom_df, get_gdrive_image_url)
