import streamlit as st
import os
import sys

# Ensure artifacts folder or current folder is in path to import sasang_app_prototype
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from sasang_app_prototype import CONSTITUTION_DATA, QUESTIONS
except ImportError:
    # Fallback if importing from adjacent folder in workspace
    sys.path.append('/workspace/artifacts')
    from sasang_app_prototype import CONSTITUTION_DATA, QUESTIONS

# Page Configuration
st.set_page_config(
    page_title="사상의학 자가 진단 및 한방 홈케어 가이드",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Hiding default Streamlit footers and polishing font sizes)
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        color: #2E7D32;
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
    .stRadio > label {
        font-weight: bold;
        color: #1B5E20;
        font-size: 1.05rem;
    }
    .result-header {
        background-color: #E8F5E9;
        padding: 20px;
        border-radius: 10px;
        border-left: 8px solid #2E7D32;
        margin-bottom: 20px;
    }
    .card-title {
        font-size: 1.2rem;
        color: #2E7D32;
        font-weight: bold;
        margin-top: 10px;
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
</style>
""", unsafe_allow_html=True)

# App Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/194/194203.png", width=80)
    st.header("🌿 사상체질 홈케어")
    st.write("본 앱은 동무 이제마 선생의 **『동의수세보원』** 원전 및 전문 한방 경혈·약재 데이터베이스를 기반으로 구축되었습니다.")
    st.divider()
    st.markdown("""
    ### 📱 주요 기능
    1. **사상체질 정밀 진단**
    2. **평소 양생 가이드 (보법)**
    3. **아플 때 긴급 가이드 (사법)**
    4. **약재 법제(가공) 및 한방 차 조제**
    """)
    st.divider()
    st.info("💡 **경혈 이미지 연결 팁:** 구글 드라이브 '경혈맵' 폴더의 이미지를 앱에 연동할 때, 구글 시트에 `https://drive.google.com/uc?export=view&id=파일고유ID` 형태로 직접 링크 주소를 입력하면 이곳에 실시간으로 이미지가 렌더링됩니다.")

# Header
st.markdown('<div class="main-title">🌿 사상체질 자가 진단 및 한방 홈케어 가이드</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">체질 진단을 바탕으로 평소 건강을 지키는 지압법과 아플 때 유용한 응급 경혈, 체질 맞춤 약재 가공법을 알아보세요.</div>', unsafe_allow_html=True)

# Check state to switch between Diagnosis Form and Results
if "diagnosis_completed" not in st.session_state:
    st.session_state.diagnosis_completed = False
if "constitution_result" not in st.session_state:
    st.session_state.constitution_result = None

# ----------------- VIEW 1: DIAGNOSIS FORM -----------------
if not st.session_state.diagnosis_completed:
    st.subheader("📋 5대 원전 기반 체질 판별 테스트")
    st.write("신중하게 읽어보신 후, 본인에게 가장 가깝다고 생각되는 항목을 하나만 선택해 주세요.")
    
    # Render Questions Dynamically
    user_answers = {}
    for q in QUESTIONS:
        st.markdown(f"**Q{q['id']}. [{q['category']}] {q['question']}**")
        options_texts = [opt["text"] for idx, opt in enumerate(q["options"])]
        
        # Display as Radio Button
        choice = st.radio(
            label=f"q_{q['id']}_label",
            options=options_texts,
            index=0,
            key=f"q_{q['id']}",
            label_visibility="collapsed"
        )
        # Find corresponding index and scores
        selected_option = next(opt for opt in q["options"] if opt["text"] == choice)
        user_answers[q["id"]] = selected_option
        st.write("") # Line break

    st.divider()
    
    # Diagnose Button
    if st.button("🔮 나의 사상체질 진단 결과 확인하기", type="primary", use_container_width=True):
        # Calculate Scores with weights
        scores = {"태음인": 0.0, "소음인": 0.0, "소양인": 0.0, "태양인": 0.0}
        for q in QUESTIONS:
            selected_option = user_answers[q["id"]]
            weight = q["weight"]
            for const, val in selected_option["scores"].items():
                scores[const] += val * weight
                
        # Find winner
        winner = max(scores, key=scores.get)
        st.session_state.constitution_result = winner
        st.session_state.diagnosis_completed = True
        st.rerun()

# ----------------- VIEW 2: RESULTS & HEALTHCARE -----------------
else:
    final_constitution = st.session_state.constitution_result
    result = CONSTITUTION_DATA[final_constitution]
    
    # Back to Diagnosis button
    if st.button("⬅️ 다시 진단하기", type="secondary"):
        st.session_state.diagnosis_completed = False
        st.session_state.constitution_result = None
        st.rerun()
        
    st.divider()
    
    # 👑 Big Result Banner
    st.markdown(f"""
    <div class="result-header">
        <h2 style='margin:0; color:#1B5E20;'>당신의 타고난 사상체질은 <b>{final_constitution} ({result['name_hanja']})</b> 입니다 🎉</h2>
        <p style='margin-top:10px; font-size:1.15rem; color:#333; line-height:1.6;'>{result['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 🌡️ Health Status Summary Card
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="info-box" style="border-left-color: #2E7D32;">
            <h4 style="margin:0; color:#1B5E20;">🟢 평소 건강 지표 (완실무병 조건)</h4>
            <p style="margin-top:8px; font-size:0.95rem; color:#444;">{result['daily_condition']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="info-box" style="border-left-color: #C62828;">
            <h4 style="margin:0; color:#C62828;">🔴 아플 때 생기는 결정적 위험 신호</h4>
            <p style="margin-top:8px; font-size:0.95rem; color:#444;">{result['warning_signs']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("💡 나의 체질 맞춤 한방 홈케어 솔루션")
    
    # Tab View for interactive navigation
    tab1, tab2, tab3 = st.tabs(["🌿 평소 양생 모드 (보법)", "⚡ 긴급 치료 모드 (사법)", "🍯 약재 법제 및 차 조제법"])
    
    # TAB 1: Daily Acupoints
    with tab1:
        st.markdown("### 🌿 평소 몸의 기운을 보강해주는 예방용 경혈")
        st.caption("비교적 부드러운 지압이나 따뜻한 온열 뜸(구법)을 사용하여 장부의 부족한 원기를 채워줍니다.")
        
        for idx, pt in enumerate(result['acupoints_daily']):
            st.markdown(f"#### **{idx+1}. {pt['name']}**")
            col_img, col_txt = st.columns([1, 3])
            with col_img:
                # Placeholder image indicating Google Drive integration
                st.image("https://cdn-icons-png.flaticon.com/512/10415/10415848.png", 
                         caption="구글드라이브 연동 경혈 이미지 (예시)", width=130)
            with col_txt:
                st.write(f"📌 **정확한 해부학적 위치:** {pt['position']}")
                st.write(f"👉 **셀프 지압/양생 가이드:** {pt['method']}")
            st.divider()
            
    # TAB 2: Acute Acupoints
    with tab2:
        st.markdown("### ⚡ 갑작스러운 통증이나 병증이 생겼을 때의 조율용 경혈")
        st.caption("막힌 기혈 순환을 강력하게 뚫고 뭉친 열을 내려주기 위해, 손끝이나 지압봉으로 뻐근한 자극(사법)을 줍니다.")
        
        for idx, pt in enumerate(result['acupoints_acute']):
            st.markdown(f"#### **{idx+1}. {pt['name']}**")
            col_img, col_txt = st.columns([1, 3])
            with col_img:
                # Placeholder image indicating Google Drive integration
                st.image("https://cdn-icons-png.flaticon.com/512/2855/2855146.png", 
                         caption="구글드라이브 연동 경혈 이미지 (예시)", width=130)
            with col_txt:
                st.write(f"📌 **정확한 해부학적 위치:** {pt['position']}")
                st.write(f"👉 **자가 지압 및 사법 치료법:** {pt['method']}")
            st.divider()
            
    # TAB 3: Herbs & Recipes
    with tab3:
        st.markdown("### 🍯 약재 전문가 법제(가공)법 및 조제 레시피")
        st.caption("사상의학 원전에 수록된 체질 맞춤 약재들로, 한의학의 독특한 독성 제거 및 약성 활성화 법제법입니다.")
        
        for hb in result['herbs']:
            with st.expander(f"⭐ {hb['name']} (자세히 보기)"):
                st.markdown(f"**한방 고유 효능:** {hb['efficacy']}")
                st.markdown(f"**👑 전문가 법제(가공) 가이드:** <span class='accent-text'>{hb['processing']}</span>", unsafe_allow_html=True)
                
        st.divider()
        st.markdown("#### 🍵 일상생활 건강 차(藥茶) 조제법")
        st.success(f"**추천 레시피:** {result['tea_recipe']}")
