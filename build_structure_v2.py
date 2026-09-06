# -*- coding: utf-8 -*-
import os

# 🌿 사상의학 자가진단 및 5대증상 홈케어 앱 - 모듈러 구조 자동 빌더
# 이 스크립트를 빈 폴더에 넣고 실행(python build_structure.py)하시면
# 프로페셔널한 폴더 구조(core, views 등)와 11개의 모든 파일이 완벽하게 자동 생성됩니다.

FILES = {
    r'''app.py''': r'''# -*- coding: utf-8 -*-
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
    \"\"\"구글 드라이브 고유 파일 ID를 활용해 보안에 강한 다이렉트 이미지 URL을 생성합니다.\"\"\"
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
st.markdown(\"\"\"
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
\"\"\", unsafe_allow_html=True)

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
''',
    r'''requirements.txt''': r'''# ==============================================================================
# 사상체질 및 한방 홈케어 앱 (Sasang App) - Requirements Specification
# ==============================================================================
# 
# [참고] 
# 제공해 드린 CLI 프로토타입(sasang_app_prototype.py)은 파이썬 표준 라이브러리(sys, time)만
# 사용하여 작성되었으므로, 별도의 패키지 설치 없이 'python sasang_app_prototype.py'로 즉시 실행됩니다.
#
# 아래 패키지들은 이 프로토타입을 웹 데모, 모바일 앱 백엔드 API, 또는 구글 시트 연동 등으로
# 확장하여 실제 앱 서비스를 개발할 때 필요한 대표적인 핵심 라이브러리들입니다.

# 1. 웹 프로토타입 및 대시보드 제작용 (추천)
streamlit>=1.30.0     # 파이썬 코드를 몇 줄만으로 아름다운 웹 앱 UI로 전환해 주는 라이브러리

# 2. 모바일 앱(Flutter/React Native) 연동을 위한 백엔드 API 개발용
fastapi>=0.100.0      # 빠르고 현대적인 고성능 Web API 프레임워크
uvicorn>=0.22.0       # FastAPI 앱을 구동하기 위한 경량 ASGI 서버

# 3. 데이터 분석 및 구글 시트/엑셀 연동용
pandas>=2.0.0         # 체질/경혈/약재 데이터베이스 가공 및 변환용
openpyxl>=3.1.0       # 엑셀 파일(.xlsx)을 직접 읽고 쓰기 위한 라이브러리
gspread>=5.10.0       # 구글 시트 API를 파이썬과 간편하게 연동해 주는 라이브러리

# 4. 이미지 처리 (경혈 지도 이미지 등)
Pillow>=10.0.0        # 서버 측에서 경혈 이미지를 가공하거나 조절할 때 필요
''',
    r'''sasang_symptom_db.csv''': r'''﻿symptom,constitution,cause,acupoint1_name,acupoint1_code,acupoint1_position,acupoint1_method,acupoint1_image,acupoint2_name,acupoint2_code,acupoint2_position,acupoint2_method,acupoint2_image,herb_name,herb_efficacy,herb_processing,tea_recipe
소화불량,태음인,"간대폐소(肝大肺小)의 체질로, 간에 열이 차거나 몸의 기혈 소통이 정체되면서 위장 운동이 둔화되어 발생합니다. 가슴 답답함이나 팽만감을 동반하는 경우가 많습니다.",태충 (太衝),LR3,첫째와 둘째 발가락뼈가 만나는 곳에서 약간 위쪽의 오목하고 맥박이 느껴지는 부위,과열되기 쉬운 간의 열을 내리고 혈압을 안정시킵니다. 다소 강한 압박감(뻐근함)이 느껴질 정도로 5초간 꾹 눌러줍니다.,LR3.png,행간 (行間),LR2,첫째와 둘째 발가락 사이의 갈라진 경계선 부위,간 수열(간의 열 독소)을 맑게 식히고 두통과 충혈을 완화해 줍니다. 손끝이나 지압봉으로 강하게 지압합니다.,LR2.png,"의이인 (薏苡仁, 율무)",비위의 습한 노폐물을 배출하고 위장 소화 기능을 고르게 돕습니다.,"껍질을 벗긴 율무를 흐르는 물에 깨끗이 씻어 말린 뒤, 팬에 약한 불로 노릇노릇해질 때까지 볶아서(초법) 사용하면 차가운 성질이 완화됩니다.",볶은 율무 20g에 물 1L를 붓고 끓여 물 대신 차처럼 은근히 나누어 마십니다.
소화불량,소음인,"신대비소(腎大脾小)의 체질로, 본래 위장 기운이 가장 약해 속이 차가워질 때 위장 평활근이 수축하고 운동을 멈추며 급체나 만성 소화불량이 쉽게 생깁니다.",합곡 (合谷),LI4,엄지와 검지 손가락 뼈가 만나는 부위의 바로 앞 오목한 곳,급체하거나 머리가 아플 때 막힌 기를 강력하게 뚫어줍니다. 찌릿한 느낌이 손끝까지 가도록 강하게 5초씩 지압합니다.,LI4.png,삼음교 (三陰交),SP6,안쪽 복사뼈 중심에서 위로 3치(본인의 손가락 네 마디 너비) 올라간 정강이뼈 뒤쪽 가장자리,전신의 혈액 순환을 돕고 비위 기능을 따뜻하게 보강합니다. 부드럽게 원을 그리며 따뜻한 온기가 돌 때까지 마사지합니다.,SP6.png,인삼 (人參),소음인의 비위 기운을 직접적으로 크게 보강하고 뱃속을 따뜻하게 하여 소화력을 극대화합니다.,수삼의 뇌두(머리 부분)를 완전히 제거하고 얇게 썰어 말린 후 사용합니다. 약성을 순하게 하기 위해 꿀에 재웠다가 사용해도 좋습니다.,손질한 인삼 6g과 대추 2알에 물 800ml를 넣고 끓여 따뜻하게 수시로 복용합니다.
소화불량,소양인,"비대신소(脾大腎小)의 체질로, 위장에 과도한 열(火)이 쌓여 소화기가 건조해지고 팽창하며 막히는 현상이 생깁니다. 체하면 속이 불전처럼 답답하고 뜨거워지는 특징이 있습니다.",족삼리 (足三里),ST36,"독비혈(무릎 바깥쪽 오목한 곳)에서 아래로 3치 내려간 곳, 정강이뼈 가쪽 한 손가락 너비",위장의 과도한 열을 내리고 소화기 기운을 아래로 끌어내려 편안하게 뚫어줍니다. 묵직하고 뻐근한 자극을 줍니다.,ST36.png,내관 (內關),PC6,손목 안쪽 주름의 정중앙에서 팔 쪽으로 약 2치(손가락 세 마디 너비) 올라간 두 힘줄 사이,스트레스로 인해 가슴과 위장에 기가 뭉친 것을 풀어주며 위장 운동을 조율합니다. 가볍게 원을 그리며 3분간 지압합니다.,PC6.png,산수유 (山茱萸),위열로 소모된 신장과 비위의 음액을 보충하여 소화기의 부드러운 움직임을 돕습니다.,산수유 열매에서 씨앗을 반드시 제거(去核)해야 합니다. 씨앗은 정력을 상하게 하므로 과육만 부드럽게 발라내어 건조해 씁니다.,씨를 뺀 산수유 10g을 물 1L에 달여 식후에 마시면 위장의 건조함을 예방해 줍니다.
소화불량,태양인,"폐대간소(肺大肝小)의 체질로, 기운이 비정상적으로 자꾸 위로만 치솟아 음식을 삼키지 못하고 거꾸로 토해내는 열격/반위증(噎膈反胃症) 소화 장애가 나타납니다.",합곡 (合谷),LI4,엄지와 검지 사이의 호구 부위 오목한 곳,치솟아 오르는 기운을 사방에서 붙잡아 아래로 가라앉히고 막힌 통로를 소통시킵니다. 찌릿하도록 강하게 압박합니다.,LI4.png,소상 (少商),LU11,엄지손가락 손톱 안쪽 모서리 가쪽으로 1mm 지점,식도가 조이거나 솟구치는 급성 체기 시 손톱 끝이나 소독된 침으로 강하게 지압/사혈하여 압력을 급격히 떨어뜨립니다.,LU11.png,모과 (木瓜),거꾸로 치솟는 기운을 아래로 순하게 내리며 식도와 위장 근육의 뒤틀린 경련을 완화해 줍니다.,"가을철 잘 익은 모과를 4등분해 안쪽 씨를 완전히 제거한 뒤, 얇게 썰어 은근한 김에 한번 찐 뒤 햇볕에 완전히 건조하여 사용합니다.",말린 모과 10g을 끓여 식힌 후 수시로 한 모금씩 천천히 넘기며 음용합니다.
두통,태음인,간열(肝熱)이 가득 차 오르고 체내 탁한 습이 머리로 향해 생깁니다. 머리가 마치 무거운 돌을 얹은 듯 무겁고 둔탁한 아픔이 특징이며 눈 피로를 동반합니다.,태충 (太衝),LR3,첫째와 둘째 발가락뼈가 만나는 곳에서 약간 위쪽의 오목하고 맥박이 느껴지는 부위,간열을 내려 머리와 눈에 쏠린 풍열(風熱) 기운을 시원하게 소통시킵니다. 뻐근함이 발끝까지 가도록 지긋이 지압합니다.,LR3.png,풍지 (風池),GB20,"목덜미 뒤쪽, 귀 뒤의 튀어나온 뼈 아래 오목하게 들어간 곳",머리로 통하는 모든 혈관과 신경이 모이는 목 뒷덜미 부위입니다. 양손으로 머리를 감싸쥐고 엄지손가락으로 머리 방향으로 밀어 올리듯 강하게 압박합니다.,GB20.png,"갈근 (葛根, 칡뿌리)",목덜미 뒷근육이 굳고 뭉쳐 유발되는 혈류 정체형 두통을 시원하게 풀고 간열을 맑게 내려줍니다.,가을에 캔 칡뿌리의 흙을 씻고 껍질을 벗겨 적당하게 편 썬 후 햇볕에 완전히 건조하여 약용합니다.,갈근 15g에 물 1L를 부어 달인 후 미지근하게 마셔 뭉친 근육을 풀어줍니다.
두통,소음인,몸이 극도로 차가워지고 양기가 부족하여 머리 부위까지 혈류와 따뜻한 온기가 닿지 못해 발생합니다. 머리가 띵하고 차가우며 어지럼증을 동반합니다.,백회 (百會),GV20,양쪽 귀 끝을 연결한 선과 머리 정중앙을 가로지르는 선이 만나는 정수리 부위,머리끝의 모든 양기를 끌어올리고 전신의 차가운 기운을 소통시킵니다. 손가락 끝으로 머리 수직 방향으로 지긋이 자극합니다.,GV20.png,합곡 (合谷),LI4,엄지와 검지 손가락 뼈가 만나는 부위의 바로 앞 오목한 곳,사지 말단으로 기혈을 막힘없이 내보내어 머리 뒤쪽과 이마 부위의 정체된 냉성 통증을 가라앉힙니다. 약간 자극이 가도록 강하게 누릅니다.,LI4.png,천궁 (川芎),"혈액 순환을 활발하게 돕는 활혈(活血) 효능의 대표 요약으로, 소음인의 차가운 냉두통을 없애는 데 특효입니다.",천궁의 특유 자극적인 정유 성분을 제거하기 위해 '쌀뜨물에 하루 동안 담가두어(미감침)' 기름기를 뺀 뒤 건조하여 약용합니다. 머리가 아프지 않고 순해집니다.,미감침 처리한 천궁 5g과 물 600ml를 넣고 달여 따뜻하게 차로 복용합니다.
두통,소양인,체질적으로 신장 음액이 부족하고 위열(胃熱)이나 쓸개 열이 가득 차올라 머리 관자놀이 부위가 지끈지끈 쪼개지듯 아픈 측두통이 잘 발생합니다.,태양 (太陽),EX-HN5,눈썹 바깥쪽 끝과 눈꼬리 바깥쪽 끝의 중간에서 뒤쪽으로 1치(손가락 한 마디 너비) 오목한 부위 (흔히 관자놀이라 부르는 곳),치솟는 머리 부위의 열독과 두통을 직접 가라앉힙니다. 양 손가락 끝으로 가벼운 원을 그리며 뻐근하게 2분 동안 지압합니다.,EXHN5.png,지구 (支溝),TE6,손등 손목 주름에서 위로 3치 올라간 두 뼈 사이의 오목한 곳,소양인의 몸 안 삼초(전신 순환계)의 열을 내리고 막힌 기를 아래로 뿜어내려 두통을 신속하게 완화합니다. 뻐근하게 누릅니다.,TE6.png,구기자 (枸杞子),머리로 솟구치는 상열감을 잡기 위해 신장의 마른 음액을 깊숙하게 채워주어 열을 끄고 눈을 맑게 합니다.,열매를 수확해 깨끗이 씻은 후 막걸리를 가볍게 뿌려 시루에 찐 다음(주증) 다시 건조하면 소양인 신장 기운을 보강하는 성질이 대폭 강화됩니다.,주증한 구기자 10g에 물 1L를 붓고 끓여 차갑게 보관하여 물처럼 수시로 마십니다.
두통,태양인,폐의 극도로 웅장한 상승 기운이 한 방향으로만 발달해 정수리와 머리 꼭대기 부위에 기운과 압력이 과도하게 몰리면서 터질 듯한 두통이 발생합니다.,소상 (少商),LU11,엄지손가락 손톱 안쪽 모서리 가쪽으로 1mm 지점,폐에 쏠린 과도한 기 기운의 압력을 급격하게 방출해 줍니다. 손가락 끝으로 아주 아플 정도로 강하게 꼭꼭 지압합니다.,LU11.png,백회 (百會),GV20,정수리 가마 맨 윗부분의 오목한 중심 부위,막히고 갇혀 뭉친 비생리적 열을 체외로 순환/발산시켜 줍니다. 손끝으로 지긋이 수직 압박을 반복해 줍니다.,GV20.png,오가피 (五加皮),체내 기의 승강출입 조화를 맞추고 뇌압 상승 두통을 부드럽게 가라앉히는 데 탁월합니다.,"오가피 가지/뿌리껍질을 채취해 깨끗이 씻고 잘게 썬 후, 소금물에 가볍게 담갔다가 꺼내어 볶는 '염수초'를 통해 하초 보강 약성을 강화합니다.",염수초한 오가피 10g에 물 800ml를 넣고 은근하게 우려내어 복용합니다.
변비,태음인,"대장 건조(장조, 腸燥)가 심해져 대장 내 수분이 빠르게 고갈되어 생깁니다. 땀을 시원하게 흘리지 못해 몸안에 독소와 열이 정체될 때 변비가 극대화됩니다.",천추 (天樞),ST25,배꼽 중심에서 가쪽(좌우 양옆)으로 각각 본인 손가락 두 마디 너비(2치) 만큼 떨어진 오목한 부위,대장의 직접적인 연동 운동과 수분 흡수 기능을 조율해 줍니다. 편안하게 누운 상태에서 양손 무릎을 세우고 손끝으로 지긋이 누르며 원을 그리듯 문질러 줍니다.,ST25.png,태충 (太衝),LR3,첫째와 둘째 발가락뼈가 만나는 곳에서 약간 위쪽의 오목한 부위,간열이 대장을 압박해 장의 진액을 건조시키는 것을 막아 장을 윤활하게 합니다. 다소 뻐근하게 지압합니다.,LR3.png,맥문동 (麥門冬),폐와 대장의 메마른 진액(수분)을 풍부하게 생성해 주어 단단해진 대변을 부드럽게 씻어내려 보냅니다.,"맥문동 열매의 약성이 없는 '가운데 심지(거심, 去心)'를 완전히 뽑아낸 후 햇볕에 완전히 건조해야 가슴 답답함이나 부작용을 막을 수 있습니다.",거심한 맥문동 10g에 물 1L를 붓고 오랜 시간 끓여 물처럼 음용합니다.
변비,소음인,하초(아랫배)의 따뜻한 양기가 극도로 떨어져 장이 꽁꽁 얼어붙듯 연동 운동을 멈춰 발생합니다. 대변이 딱딱하지 않은데도 몇 일 동안 밀어내지 못하는 냉성 변비가 흔합니다.,기해 (氣海),CV6,배꼽 아래로 약 1.5치(본인 검지와 중지 너비) 내려간 앞정중선 부위,단전의 멈춘 양기와 원기를 채워 차가운 장을 사르르 녹여 연동 운동을 시작하게 돕습니다. 따뜻한 뜸이나 손바닥 지압이 훌륭합니다.,CV6.png,삼음교 (三陰交),SP6,안쪽 복사뼈 중심에서 위로 3치 올라간 정강이뼈 뒤쪽 가장자리,하복부 장관막의 혈액과 림프 소통을 직접 활성화합니다. 손끝으로 깊숙하게 3초간 누르기를 15회 반복합니다.,SP6.png,백출 (白朮),소음인 장내 비정상적인 수분 축적(냉습)을 정돈해 주어 약해진 장 평활근의 수축력을 든든하게 복원합니다.,삽주 뿌리를 쌀뜨물에 하루 동안 담가(미감침) 정유 기름기를 빼주고 오븐이나 마른 가마솥에 은근하게 구워 완전히 말린 후 사용합니다.,손질된 백출 8g과 생강 1편에 물 600ml를 붓고 끓여 따뜻한 상태로 나누어 복용합니다.
변비,소양인,위장과 대장의 열독(火)이 한데 엉켜 대변의 수분을 전부 증발시켰을 때 발생하는 전형적인 조열성 극심한 변비입니다. 변이 단단해 똥글똥글 굴러가는 형태로 나타납니다.,지구 (支溝),TE6,손등 손목 주름에서 위로 3치 올라간 두 뼈 사이의 오목한 곳,대장의 수분 조절과 삼초의 열을 내려 대변 통로를 시원하게 열어주는 변비 치료 최고의 요혈입니다. 다소 강한 압력으로 지압봉 지압을 합니다.,TE6.png,음릉천 (陰陵泉),SP9,종아리 안쪽 정강이뼈 아래 무릎 관절 바로 아래 오목하게 만나는 부위,"과열된 장의 비정상적 열을 해수/해독하여 진액이 대장으로 고르게 돌 수 있도록 도우며, 손가락으로 꾹꾹 자극합니다.",SP9.png,숙지황 (熟地黃),소양인 변비 치료에 있어 장에 윤활유를 바르듯 수분과 신장의 정혈을 대폭 쏟아부어 대변이 스스로 미끄러져 나오게 돕습니다.,생지황을 막걸리에 적셔 시루에 9번 찌고 말리는 정성(구증구포)을 거쳐 검고 끈적한 숙지황으로 법제하여 독성을 전면 제어하고 효능을 극대화해 씁니다.,숙지황 6g을 뜨거운 물 500ml에 은근히 우려내어 깊고 진한 차로 음용합니다.
변비,태양인,하체 힘이 약하고 척추 골격의 압박으로 인해 하초의 대장 연동 기능을 담당하는 자율신경 기운이 원활하게 밑으로 도달하지 못해 발생하는 무력성 변비입니다.,삼음교 (三陰交),SP6,안쪽 복사뼈 중심에서 위로 3치 올라간 뼈 뒷가장자리 오목한 부위,태양인의 가장 약한 하반신과 신장/간 기운을 함께 자극하여 하초 대장 소통 운동을 유도합니다. 지긋이 깊게 5초간 자극합니다.,SP6.png,신수 (腎兪),BL23,허리 둘째 허리뼈 가시돌기 아래에서 가쪽으로 1.5치 부위,신장의 원기를 자극해 하반신으로 통하는 척추 신경과 골반저근 혈류를 살려 쾌변을 유도합니다. 허리를 문지르거나 꾹 누릅니다.,BL23.png,모과 (木瓜),하체 근육과 장 평활근의 긴장을 부드럽게 이완시켜 장내 정체된 노폐물의 활발한 하행 소통을 촉진합니다.,모과를 4등분하여 한가운데 씨를 긁어 버리고 얇게 저민 뒤 가벼운 증기에 살짝 찐 다음 햇볕에 건조하여 약제로 가공합니다.,말린 모과 10g과 약간의 율무를 물 1L와 우려내어 시원하게 복용합니다.
두근거림,태음인,태음인의 대표적인 기혈 순환 정체증이자 전조 증상인 정충증(怔忡症)입니다. 가슴이 이유 없이 쿵쾅거리고 울렁거리며 기가 막혀 답답해지는 증상입니다.,태연 (太淵),LU9,"손목 안쪽 가로주름의 노쪽(엄지손가락 쪽), 요골동맥이 뛰는 오목한 부위",태음인의 약한 폐 기운을 자극해 전신의 기 소통을 강력하게 이끌고 불안해진 심장을 감싸 안아 안정을 찾게 합니다. 부드럽게 지압합니다.,LU9.png,신문 (神門),HT7,손목 안쪽 주름의 안쪽(새끼손가락 쪽) 끝부분 틈새의 오목한 부위,심장 신경과 직접 교류하는 요혈로 흥분되거나 불안정한 기와 혈을 뚝 가라앉힙니다. 손톱 끝으로 지긋이 꾹 눌러줍니다.,HT7.png,"산조인 (酸棗仁, 대추나무씨)","천연 신경안정제로 불리며, 태음인의 가슴 떨림과 불안증, 수면 장애를 조절하는 최고의 영약입니다.",맷돌이나 팬에 산조인 씨앗을 노릇노릇하고 바삭해질 때까지 '볶아서(초법)' 사용해야 약성이 우러나며 불면과 두근거림 완화 효과가 나타납니다. 생으로 쓰면 반대로 작용할 수 있습니다.,볶은 산조인 10g을 살짝 짓이겨 물 800ml에 넣고 달여 잠들기 1시간 전에 따뜻하게 차로 마십니다.
두근거림,소음인,"전반적인 혈액(血)과 심장 양기가 허약하여, 아주 조그만 소리나 사소한 외부 스트레스에도 가슴이 깜짝깜짝 놀라며 심하게 뛰는 증상(경계증)이 나타납니다.",내관 (內關),PC6,손목 안쪽 주름의 정중앙에서 팔 쪽으로 약 2치 올라간 두 힘줄 사이,심포(심장 보호막)의 혈류를 늘려 약해진 심장을 튼튼하게 감싸 안고 구토감이나 가슴 떨림을 부드럽게 잠재웁니다.,PC6.png,기해 (氣海),CV6,배꼽 아래 1.5치 내려간 부위,단전의 약해진 양기를 원천 보강하여 심장의 과열된 가짜 열을 하초로 부드럽게 가라앉혀 평정을 유도합니다.,CV6.png,당귀 (當歸),소음인의 부족한 피(정혈)를 가득 보충하여 심장 근육과 뇌 혈류로 가는 산소 공급을 풍부하게 돕습니다.,"당귀의 매운맛과 특이 자극 성분을 완화하고 약성을 고르게 하기 위해 '막걸리(청주)를 골고루 뿌려 촉촉하게 재운 뒤 가마솥에 살짝 볶는(주초, 酒炒)' 법제를 진행합니다.",주초 가공한 당귀 8g과 말린 대추 2알에 물 700ml를 넣고 끓여 하루에 서너 번 차로 마십니다.
두근거림,소양인,몸 안의 조절되지 않는 번조증(煩躁症 - 가슴에 뜨거운 화가 꽉 차서 손발을 가만히 두지 못하고 심장이 사납게 뛰는 병증)으로 인해 유발됩니다.,내관 (內關),PC6,"손목 안쪽 두 힘줄 사이, 손목 주름 위로 약 2치 부위",심포의 과열된 심열(心熱)을 가라앉혀 맥박의 폭주를 진정시키고 흥분된 자율신경을 다스립니다. 가볍게 호흡하며 3분간 누릅니다.,PC6.png,신수 (腎兪),BL23,"허리 부위, 둘째 허리뼈 아래에서 가쪽으로 1.5치 부위",소양인의 극도로 말라붙은 신장의 차가운 수(水) 기운을 북돋워 위쪽 심장의 불(火)을 자연스럽게 끄는 '수승화강'의 핵심 요혈입니다.,BL23.png,"지황 (地黃, 생지황)",피 속의 뜨거운 심열과 염증을 즉각 식혀주고 심장 주변의 모세혈관 열 압력을 떨어뜨려 마음을 평온하게 해 줍니다.,"생지황을 깨끗이 씻어 얇게 썰어 햇볕에 완벽히 말리거나(건지황), 꿀과 술을 사용해 가볍게 법제하여 소양인의 심장의 불을 다스리는 데 사용합니다.",말린 건지황 6g을 뜨거운 물 500ml에 은근하게 차처럼 오랫동안 우려 한 김 식혀서 시원하게 음용합니다.
두근거림,태양인,"극도의 정신적 분노나 과로로 인해 상승 기운이 최고조에 달했을 때, 심장이 쿵쾅거리며 압력이 머리 끝까지 쏠려 가슴이 찢어지듯 팽창하는 병증입니다.",소상 (少商),LU11,엄지손가락 손톱 안쪽 모서리 가쪽으로 1mm 지점,과열된 폐 기운의 출구를 강하게 흔들며 열어주어 가슴의 답답함과 맥박 안정을 즉각 도모합니다. 손끝 지압기로 세게 자극합니다.,LU11.png,신문 (神門),HT7,손목 안쪽 주름의 안쪽(새끼손가락 쪽) 끝부분 오목한 부위,심장으로 가는 맥맥을 진정시키고 기맥의 솟구침을 차분하게 붙잡아 가슴속 답답함을 순하게 가라앉힙니다.,HT7.png,오가피 (五加皮),"치솟은 흥분성 자율신경 기운을 온화하게 잡아주고, 전신의 흐름을 전반적으로 가라앉히는 데 특효입니다.",잘 자란 가시오갈피의 뿌리 껍질을 씻고 얇게 편 썬 후 약한 소금물에 한 시간 동안 재웠다가 마른 팬에 가볍게 볶아(염수초) 성질을 부드럽게 바꿉니다.,가공한 오가피 12g을 물 1L와 함께 진하게 끓여 물처럼 음용합니다.
요통,태음인,몸에 과도한 습기(습담)와 노폐물이 허리 뒷근육과 척추 뼈 관절 마디사이에 눌러앉아 혈류를 방해해 발생합니다. 날씨가 흐리거나 비가 올 때 허리가 찌뿌둥하고 묵직한 요통이 전형적입니다.,위중 (委中),BL40,무릎 뒤쪽 오금 가로주름의 정중앙 부위,허리 부위의 꽉 뭉친 혈류와 기운 정체를 발아래로 시원하게 터트려주는 '요통 최고의 구급 명혈'입니다. 무릎을 가볍게 세운 뒤 손가락 힘으로 오금을 꾹 자극해 마사지합니다.,BL40.png,태충 (太衝),LR3,첫째와 둘째 발가락뼈 사이 위쪽 오목한 곳,간과 신장의 뭉친 기혈 소통을 도우며 척추를 둘러싸고 있는 후두근육과 허리 근막의 유연한 이완을 유도합니다.,LR3.png,두충 (杜仲),척추 뼈와 허리 인대를 강건하게 하여 노화성 허리 통증이나 요통을 진정시키는 한방 최고의 보골제(補骨劑)입니다.,"두충 껍질 안쪽의 가느다란 하얀 고무 실 같은 성분(실, 絲)을 완전히 끊어야 약효가 우러납니다. 따라서 '약한 소금물에 버무려 껍질의 하얀 실이 끊어질 때까지 가마솥에 까맣게 그을려 볶아내는(염소초, 鹽炙炒)' 정교한 법제 요령이 반드시 요구됩니다.",염소초하여 실을 완전히 제거한 두충 10g에 물 800ml를 넣고 끓여 하루에 세 잔 차로 나누어 마십니다.
요통,소음인,신장의 양기가 극도로 차가워져 허리 뼈 주변의 모세혈관이 수축되고 척추립근이 뻣뻣하게 얼어붙어 붓는 냉성 요통이 주로 나타납니다. 허리를 핫팩 등으로 따뜻하게 해 주면 아픔이 가시는 특징이 있습니다.,기해 (氣海),CV6,배꼽 아래 1.5치 내려간 부위,허리 전면 단전에 양기를 불어넣어 차갑게 얼어붙은 척추립근 뒤쪽까지 온기가 순환하게 만듭니다. 손바닥을 부벼 따뜻하게 올려 누릅니다.,CV6.png,삼음교 (三陰交),SP6,안쪽 복사뼈 중심에서 위로 3치 올라간 뼈 뒷가장자리 안쪽,골반 내부 순환과 허리 골반기저근의 통증 유발 물질을 부드럽게 청소해 주는 자극을 손끝으로 가해 줍니다.,SP6.png,파극천 (巴戟天),아랫배와 신장 주변에 강력한 아궁이 불을 지피듯 양기를 가득 채워 냉성 척추 요통을 깨끗이 날려버립니다.,파극천 뿌리 안쪽의 단단한 '심지(목질부)를 반드시 제거(去心)'해야 합니다. 그렇지 않으면 심장의 과열을 유발할 수 있습니다. 감초 끓인 물에 푹 달인 후 칼로 눌러 심지를 뺀 뒤 완전히 말려 씁니다.,손질된 파극천 6g에 물 600ml를 붓고 끓여 우려내어 하루에 두 번 차로 복용합니다.
요통,소양인,비대신소의 체질로 장부 중 신장(腎) 기운이 가장 빈약하여 허리 등뼈와 골반 주변을 지탱하는 진액과 근골의 보강 기운이 쉽게 마르고 약화되어 요통과 무릎 통증이 상시적으로 찾아옵니다.,신수 (腎兪),BL23,허리 뒤쪽 둘째 허리등뼈 아래 양옆으로 손가락 두 마디 너비(1.5치) 부위,약해진 소양인의 신장 원기를 골반 부위 뒤에서 직접 수혈해 주듯 채우는 요통 최고의 요혈입니다. 엄지손가락으로 척추 방향을 향해 지긋이 꾹 자극해 마사지합니다.,BL23.png,족삼리 (足三里),ST36,"독비혈 아래로 3치 내려간 곳, 정강이뼈 가쪽 부위",상체 열을 무릎 아래로 내려 허리 척추 압박 부위로 가는 기의 울체를 전신 골격계로 분산시킵니다. 묵직하게 누릅니다.,ST36.png,산수유 (山茱萸),허리를 지탱하는 든든한 뼈대 기운인 '신수'를 풍부하게 충전해 주어 만성 요통을 뿌리 뽑는 명약입니다.,반드시 씨앗을 까서 빼내고 가공해야 부작용이 없습니다. 과육만 발라 건조한 후 사용하면 소양인의 하체 약화와 허리 시림 요통에 훌륭하게 작용합니다.,씨를 제거한 산수유 12g을 물 1L와 우려내어 매일 보리차 대용으로 복용합니다.
요통,태양인,폐대간소로 인해 하체가 극도로 빈약하고 목덜미에만 기세가 쏠려 척추 뒤쪽을 든든히 받쳐줄 척추 기립근과 골반 인대가 영양을 공급받지 못해 주저앉듯 발생합니다.,신수 (腎兪),BL23,허리 뒤쪽 둘째 허리뼈 가쪽 1.5치 부위,태양인의 빈약한 신장과 하체 척추뼈 관절을 직접적으로 강화시키는 명혈입니다. 양손을 비벼 허리를 매일 부드럽게 비벼줍니다.,BL23.png,삼음교 (三陰交),SP6,안쪽 복사뼈 중심에서 위로 3치 올라간 정강이뼈 뒷가장자리 안쪽,하체 음혈을 풍부하게 생성하여 척추와 허리 엉덩이 근육마름 증상(태양인 전형증)을 방지하도록 돕습니다.,SP6.png,오가피 (五加皮),근육과 인대를 질기고 견고하게 강화시켜 하체 무력증 및 척추 관절 쇠약형 요통을 다스립니다.,"가시오갈피의 껍질을 씻어 편 썬 뒤, 볶는 염수초 가공을 통해 신장을 자극하는 따뜻하고 이완 뼈 보강 성질을 끌어올려 약용합니다.",염수초한 오가피 12g에 물 1L를 붓고 오랜 시간 끓여 물 대신 자주 나누어 마십니다.
''',
    r'''views/Result.py''': r'''# -*- coding: utf-8 -*-
import streamlit as st

CONSTITUTION_DATA = {
    "태음인": {
        "name_hanja": "太陰人",
        "description": "간의 기능은 성하고 폐의 기능은 약한 '간대폐소(肝大肺小)'의 장부 구조를 타고났습니다. 체구가 듬직하고 골격이 발달했으며, 성격이 묵묵하고 끈기 있게 목표를 완수하는 우직함이 장점입니다.",
        "daily_condition": "땀(汗)이 전신에 잘 나고 소통이 원활할 때 몸이 가장 개운하고 완벽하게 건강한 상태(완실무병)입니다.",
        "warning_signs": "피부가 야무지고 단단해지며 땀이 한 방울도 나지 않거나, 가슴이 심하게 쿵쾅거리며 불안해지는 정충증(怔忡症)이 생기면 순환이 막히고 있다는 위험 신호입니다.",
        "acupoints_daily": [
            {"name": "태연 (太淵, LU9)", "position": "손목 안쪽 주름의 요골 쪽(엄지손가락 쪽) 맥박이 뛰는 부위", "method": "약해지기 쉬운 폐의 기운을 보강하기 위해, 손가락 끝으로 3초간 지긋이 누르기를 10회 반복합니다. 뜸을 가볍게 뜨는 것도 좋습니다.", "image": "LU9.png"},
            {"name": "열결 (列缺, LU7)", "position": "양손의 엄지와 검지 사이를 엇갈려 잡았을 때, 집게손가락 끝이 닿는 손목 안쪽의 오목한 틈새", "method": "폐의 소통을 돕고 호흡기를 보호하는 자리입니다. 가볍게 원을 그리며 마사지하듯 눌러줍니다.", "image": "LU7.png"}
        ],
        "herbs": [
            {"name": "의이인 (薏苡仁, 율무)", "efficacy": "비위(위장)와 폐의 습한 기운을 없애주고 노폐물 배출을 도와 자양강장 및 체중 조절에 좋습니다.", "processing": "껍질을 벗긴 율무를 흐르는 물에 깨끗이 씻어 말린 뒤, 팬에 '약한 불로 노릇노릇해질 때까지 볶아서(초법, 炒法)' 사용하면 성질이 부드러워집니다."},
            {"name": "갈근 (葛根, 칡뿌리)", "efficacy": "간에 쌓인 열과 독소를 풀어주고 땀구멍을 열어주어 초기 감기 발열 및 굳어 있는 목덜미 근육을 풀어줍니다.", "processing": "가을에 캔 칡뿌리를 깨끗이 씻어 겉껍질을 벗긴 후, 얇게 썰어 햇볕에 완벽하게 건조하여 사용합니다."}
        ],
        "tea_recipe": "볶은 율무 20g과 건조한 갈근 10g에 물 1L를 붓고 약한 불에 끓여 하루 2-3회 차처럼 나누어 드세요."
    },
    "소음인": {
        "name_hanja": "少陰人",
        "description": "신장의 기능은 성하고 비장의 기능은 약한 '신대비소(腎大脾小)'의 장부 구조를 지녔습니다. 성격이 차분하고 치밀하며 다정한 한편, 소화 기능이 예민하고 몸이 차가워지기 쉬워 따뜻한 보호가 필요합니다.",
        "daily_condition": "먹은 음식이 체하지 않고 소화(消化)가 부드럽게 잘 될 때 비로소 속이 가장 개운하고 완벽하게 건강한 상태(완실무병)입니다.",
        "warning_signs": "평소 한숨을 깊게 자주 쉬거나, 손발이 얼음처럼 차가워지며(수족냉증) 설사를 하고 억지로 땀을 흘릴 때 기운이 쏙 빠지면 면역이 급격히 저하되고 있다는 위험 신호입니다.",
        "acupoints_daily": [
            {"name": "삼음교 (三陰交, SP6)", "position": "안쪽 복사뼈 중심에서 위로 3치(본인 손가락 네 마디 너비) 올라간 정강이뼈 뒤쪽 가장자리", "method": "하복부를 따뜻하게 하고 소화기 기운을 북돋우는 핵심 양생혈입니다. 부드러운 온열 뜸을 뜨거나 가볍게 마사지합니다.", "image": "SP6.png"},
            {"name": "기해 (氣海, CV6)", "position": "배꼽 아래로 약 1.5치(본인의 검지와 중지 너비) 내려간 부위", "method": "원기의 바다라 불리는 곳으로 하초를 따뜻하게 덥혀줍니다. 평소 온뜸이나 따뜻한 온팩을 적용하면 소화력이 몰라보게 좋아집니다.", "image": "CV6.png"}
        ],
        "herbs": [
            {"name": "인삼 (人參)", "efficacy": "비위의 약한 기운을 북돋우고 양기를 채워주어 손발을 따뜻하게 하고 소화력을 대폭 끌어올립니다.", "processing": "수삼의 뇌두(머리 부분)를 완전히 잘라내고(구토를 유발하므로 필수), 얇게 썰어 말리거나 꿀에 재워 사용하여 약성을 부드럽게 조율합니다."},
            {"name": "백출 (白朮, 삽주뿌리)", "efficacy": "위장을 튼튼하게 하고 뱃속의 차가운 물기를 없애주어 소화불량과 설사를 즉각 멈추게 합니다.", "processing": "삽주 뿌리를 깨끗이 씻고 '쌀뜨물에 하루 동안 담가두어(미감침)' 기름기를 뺀 다음, 약한 불에 구워 건조하여 사용합니다."}
        ],
        "tea_recipe": "인삼 6g과 미감침 가공한 백출 6g에 대추 2알을 넣고 물 800ml에 은근히 우려내어 따뜻하게 복용합니다."
    },
    "소양인": {
        "name_hanja": "少陽人",
        "description": "비장의 기능은 성하고 신장의 기능은 약한 '비대신소(脾대腎小)'의 장부 구조를 지녔습니다. 행동이 민첩하고 굳세며 사안을 시원시원하게 해결하는 돌파력이 뛰어나지만, 위장에 열이 차올라 성격이 급해지기 쉽습니다.",
        "daily_condition": "대변(大便)이 막히지 않고 하루 한 번 막힘없이 시원하게 잘 통하는 것이 최고의 건강 척도(완실무병)입니다.",
        "warning_signs": "대변이 3일 이상 통하지 않으면 가슴속이 불같이 답답하고 뜨거워지며, 머리가 지끈거리거나 극도로 예민해져 화가 자주 치미는 것이 건강 적신호입니다.",
        "acupoints_daily": [
            {"name": "음릉천 (陰陵泉, SP9)", "position": "종아리 안쪽 정강이뼈를 따라 위로 올라가다 무릎 관절 바로 아래 오목하게 걸리는 부위", "method": "몸 안의 비생리적인 열 독소와 쓸데없는 수분을 빼주어 하체를 가볍게 돕습니다. 엄지손가락으로 꾹꾹 지압해 줍니다.", "image": "SP9.png"},
            {"name": "내관 (內關, PC6)", "position": "손목 안쪽 주름의 정중앙에서 팔 쪽으로 약 2치(손가락 세 마디 너비) 올라간 두 힘줄 사이", "method": "가슴으로 치솟는 화와 열 기운을 아래로 내리고 울화를 가라앉혀 줍니다. 편안하게 호흡하며 3분씩 부드럽게 지압합니다.", "image": "PC6.png"}
        ],
        "herbs": [
            {"name": "구기자 (枸杞子)", "efficacy": "약해지기 쉬운 신장의 음액을 풍부하게 보하고 눈을 맑게 하여 상체 열을 내리고 노화를 방지합니다.", "processing": "붉은 구기자 열매를 '막걸리를 뿌려 시루에 한 번 찐 다음(주증, 酒蒸)' 다시 건조하여 신장을 보강하는 약성을 극대화합니다."},
            {"name": "산수유 (山茱萸)", "efficacy": "소양인의 빈약한 하체를 든든하게 받쳐주고 기운을 안으로 단단하게 모아줍니다.", "processing": "산수유 열매에서 '반드시 씨앗을 제거(去核)'해야 합니다. 씨앗은 정력을 상하게 하므로 껍질만 햇볕에 완전히 건조해 사용합니다."}
        ],
        "tea_recipe": "주증한 구기자 15g과 씨를 뺀 산수유 10g을 물 1.2L에 끓인 후 식혀서 시원하게 물 대용으로 수시로 음용합니다."
    },
    "태양인": {
        "name_hanja": "太陽人",
        "description": "폐의 기능은 성하고 간의 기능은 약한 '폐대간소(肺大肝小)'의 장부 구조를 지녔습니다. 기세가 웅장하고 결단성이 뛰어나 대인 관계의 리더십이 탁월하지만, 기운이 위로 쏠려 하체 관절이 쉽게 약해질 수 있는 희귀 체질입니다.",
        "daily_condition": "소변(小便)이 넉넉하고 시원하게 콸콸 잘 나올 때 체내 순환이 막힘없이 가장 완벽하게 건강한 상태(완실무병)입니다.",
        "warning_signs": "음식을 삼키기 어렵고 식도가 좁아지며 자꾸 입안에 맑은 침이나 가래 거품이 차올라 뱉어내는 열격/반위(噎膈反胃) 증상이 생기면 즉각 조율해야 하는 위급 신호입니다.",
        "acupoints_daily": [
            {"name": "신수 (腎兪, BL23)", "position": "허리 부위, 둘째 허리뼈 가시돌기 아래에서 가쪽으로 1.5치(손가락 두 마디 너비) 부위", "method": "약한 신장과 하체의 힘을 든든하게 보강해 줍니다. 양손을 뜨겁게 비벼 따뜻하게 한 뒤 허리 뒷덜미를 쓸어내립니다.", "image": "BL23.png"},
            {"name": "삼음교 (三陰交, SP6)", "position": "안쪽 복사뼈 중심에서 위로 3치 올라간 정강이뼈 뒷가장자리 안쪽", "method": "간과 신장의 음액을 동시에 자양하여 음기를 풍부하게 채워주므로 매일 지압하면 하체 힘이 강해집니다.", "image": "SP6.png"}
        ],
        "herbs": [
            {"name": "오가피 (五加皮, 가시오갈피)", "efficacy": "약한 간의 뼈 건강을 튼튼하게 이끌어주어 다리와 발의 무력감을 치료하고 하체 힘을 강화합니다.", "processing": "오가피 가지 껍질을 씻어 잘게 썬 뒤, 소금물에 가볍게 적셔 가마솥에 은근히 볶아내는 '염수초(鹽水炒)' 처리를 거쳐 하초 보강 약성을 살립니다."},
            {"name": "모과 (木瓜)", "efficacy": "기의 흐름을 원활하게 가라앉히고 식도 경련을 막아주어 역류를 방지하며 하체 쥐를 신속하게 풀어줍니다.", "processing": "잘 익은 모과를 잘라 씨를 긁어낸 후, 얇게 썰어 증기에 한 번 찐 다음(주증) 햇볕에 바짝 건조해 사용합니다."}
        ],
        "tea_recipe": "염수초 가공한 오가피 12g과 말린 모과 8g에 물 1L를 부어 달인 뒤 물 대용으로 차갑게 마십니다."
    }
}

def render_result(symptom_df, get_gdrive_image_url):
    final_constitution = st.session_state.constitution_result
    const_data = CONSTITUTION_DATA[final_constitution]
    
    # Restart Button
    if st.button("⬅️ 처음부터 다시 자가 진단하기", type="secondary"):
        st.session_state.step = "intro"
        st.session_state.answers = {}
        st.session_state.constitution_result = None
        st.rerun()
        
    st.divider()
    
    # 👑 체질 판정 결과 배너
    st.markdown(f\"\"\"
    <div class="result-header">
        <h2 style='margin:0; color:#1B5E20;'>당신의 타고난 사상체질은 <b>{final_constitution} ({const_data['name_hanja']})</b> 입니다 🎉</h2>
        <p style='margin-top:10px; font-size:1.15rem; color:#333; line-height:1.6;'>{const_data['description']}</p>
    </div>
    \"\"\", unsafe_allow_html=True)
    
    # 🌡️ 체질 기본 완실무병 & 경고등 요약
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f\"\"\"
        <div class="info-box" style="border-left-color: #2E7D32;">
            <h4 style="margin:0; color:#1B5E20;">🟢 평소 건강 지표 (완실무병 조건)</h4>
            <p style="margin-top:8px; font-size:0.95rem; color:#444;">{const_data['daily_condition']}</p>
        </div>
        \"\"\", unsafe_allow_html=True)
    with col2:
        st.markdown(f\"\"\"
        <div class="info-box" style="border-left-color: #C62828;">
            <h4 style="margin:0; color:#C62828;">🔴 아플 때 생기는 결정적 위험 신호</h4>
            <p style="margin-top:8px; font-size:0.95rem; color:#444;">{const_data['warning_signs']}</p>
        </div>
        \"\"\", unsafe_allow_html=True)

    # 탭 설계: 1. 평소 양생, 2. 5대 주요 증상별 응급 치료
    tab1, tab2 = st.tabs(["🌿 1. 평소 건강 관리 및 기본 양생", "🚨 2. [신규 추가] 5대 주요 증상별 한방 홈케어"])
    
    # [TAB 1] 평소 건강 관리
    with tab1:
        st.markdown(f"### 🍵 {final_constitution}의 평소 장부 기능 조화 가이드")
        st.write("체질적으로 부족한 원기를 부드럽게 채워주는 평소 상시 양생 수칙과 전용 약재 조제법입니다.")
        st.divider()
        
        # 평소 지압법
        st.markdown("#### ① 매일 가볍게 실천하는 2대 평소 양생혈 지압")
        for idx, pt in enumerate(const_data["acupoints_daily"]):
            st.markdown(f"**[{idx+1}] {pt['name']}**")
            c_img, c_txt = st.columns([1, 4])
            with c_img:
                img_url = get_gdrive_image_url(pt["image"])
                if img_url:
                    st.image(img_url, caption=pt["name"], width=130)
                else:
                    st.image("https://cdn-icons-png.flaticon.com/512/10415/10415848.png", 
                             caption=f"연동 대기: {pt['image']}", width=120)
            with c_txt:
                st.write(f"📌 **정확한 위치:** {pt['position']}")
                st.write(f"👉 **셀프 양생법:** {pt['method']}")
            st.divider()
            
        # 평소 약초 및 조제법
        st.markdown("#### ② 체질별 기본 맞춤형 한방 약재")
        for hb in const_data["herbs"]:
            with st.expander(f"⭐ {hb['name']} (자세히 보기)"):
                st.markdown(f"**한방 고유 효능:** {hb['efficacy']}")
                st.markdown(f"**👑 전문가 가공(법제) 요령:** <span class='accent-text'>{hb['processing']}</span>", unsafe_allow_html=True)
        st.divider()
        st.markdown("#### ③ 일상생활 추천 보약 차(藥茶) 레시피")
        st.success(f"🍵 **보약 차 섭취 공식:** {const_data['tea_recipe']}")

    # [TAB 2] 5대 주요 증상별 치료 (동적 CSV 연동)
    with tab2:
        st.markdown("### 🏥 지금 겪고 있는 불편한 증상별 체질 맞춤 처방")
        st.write("불편한 증상을 하나 선택해 주세요. 외부 DB에서 해당 체질의 기혈 막힘 원인에 최적화된 처방을 가져옵니다.")
        
        selected_symptom = st.selectbox(
            "👉 증상을 선택하세요",
            ["소화불량", "두통", "변비", "두근거림", "요통"],
            index=0
        )
        
        if symptom_df is not None:
            # CSV 데이터에서 현재 체질과 선택된 증상에 맞는 행 찾기
            filtered = symptom_df[(symptom_df["symptom"] == selected_symptom) & (symptom_df["constitution"] == final_constitution)]
            
            if not filtered.empty:
                row = filtered.iloc[0]
                
                # 증상 카드 그리기
                st.markdown(f\"\"\"
                <div class="symptom-card">
                    <h3 style="margin:0; color:#33691E;">⚡ {final_constitution}의 '{selected_symptom}' 원천 진단 및 해결 가이드</h3>
                    <p style="margin-top:10px; font-size:1.05rem; line-height:1.6; color:#444;">
                        <b>[한의학적 원인]:</b> {row['cause']}
                    </p>
                </div>
                \"\"\", unsafe_allow_html=True)
                st.write("")
                
                # 경혈 1 및 경혈 2 가이드라인 (2열 구성)
                st.markdown(f"#### 📍 {selected_symptom} 치료에 가장 효과적인 2대 침/뜸자리")
                col_pt1, col_pt2 = st.columns(2)
                
                # 경혈 1 카드
                with col_pt1:
                    st.markdown(f"##### 1️⃣ {row['acupoint1_name']} ({row['acupoint1_code']})")
                    img_url1 = get_gdrive_image_url(row['acupoint1_image'])
                    if img_url1:
                        st.image(img_url1, caption=f"{row['acupoint1_name']} 경혈 지도", use_container_width=True)
                    else:
                        st.image("https://cdn-icons-png.flaticon.com/512/2855/2855146.png", 
                                 caption=f"연동 대기: {row['acupoint1_image']}", width=120)
                    st.write(f"📌 **해부학적 위치:** {row['acupoint1_position']}")
                    st.write(f"👉 **자가 치료법 (사법):** {row['acupoint1_method']}")
                
                # 경혈 2 카드
                with col_pt2:
                    st.markdown(f"##### 2️⃣ {row['acupoint2_name']} ({row['acupoint2_code']})")
                    img_url2 = get_gdrive_image_url(row['acupoint2_image'])
                    if img_url2:
                        st.image(img_url2, caption=f"{row['acupoint2_name']} 경혈 지도", use_container_width=True)
                    else:
                        st.image("https://cdn-icons-png.flaticon.com/512/2855/2855146.png", 
                                 caption=f"연동 대기: {row['acupoint2_image']}", width=120)
                    st.write(f"📌 **해부학적 위치:** {row['acupoint2_position']}")
                    st.write(f"👉 **자가 치료법 (사법):** {row['acupoint2_method']}")
                
                st.divider()
                
                # 전용 약초 및 처방 차
                st.markdown(f"#### 🍯 {selected_symptom} 진정을 위한 체질 맞춤 전용 한방 약차")
                col_hb, col_tea = st.columns([2, 3])
                with col_hb:
                    st.info(f"🌿 **추천 약재:** **{row['herb_name']}**")
                    st.write(f"**약리 작용 및 효능:** {row['herb_efficacy']}")
                    st.write(f"**👑 전문가 법제(가공)법:**")
                    st.markdown(f"<span class='accent-text'>{row['herb_processing']}</span>", unsafe_allow_html=True)
                with col_tea:
                    st.success(f"🍵 **가정용 홈케어 약차 조제식:**")
                    st.write(row['tea_recipe'])
            else:
                st.error("해당 체질 및 증상에 맞는 데이터셋이 존재하지 않습니다.")
        else:
            st.error("⚠️  파일을 찾을 수 없어 실시간 치료법을 불러오지 못했습니다. 깃허브 저장소에 파일을 함께 업로드해 주세요!")
''',
    r'''views/Symptoms.py''': r'''# -*- coding: utf-8 -*-
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
''',
    r'''views/Physiology.py''': r'''# -*- coding: utf-8 -*-
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
''',
    r'''views/Personality.py''': r'''# -*- coding: utf-8 -*-
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
''',
    r'''views/BodyShape.py''': r'''# -*- coding: utf-8 -*-
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
''',
    r'''views/Intro.py''': r'''# -*- coding: utf-8 -*-
import streamlit as st

def render_intro():
    st.subheader("🌿 사상의학 자가 건강 진단 시작")
    st.write(\"\"\"
    본 자가 진단은 동무 이제마 선생의 『동의수세보원』 원전에 기록된 핵심 진단 지표들을 기반으로 구성되었습니다.
    총 **15개의 문항**을 거치며 여러분의 체형, 성격, 평소의 생리 지표, 그리고 아플 때 나타나는 특이 증상들을 종합 분석합니다.
    
    진단 결과에 따라 평소에 원기를 보하는 **양생 지압 및 맞춤 법제 약차 조제법**과,
    갑작스러운 불편함이 있을 때 이를 즉각 완화해 주는 **5대 증상별 정밀 치료 카드**를 제공합니다.
    \"\"\")
    st.divider()
    
    st.info("💡 **진단 안내**: 더 높은 정확도를 위해 본인의 평소 컨디션과 외형, 기질에 가장 가까운 답변을 진중하게 골라주세요.")
    st.write("")
    
    if st.button("🔮 체질 자가 진단 시작하기", type="primary", use_container_width=True):
        st.session_state.step = "bodyshape"
        st.rerun()
''',
    r'''core/scoring.py''': r'''# -*- coding: utf-8 -*-
def calculate_scores(answers):
    \"\"\"답변 데이터를 받아 각 체질별 점수를 정밀 계산합니다.\"\"\"
    scores = {"태음인": 0.0, "소음인": 0.0, "소양인": 0.0, "태양인": 0.0}
    for q_id, opt in answers.items():
        # opt는 선택된 option 딕셔너리
        weight = opt.get("weight", 1.0)
        for const, val in opt.get("scores", {}).items():
            scores[const] += val * weight
    return scores
''',
    r'''core/questionnaire.py''': r'''# -*- coding: utf-8 -*-
QUESTIONS = [
    {
        "id": 1,
        "category": "체형 및 외모 (기상)",
        "question": "거울을 보거나 남들이 말할 때, 나의 전체적인 신체 실루엣과 가장 가까운 것은 무엇인가요?",
        "options": [
            {"text": "목덜미 부근(목과 어깨 사이)의 기세는 우뚝 솟아 발달해 보이나, 상대적으로 엉덩이와 하체가 외롭고 빈약해 보인다.", "scores": {"태양인": 1.0}},
            {"text": "가슴둘레(상체) 부위가 떡 벌어지고 실해 보이나, 엉덩이와 골반 부위가 빈약하여 앉아 있는 자세가 다소 불안정해 보인다.", "scores": {"소양인": 1.0}},
            {"text": "허리둘레와 복부(요척)가 튼튼하게 발달하여 골격이 듬직하고 기세가 장대하지만, 상대적으로 목덜미 기운은 약해 보인다.", "scores": {"태음인": 1.0}},
            {"text": "엉덩이와 골반(이둔) 부위가 잘 발달하여 앉아 있는 자세가 매우 안정적이고 아담하지만, 가슴둘레와 상체 기세가 좁고 빈약해 보인다.", "scores": {"소음인": 1.0}}
        ],
        "weight": 1.0
    },
    {
        "id": 2,
        "category": "성격 및 재간 (성정)",
        "question": "업무를 처리하거나 대인 관계에서 나타나는 나만의 가장 돋보이는 행동 스타일은 무엇인가요?",
        "options": [
            {"text": "새로운 사람들과 막힘없이 적극적으로 소통하고 대인 관계를 넓히는 일(교우)에 뛰어난 과단성이 있다.", "scores": {"태양인": 1.0}},
            {"text": "행동이 민첩하고 굳세며, 공적인 업무나 어려운 사무를 시원시원하고 빠르게 처리하는 데 유능하다.", "scores": {"소양인": 1.0}},
            {"text": "한 번 정착한 곳에서 묵묵하게 일을 꾸준히 진행하며, 어떤 난관이 있어도 끝까지 일(거처)을 완수해 내는 인내심이 있다.", "scores": {"태음인": 1.0}},
            {"text": "매사에 온화하고 침착하며 치밀하게 생각하고 계획을 짜며, 내적인 무리를 조화롭게 조직하고 이끄는 데 장점이 있다.", "scores": {"소음인": 1.0}}
        ],
        "weight": 1.0
    },
    {
        "id": 3,
        "category": "완실무병 (건강할 때의 핵심 지표)",
        "question": "몸 컨디션이 최고조로 좋아 '아주 건강하다'고 느낄 때 나타나는 대표적인 내 몸의 신호는 무엇인가요?",
        "options": [
            {"text": "소변이 막힘없이 시원하게 아주 잘 나오고 양이 넉넉할 때 몸이 가볍다.", "scores": {"태양인": 1.5}},
            {"text": "대변이 하루라도 거르지 않고 막힘없이 아주 부드럽고 시원하게 매일 잘 나온다.", "scores": {"소양인": 1.5}},
            {"text": "운동이나 목욕(사우나)을 통해 전신 땀구멍이 열려 땀을 흠뻑 개운하게 흘리고 나도 피곤하지 않고 몸이 개운하다.", "scores": {"태음인": 1.5}},
            {"text": "음식을 찬 것이든 뜨거운 것이든 가리지 않고 맛있게 먹고, 체기 없이 소화가 아주 훌륭하게 잘 된다.", "scores": {"소음인": 1.5}}
        ],
        "weight": 1.5
    },
    {
        "id": 4,
        "category": "특이 병증 (몸이 지치거나 아플 때)",
        "question": "극도로 피곤하거나 컨디션이 악화되었을 때 몸에서 즉각적으로 나타나는 고유한 불편함은 무엇인가요?",
        "options": [
            {"text": "음식물을 삼키는 목구멍이나 식도가 뻑뻑하게 좁아지는 느낌이 들거나, 속에서 신침이나 맑은 침이 솟구쳐 토하려 한다.", "scores": {"태양인": 1.5}},
            {"text": "대변이 하루이틀만 통하지 않아도 아랫배가 더부룩해지면서 가슴 속이 불이 붙는 듯이 뜨거워지고 머리가 지끈거린다.", "scores": {"소양인": 1.5}},
            {"text": "기가 위로 솟구치며 이유 없이 가슴이 쿵쾅거리고 울렁거리거나(정충증), 눈꺼풀이 미세하게 떨리고 눈 속 깊은 곳이 쏘듯이 아프다.", "scores": {"태음인": 1.5}},
            {"text": "가끔 평소에 깊은 한숨을 크게 쉬며, 몸살 기운에 억지로 땀을 흘리고 나면 힘이 쏙 빠지고 몸이 더 처지고 극도로 피로해진다.", "scores": {"소음인": 1.5}}
        ],
        "weight": 1.5
    },
    {
        "id": 5,
        "category": "피부 및 뼈마디의 감각 (정밀 확인)",
        "question": "나의 피부 상태 및 만졌을 때의 탄력, 뼈마디의 전반적인 결합 상태는 어떠한가요?",
        "options": [
            {"text": "피부나 근육질이 비교적 조밀하지 못하고 살결이 거칠거나 보통이며, 서 있는 하반신의 관절이 쉽게 떨리거나 허약하다.", "scores": {"태양인": 1.5}},
            {"text": "상반신(어깨, 가슴)에 힘이 많이 들어가며 뼈대가 견고하나, 상대적으로 발이 다소 가볍고 걸음걸이가 매우 빠르다.", "scores": {"소양인": 1.5}},
            {"text": "피부 가죽이 연하지 않고 비교적 두껍거나 듬직하며, 피부가 야무지게 단단하고 조여드는 느낌이 들면 몸에 병이 있는 신호이다.", "scores": {"태음인": 1.5}},
            {"text": "살결이 대단히 부드럽고 고우며, 손끝으로 만졌을 때 살가죽과 근육이 매우 짜임새 있고 야무지게 단단해야 건강한 상태이다.", "scores": {"소음인": 1.5}}
        ],
        "weight": 1.5
    },
    {
        "id": 6,
        "category": "성격 및 사회성 (정밀 확인)",
        "question": "일을 대하는 태도와 행동적인 특징에서 나와 가장 잘 맞는 성향은 무엇인가요?",
        "options": [
            {"text": "기세가 남보다 우수하고 남의 위에 서기를 좋아하며 비타협적인 결단력을 지녔다.", "scores": {"태양인": 1.0}},
            {"text": "성정이 급하고 새로운 일을 잘 벌이나 마무리가 흐지부지되는 경향이 있다.", "scores": {"소양인": 1.0}},
            {"text": "행동이 점잖고 무거우며, 어떤 일에 시작하면 우직하게 고집을 부려 반드시 마친다.", "scores": {"태음인": 1.0}},
            {"text": "소박하고 단정하며 남에게 지기 싫어하는 자존심이 세고 세심한 성격이다.", "scores": {"소음인": 1.0}}
        ],
        "weight": 1.0
    },
    {
        "id": 7,
        "category": "스트레스 및 성질 (정밀 확인)",
        "question": "스트레스 상황이 닥쳤을 때 마음속으로 느끼는 성질과 내적 극단성은 무엇인가요?",
        "options": [
            {"text": "화를 낼 때 노를 극도로 발하고 물러서지 않는 영웅적인 기개가 솟구친다.", "scores": {"태양인": 1.0}},
            {"text": "한 번 노하면 조급함이 생겨 안절부절못하고 일이 안 풀리면 화를 버럭 낸다.", "scores": {"소양인": 1.0}},
            {"text": "마음속에 은연중 겁이 많아 무언가를 지키지 못할까 봐 겁내는 마음(겁심)이 늘 바탕에 흐른다.", "scores": {"태음인": 1.0}},
            {"text": "매사에 조심스럽고 내심 불안해하는 마음(불안심)이 항상 마음속에 도사리고 있다.", "scores": {"소음인": 1.0}}
        ],
        "weight": 1.0
    },
    {
        "id": 8,
        "category": "인생관 및 삶의 지표",
        "question": "본인이 평소 추구하거나 중요하게 생각하는 삶의 리더십이나 재간은 무엇인가요?",
        "options": [
            {"text": "널리 사방을 개척하고 큰 흐름을 대담하게 추진하며, 소통(교우)의 과단성이 뛰어나다.", "scores": {"태양인": 1.0}},
            {"text": "밖의 공적인 용무나 여러 사람과 조율하며 문제를 시원하고 빠르게 해결하는 일(사무)에 재능이 있다.", "scores": {"소양인": 1.0}},
            {"text": "한자리에 안정적으로 머무르며 가정을 소중히 하고 성과를 묵묵히 쌓는 일(거처)에 뛰어난 능력이 있다.", "scores": {"태음인": 1.0}},
            {"text": "동료와 팀 내적인 관계를 세심하고 긴밀하게 조율하여 화합을 도모하는 일(당여)에 유능하다.", "scores": {"소음인": 1.0}}
        ],
        "weight": 1.0
    },
    {
        "id": 9,
        "category": "땀(汗)의 생리 반응 (정밀 소증)",
        "question": "평소 일상 활동이나 더울 때 흘리는 땀의 반응은 어떠한가요?",
        "options": [
            {"text": "땀이 전신에 고르게 흠뻑 흘려야 몸이 개운하고 가벼워지며 피로가 싹 가신다.", "scores": {"태음인": 1.5}},
            {"text": "평소 땀이 잘 나지 않는 편이며, 억지로 땀을 흘리거나 사우나를 오래 하면 오히려 기운이 탈진해 쓰러질 듯 피로하다.", "scores": {"소음인": 1.5}},
            {"text": "체온 조절을 위해 적당하게 흐르는 땀은 전혀 피로를 부르지 않으나, 손발이나 이마 부위에 땀이 마르지 않고 잘 난다.", "scores": {"소양인": 1.0}},
            {"text": "땀 자체의 양이 많지 않은 편이며, 건강 상태에 따라 땀의 양이 크게 좌우되지 않고 늘 보통이다.", "scores": {"태양인": 1.0}}
        ],
        "weight": 1.5
    },
    {
        "id": 10,
        "category": "소화 및 식생활 (정밀 소증)",
        "question": "음식물을 섭취하거나 체할 때, 평소 위장의 반응은 어떤 특징을 보이나요?",
        "options": [
            {"text": "소화력이 약해 평소 찬 물이나 찬 음식을 먹으면 위장이 불편해지며, 뱃속에서 끓는 소리가 나고 설사하기 쉽다.", "scores": {"소음인": 1.5}},
            {"text": "소화력이 대단히 뛰어나 돌도 씹어 먹을 정도로 무엇이든 식욕이 왕성하고, 체하는 일이 거의 없이 뱃속이 든든하다.", "scores": {"태음인": 1.0}},
            {"text": "위장의 기가 성해 매운 것이나 기름진 것을 자주 먹으면 가슴에 열이 차며 체했을 때 가슴속이 뜨거워진다.", "scores": {"소양인": 1.5}},
            {"text": "식도가 예민하고 상체 기운이 강해 음식을 잘못 삼키면 뻑뻑한 느낌이 들며 위장 부위가 정체되는 편이다.", "scores": {"태양인": 1.5}}
        ],
        "weight": 1.5
    },
    {
        "id": 11,
        "category": "대변 및 변비 상태 (정밀 소증)",
        "question": "평소 대변의 습관이나 대변이 안 통할 때 몸의 자각 반응은 어떠한가요?",
        "options": [
            {"text": "대변이 하루나 이틀만 통하지 않아도 아랫배가 더부룩해지면서 가슴이 불타듯 뜨거워지고 머리가 지끈거리며 예민해진다.", "scores": {"소양인": 1.5}},
            {"text": "대변이 평소 묽거나 무르게 자주 나오는 편이며, 몸에 병이 생기면 갑자기 설사로 콸콸 쏟아져 원기가 하강하는 위급함이 생긴다.", "scores": {"소음인": 1.5}},
            {"text": "대변의 주기가 2~3일 정도로 다소 긴 편이고 단단하게 나오더라도, 가슴 답답함 없이 몸 상태는 늘 시원하고 무던하다.", "scores": {"태음인": 1.0}},
            {"text": "대변 상태는 보통이며 변비나 설사에 의해 전체 컨디션이 심각하게 변하지 않고 비교적 균형적이다.", "scores": {"태양인": 1.0}}
        ],
        "weight": 1.5
    },
    {
        "id": 12,
        "category": "소변 및 진액 순환 (정밀 소증)",
        "question": "평소 소변의 양과 소변을 보고 난 후 몸의 기운 느낌은 어떠한가요?",
        "options": [
            {"text": "소변의 양이 매우 풍부하고 막힘없이 시원하게 콸콸 나올 때 온몸이 개운하고 가벼워지며 기력이 상승한다.", "scores": {"태양인": 1.5}},
            {"text": "밤에 소변을 자주 보러 가거나 피로할 때 소변 횟수가 급증하는 편이며 하체에 약간의 무력감이 생긴다.", "scores": {"소양인": 1.0}},
            {"text": "보통 수준의 양과 횟수를 나타내며, 소변보다는 주로 땀이나 호흡 순환 상태에 더 많은 컨디션 영향을 받는다.", "scores": {"태음인": 1.0}},
            {"text": "소변에 큰 불편함이나 신체 반응 변화를 거의 느끼지 못하는 일반적인 양상을 보인다.", "scores": {"소음인": 1.0}}
        ],
        "weight": 1.5
    },
    {
        "id": 13,
        "category": "급성 소화기 거부 (병증 정밀)",
        "question": "급격히 아플 때나 평소 몸 상태가 극도로 지칠 때, 목구멍이나 명치의 특징적인 병증 반응은 어떠한가요?",
        "options": [
            {"text": "음식물을 삼키는 목구멍과 식도 부근이 뻑뻑하게 조여 오거나, 자꾸 맑은 가래 거품과 침이 솟구쳐 나와 토하려고 한다.", "scores": {"태양인": 1.5}},
            {"text": "체할 때 가슴 밑 명치 부위가 돌덩이를 얹은 듯이 딱딱하게 막히며 가슴속이 화끈화끈 달아오르고 초조해진다.", "scores": {"소양인": 1.5}},
            {"text": "소화불량이 오면 아랫배가 차가워지면서 쥐어짜듯 살살 아프고, 따뜻한 손으로 쓸어내리거나 온열팩을 대야 진정된다.", "scores": {"소음인": 1.5}},
            {"text": "소화기 자체보다 머리와 목덜미가 굳어가면서 머리가 맑지 못하고 멍해지는 피로감 위주로 온다.", "scores": {"태음인": 1.0}}
        ],
        "weight": 1.5
    },
    {
        "id": 14,
        "category": "두근거림 및 불안 (병증 정밀)",
        "question": "컨디션이 극도로 저하되었을 때, 가슴의 두근거림이나 심리적 상태는 어떠한가요?",
        "options": [
            {"text": "기가 위로 쏠리며 이유 없이 가슴이 미친 듯이 쿵쾅거리고 울렁거려 큰 불안감(정충증)을 느껴 자꾸만 집 안에 웅크리려 한다.", "scores": {"태음인": 1.5}},
            {"text": "평소 한숨을 깊게 자주 쉬며 가슴이 꽉 찬 듯 답답하고 억울한 감정이나 슬픈 기분이 지배하기 쉽다.", "scores": {"소음인": 1.5}},
            {"text": "가슴에 화(火)가 가득 차올라 사소한 말이나 대화에도 신경질적으로 버럭 화가 나고 가슴속에 열불이 치솟는다.", "scores": {"소양인": 1.5}},
            {"text": "심장이나 가슴 증상보다는 주로 하체 다리 관절이 쉽게 후들후들 떨려 오래 서 있지 못하고 자꾸 앉으려는 무력이 온다.", "scores": {"태양인": 1.0}}
        ],
        "weight": 1.5
    },
    {
        "id": 15,
        "category": "추위 및 더위 민감도 (병증 정밀)",
        "question": "손발 및 아랫배의 온도감과 평소 추위/더위를 견디는 힘은 어떠한가요?",
        "options": [
            {"text": "온몸과 손발, 아랫배가 대단히 차가운 편(수족냉증)이라 찬 바람만 불어도 온몸을 웅크리고 옷을 항상 두껍게 입어야 한다.", "scores": {"소음인": 1.5}},
            {"text": "상반신(머리와 가슴)에는 열이 펄펄 끓고 더위를 지독히 못 참는 반면, 아랫배나 엉덩이 부위는 서늘하여 상열하한증이 뚜렷하다.", "scores": {"소양인": 1.5}},
            {"text": "더위를 많이 타고 땀을 자주 흘리는 편이나 몸 자체의 기력은 탄탄하여 차가운 에어컨 바람이나 찬 음료를 먹어야 몸이 식는다.", "scores": {"태음인": 1.0}},
            {"text": "하반신과 척추가 쉽게 냉해지기 쉬우나, 몸 안의 기는 항상 건조하고 상승하여 전형적인 마른 편 체격을 유지한다.", "scores": {"태양인": 1.0}}
        ],
        "weight": 1.5
    }
]
''',
}

def main():
    print("🌿 사상의학 모듈러 프로젝트 구조 빌드를 시작합니다...")
    success_count = 0
    for rel_path, content in FILES.items():
        # Ensure parent directories exist
        parent_dir = os.path.dirname(rel_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        
        # Write the file
        with open(rel_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [생성 완료] {rel_path}")
        success_count += 1
        
    print(f"\n🎉 빌드가 성공적으로 완료되었습니다! (총 {success_count}개 파일 생성)")
    print("👉 실행 방법:")
    print("   1. pip install -r requirements.txt")
    print("   2. streamlit run app.py")

if __name__ == '__main__':
    main()
