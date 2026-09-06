# -*- coding: utf-8 -*-
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
    # 1. 원래 진단받은 체질을 기억합니다.
    diagnosed_const = st.session_state.constitution_result
    
    # 2. 결과 페이지 상단에 다른 체질을 수동 선택할 수 있는 드롭다운 메뉴를 배치합니다.
    const_list = ["태음인", "소음인", "소양인", "태양인"]
    final_constitution = st.selectbox(
        "🔍 [체질 강제 변경] 다른 사상체질의 건강 가이드도 구경해 보세요!",
        options=const_list,
        index=const_list.index(diagnosed_const)
    )
    
    const_data = CONSTITUTION_DATA[final_constitution]
    
    # 3. 만약 원래 내 실제 진단 결과와 다른 체질을 선택했다면 파란색 안내 배너를 띄워줍니다.
    if final_constitution != diagnosed_const:
        st.info(f"💡 현재 실제 진단 결과인 **{diagnosed_const}** 대신, 임의로 선택하신 **{final_constitution}**의 건강 가이드를 보고 계십니다.")
        
    # Restart Button
    if st.button("⬅️ 처음부터 다시 자가 진단하기", type="secondary"):
        st.session_state.step = "intro"
        st.session_state.answers = {}
        st.session_state.constitution_result = None
        st.rerun()
        
    st.divider()
    
    # 👑 체질 판정 결과 배너
    st.markdown(f"""
    <div class="result-header">
        <h2 style='margin:0; color:#1B5E20;'>당신의 타고난 사상체질은 <b>{final_constitution} ({const_data['name_hanja']})</b> 입니다 🎉</h2>
        <p style='margin-top:10px; font-size:1.15rem; color:#333; line-height:1.6;'>{const_data['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 🌡️ 체질 기본 완실무병 & 경고등 요약
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="info-box" style="border-left-color: #2E7D32;">
            <h4 style="margin:0; color:#1B5E20;">🟢 평소 건강 지표 (완실무병 조건)</h4>
            <p style="margin-top:8px; font-size:0.95rem; color:#444;">{const_data['daily_condition']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="info-box" style="border-left-color: #C62828;">
            <h4 style="margin:0; color:#C62828;">🔴 아플 때 생기는 결정적 위험 신호</h4>
            <p style="margin-top:8px; font-size:0.95rem; color:#444;">{const_data['warning_signs']}</p>
        </div>
        """, unsafe_allow_html=True)

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
                st.markdown(f"""
                <div class="symptom-card">
                    <h3 style="margin:0; color:#33691E;">⚡ {final_constitution}의 '{selected_symptom}' 원천 진단 및 해결 가이드</h3>
                    <p style="margin-top:10px; font-size:1.05rem; line-height:1.6; color:#444;">
                        <b>[한의학적 원인]:</b> {row['cause']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
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
