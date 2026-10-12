# -*- coding: utf-8 -*-
import streamlit as st
import os
import pandas as pd

# ==============================================================================
# [필독] 구글 드라이브 경혈 이미지 고유 ID 매핑 설정
# 구글 드라이브에 올린 이미지 파일의 공유 링크에서 고유 ID를 가져와 아래에 적어주세요.
# ==============================================================================
GDRIVE_FILE_IDS = {
    # 13개 기본 핵심 경혈 이미지
    "LU9.png": "1VU9zgUa_XRsTQ4YAV-JrYCmibcDH1jN1",    # 태연 (태음인 평소 / 태음인 두근거림)
    "LU7.png": "1teSFmDtMQ8N03Oe2WbwG5h29AWkx3sQx",    # 열결 (태음인 평소)
    "LR3.png": "1WjeuZHNkp4IB7Qz0pob5TVt3GilgH9Kp",    # 태충 (태음인 소화불량·두통·변비·요통)
    "LR2.png": "1uQ0Jkz5RwgtY_ebKSI7SEac_MBVnmMn-",    # 행간 (태음인 소화불량)
    "SP6.png": "1qMIcTi35Ck8km9KcehY56vCv48JloLDM",    # 삼음교 (소음인/태양인 평소 외)
    "CV6.png": "1xyvD-YHRHBGfq9cvJRO9DYwTJqrdRxeM",    # 기해 (소음인 평소 외)
    "LI4.png": "1-lk9zMhKnuOqnSGEDBHg1GPaoVnCy_mk",    # 합곡 (소음인/태양인)
    "LU11.png": "11ZZu7A_YT-2iY8fNwT7hD9ghMGFOT3TQ",   # 소상 (태양인)
    "SP9.png": "1g6FRjkvr4E5Z7OiZCLcwAjuEco0ic_rK",    # 음릉천 (소양인 평소 / 소양인 변비)
    "PC6.png": "1rf1j8-xFurVBvw5ooqhiI5oxgo3PnzqL",    # 내관 (소양인 평소 외)
    "ST36.png": "15uMHdutKXVX_blowl188q56XYuHzie0m",   # 족삼리 (소양인 소화불량·요통)
    "TE6.png": "1epLxmBRrBsEo1gb3nljh39xPzs7lBN19",    # 지구 (소양인 두통·변비)
    "BL23.png": "1dUFiwR_TsTELeUZnYsGd56Hkil8UVT7a",   # 신수 (태양인 평소 외)

    # 5대 증상 확장용 추가 경혈 이미지
    "GB20.png": "1aXCkct9B0ITr7dN0mu2Egr4ieJg9ZIj2",   # 풍지 (태음인 두통)
    "GV20.png": "1Uw2fFJnue8Q4Ern_SmkIgP4w4YE2NheW",   # 백회 (소음인 두통 / 태양인 두통)
    "EXHN5.png": "1C8OBPEMATmgtM2fXwcwBKkb7DLHL3g4C",  # 태양 (소양인 두통)
    "ST25.png": "1J6hpGETULMqx1eD7JcBBQxsKUsU-nuaT",   # 천추 (태음인 변비)
    "HT7.png": "1K3d9JahX0OjA0OJoMuaefe45cREgi3yl",    # 신문 (태음인/태양인 두근거림)
    "BL40.png": "15Pqh2nBAPi2ZGRcfTx5Rovy7IAA5G9b2",   # 위중 (태음인 요통)
}


def get_gdrive_image_url(image_filename):
    """구글 드라이브 고유 파일 ID로 이미지 URL을 만듭니다."""
    file_id = GDRIVE_FILE_IDS.get(image_filename, "")
    if file_id and file_id.strip():
        return f"https://lh3.googleusercontent.com/d/{file_id.strip()}"
    return None


CONSTITUTIONS = ["태음인", "소음인", "소양인", "태양인"]

# ==============================================================================
# [안전] 임산부 금기 혈자리 / 약재 주의 / 증상별 병원 방문 신호
# ==============================================================================
PREGNANCY_CAUTION_CODES = {"SP6": "삼음교", "LI4": "합곡"}

HERB_CAUTIONS = {
    "인삼": "고혈압이 있거나 항응고제·당뇨약을 복용 중이면 주의가 필요합니다. 열이 많은 사람은 두근거림·불면이 생길 수 있습니다.",
    "당귀": "피 순환을 돕는(활혈) 약재라 임신 중이거나 항응고제(와파린 등)를 복용 중이면 피하세요.",
    "천궁": "피 순환을 돕는(활혈) 약재라 임신 중이거나 항응고제를 복용 중이면 피하세요.",
    "산조인": "졸림을 유발할 수 있어 운전이나 기계 조작 전에는 피하세요.",
    "숙지황": "소화가 약한 사람은 더부룩함이나 설사가 생길 수 있습니다.",
    "생지황": "성질이 차서 소화가 약하거나 설사가 잦은 사람은 피하세요.",
    "의이인": "임신 중에는 섭취를 피하는 것이 좋다고 알려져 있습니다.",
}

GENERAL_HERB_NOTE = "복용 중인 약이 있거나 임신·수유 중이거나 지병이 있다면, 약차를 마시기 전에 한의사와 상담하세요."

RED_FLAGS = {
    "소화불량": [
        "음식을 삼키기 어려운 증상이 계속됨",
        "피가 섞인 구토, 검은 변",
        "이유 없는 체중 감소",
        "참기 힘든 복통",
    ],
    "두통": [
        "갑자기 시작된, 살면서 가장 심한 두통",
        "팔다리 마비, 말이 어눌해짐, 시야 이상",
        "고열과 함께 목이 뻣뻣함",
        "머리를 부딪친 뒤 생긴 두통",
    ],
    "변비": [
        "피가 섞인 변",
        "심한 복통·구토와 함께 가스도 나오지 않음",
        "평소 배변 습관이 갑자기 바뀜 (특히 40대 이상)",
        "이유 없는 체중 감소",
    ],
    "두근거림": [
        "가슴 통증이나 가슴을 짓누르는 느낌",
        "숨이 차거나 호흡이 곤란함",
        "실신하거나 쓰러질 듯 어지러움",
        "맥이 매우 빠르거나 불규칙한 상태가 계속됨",
    ],
    "요통": [
        "다리 저림이나 다리 힘 빠짐",
        "대소변 조절이 잘 안 됨",
        "열이 함께 남",
        "넘어지거나 부딪친 뒤 생긴 통증, 밤에도 계속되는 통증",
    ],
}

# 응급 가능성이 있어 119를 먼저 안내하는 증상
EMERGENCY_SYMPTOMS = {"두근거림", "두통"}


def show_pregnancy_warning(codes):
    """카드에 임산부 금기 혈자리가 있으면 경고를 표시합니다."""
    hits = []
    for code in codes:
        code = str(code).strip()
        if code in PREGNANCY_CAUTION_CODES:
            label = f"{PREGNANCY_CAUTION_CODES[code]}({code})"
            if label not in hits:
                hits.append(label)
    if hits:
        st.warning(f"🤰 **임산부 주의:** {', '.join(hits)}은(는) 자궁 수축 작용이 있어 임신 중에는 지압·뜸을 하지 마세요.")


def show_herb_cautions(herb_names):
    """약재 이름에 맞는 복용 주의사항과 공통 안내를 표시합니다."""
    messages = []
    for herb in herb_names:
        for keyword, msg in HERB_CAUTIONS.items():
            if keyword in str(herb):
                line = f"**{keyword}:** {msg}"
                if line not in messages:
                    messages.append(line)
    body = "\n".join(f"- {m}" for m in messages)
    if body:
        body += "\n"
    body += f"- {GENERAL_HERB_NOTE}"
    st.caption("⚠️ 복용 주의")
    st.markdown(body)


def show_red_flags(symptom):
    """증상별로 바로 병원에 가야 하는 신호를 표시합니다."""
    flags = RED_FLAGS.get(symptom, [])
    if not flags:
        return
    items = "\n".join(f"- {f}" for f in flags)
    if symptom in EMERGENCY_SYMPTOMS:
        st.error(f"🚑 **아래 증상이 있으면 지압보다 먼저 119에 연락하거나 응급실로 가세요.**\n\n{items}")
    else:
        st.warning(f"🏥 **아래 증상이 있으면 홈케어보다 먼저 병원 진료를 받으세요.**\n\n{items}")


def show_method(method_text):
    """지압법을 표시하고, 가정에서 하면 안 되는 사혈 안내가 섞여 있으면 경고합니다."""
    st.write(f"👉 **자가 지압법:** {method_text}")
    if "사혈" in str(method_text):
        st.warning("가정에서 침이나 바늘로 피를 내는 사혈은 감염 위험이 있으니 하지 마시고, 손가락 지압만 하세요.")


# ==============================================================================
# 기본 사상체질 데이터베이스 (평소 완실무병 & 약재 기본)
# ==============================================================================
CONSTITUTION_DATA = {
    "태음인": {
        "name_hanja": "太陰人",
        "description": "간의 기능은 성하고 폐의 기능은 약한 '간대폐소(肝大肺小)'의 장부 구조를 타고났습니다. 체구가 듬직하고 골격이 발달했으며, 성격이 묵묵하고 끈기 있게 목표를 완수하는 우직함이 장점입니다.",
        "daily_condition": "땀(汗)이 전신에 잘 나고 소통이 원활할 때 몸이 가장 개운하고 건강한 상태(완실무병)입니다.",
        "warning_signs": "피부가 야무지고 단단해지며 땀이 한 방울도 나지 않거나, 가슴이 심하게 쿵쾅거리며 불안해지는 정충증(怔忡症)이 생기면 순환이 막히고 있다는 신호입니다. 가슴 통증이나 호흡곤란이 함께 있으면 바로 병원에 가세요.",
        "personality": "생각이 깊고 안으로 겁심(겁내는 마음)이 많으며, 항상 안주하려 하고 묵묵하고 끈기 있게 완수하려는 고요한 성향을 지닙니다. 말솜씨와 행동에 위엄(威儀)이 있고 공명정대한 가치관을 지향합니다.",
        "talent": "무언가를 끝내 포기하지 않고 '성취'해내는 집념이 강하며, 한곳에 안정적으로 머무르며 책임지고 일(거처)을 정밀히 처리하는 능력이 뛰어납니다. 다만, 겁심이 깊어지면 정충증(불안증)이 생길 수 있으니 유의해야 합니다.",
        "acupoints_daily": [
            {"name": "태연 (太淵, LU9)", "position": "손목 안쪽 주름의 요골 쪽(엄지손가락 쪽) 맥박이 뛰는 부위", "method": "약해지기 쉬운 폐의 기운을 보강하기 위해, 손가락 끝으로 3초간 지긋이 누르기를 10회 반복합니다.", "image": "LU9.png"},
            {"name": "열결 (列缺, LU7)", "position": "양손의 엄지와 검지 사이를 엇갈려 잡았을 때, 집게손가락 끝이 닿는 손목 안쪽의 오목한 틈새", "method": "폐의 소통을 돕고 호흡기를 보호하는 자리입니다. 가볍게 원을 그리며 마사지하듯 눌러줍니다.", "image": "LU7.png"}
        ],
        "herbs": [
            {"name": "의이인 (薏苡仁, 율무)", "efficacy": "비위(위장)와 폐의 습한 기운을 없애고 노폐물 배출을 도와 체중 조절에 도움을 줄 수 있습니다.", "processing": "껍질을 벗긴 율무를 흐르는 물에 깨끗이 씻어 말린 뒤, 팬에 '약한 불로 노릇노릇해질 때까지 볶아서(초법, 炒法)' 사용하면 성질이 부드러워집니다."},
            {"name": "갈근 (葛根, 칡뿌리)", "efficacy": "간에 쌓인 열을 풀고 땀구멍을 열어주어 초기 감기 발열과 굳은 목덜미 근육을 푸는 데 도움을 줍니다.", "processing": "가을에 캔 칡뿌리를 깨끗이 씻어 겉껍질을 벗긴 후, 얇게 썰어 햇볕에 완전히 건조하여 사용합니다."}
        ],
        "tea_recipe": "볶은 율무 20g과 건조한 갈근 10g에 물 1L를 붓고 약한 불에 끓여 하루 2-3회 차처럼 나누어 드세요."
    },
    "소음인": {
        "name_hanja": "少陰人",
        "description": "신장의 기능은 성하고 비장의 기능은 약한 '신대비소(腎大脾小)'의 장부 구조를 지녔습니다. 성격이 차분하고 치밀하며 다정한 한편, 소화 기능이 예민하고 몸이 차가워지기 쉬워 따뜻한 보호가 필요합니다.",
        "daily_condition": "먹은 음식이 체하지 않고 소화(消化)가 부드럽게 잘 될 때 속이 가장 개운하고 건강한 상태(완실무병)입니다.",
        "warning_signs": "평소 한숨을 깊게 자주 쉬거나, 손발이 얼음처럼 차가워지며(수족냉증) 설사를 하고 땀을 흘린 뒤 기운이 쏙 빠지면 몸이 지쳐 있다는 신호입니다. 설사가 며칠씩 계속되거나 탈수 증상이 보이면 병원에 가세요.",
        "personality": "매사에 온화하고 단정하며 얌전하고 맵시가 있습니다. 붙임성이 좋고 친화력이 강해 타인을 부드럽게 위로하며 이끄는 능력이 돋보이나, 내성적이고 항상 안으로만 들어앉으려는 성향이 강해 소심해지기 쉽습니다.",
        "talent": "다재다능하여 잔재주가 많고, 팀이나 조직을 부드럽고 조화롭게 규합하여 기획·조직(당여)하는 재능이 뛰어납니다. 불안정하고 조바심을 내는 마음(불안정지심)을 비우면 비위(소화기) 기운이 살아납니다.",
        "acupoints_daily": [
            {"name": "삼음교 (三陰交, SP6)", "position": "안쪽 복사뼈 중심에서 위로 3치(본인 손가락 네 마디 너비) 올라간 정강이뼈 뒤쪽 가장자리", "method": "하복부를 따뜻하게 하고 소화기 기운을 북돋우는 양생혈입니다. 부드러운 온열 뜸을 뜨거나 가볍게 마사지합니다.", "image": "SP6.png"},
            {"name": "기해 (氣海, CV6)", "position": "배꼽 아래로 약 1.5치(본인의 검지와 중지 너비) 내려간 부위", "method": "원기의 바다라 불리는 곳으로 아랫배를 따뜻하게 해 줍니다. 평소 따뜻한 온팩을 올려 두면 소화에 도움이 됩니다.", "image": "CV6.png"}
        ],
        "herbs": [
            {"name": "인삼 (人參)", "efficacy": "비위의 약한 기운을 북돋우고 양기를 채워 손발을 따뜻하게 하고 소화를 돕습니다.", "processing": "수삼의 뇌두(머리 부분)를 잘라내고(구토를 유발할 수 있음), 얇게 썰어 말리거나 꿀에 재워 사용합니다."},
            {"name": "백출 (白朮, 삽주뿌리)", "efficacy": "위장을 튼튼하게 하고 뱃속의 차가운 습기를 없애 소화불량과 설사를 줄이는 데 도움을 줍니다.", "processing": "삽주 뿌리를 깨끗이 씻고 '쌀뜨물에 하루 동안 담가두어(미감침)' 기름기를 뺀 다음, 약한 불에 구워 건조하여 사용합니다."}
        ],
        "tea_recipe": "인삼 6g과 미감침 가공한 백출 6g에 대추 2알을 넣고 물 800ml에 은근히 우려내어 따뜻하게 복용합니다."
    },
    "소양인": {
        "name_hanja": "少陽人",
        "description": "비장의 기능은 성하고 신장의 기능은 약한 '비대신소(脾大腎小)'의 장부 구조를 지녔습니다. 행동이 민첩하고 굳세며 사안을 시원시원하게 해결하는 돌파력이 뛰어나지만, 위장에 열이 차올라 성격이 급해지기 쉽습니다.",
        "daily_condition": "대변(大便)이 막히지 않고 하루 한 번 시원하게 잘 통하는 것이 건강의 척도(완실무병)입니다.",
        "warning_signs": "대변이 3일 이상 통하지 않으면 가슴속이 답답하고 뜨거워지며, 머리가 지끈거리거나 예민해져 화가 자주 치미는 것이 건강 신호입니다. 심한 복통이나 혈변이 있으면 바로 병원에 가세요.",
        "personality": "성격이 날카롭고 용맹하며 행동이 강인하고 날랩니다. 항상 움직이려 하고 시원시원하게 매사를 돌파하는 적극성을 보이나, 때로는 말과 몸가짐이 다소 가볍거나 경솔해 보일 수 있습니다.",
        "talent": "공적인 업무나 복잡하게 꼬인 사무(事務)를 빠르고 막힘없이 해결하는 실무형 돌파력이 강합니다. 다만, 행동이 먼저 앞서 서두르면 가슴에 화(火)가 쌓여 소화기가 건조해지기 쉬우니 한 템포 쉬어가는 지혜가 필요합니다.",
        "acupoints_daily": [
            {"name": "음릉천 (陰陵泉, SP9)", "position": "종아리 안쪽 정강이뼈를 따라 위로 올라가다 무릎 관절 바로 아래 오목하게 걸리는 부위", "method": "몸 안의 열과 쓸데없는 수분을 빼주어 하체를 가볍게 돕습니다. 엄지손가락으로 꾹꾹 지압해 줍니다.", "image": "SP9.png"},
            {"name": "내관 (內關, PC6)", "position": "손목 안쪽 주름의 정중앙에서 팔 쪽으로 약 2치(손가락 세 마디 너비) 올라간 두 힘줄 사이", "method": "가슴으로 치솟는 화와 열 기운을 내리고 울화를 가라앉혀 줍니다. 편안하게 호흡하며 3분씩 부드럽게 지압합니다.", "image": "PC6.png"}
        ],
        "herbs": [
            {"name": "구기자 (枸杞子)", "efficacy": "약해지기 쉬운 신장의 음액을 보하고 눈을 맑게 하여 상체 열을 내리는 데 도움을 줍니다.", "processing": "붉은 구기자 열매를 '막걸리를 뿌려 시루에 한 번 찐 다음(주증, 酒蒸)' 다시 건조하여 사용합니다."},
            {"name": "산수유 (山茱萸)", "efficacy": "소양인의 약한 하체를 받쳐주고 기운을 안으로 모아줍니다.", "processing": "산수유 열매에서 '반드시 씨앗을 제거(去核)'하고 과육만 햇볕에 완전히 건조해 사용합니다."}
        ],
        "tea_recipe": "주증한 구기자 15g과 씨를 뺀 산수유 10g을 물 1.2L에 끓인 후 식혀서 물 대용으로 수시로 음용합니다."
    },
    "태양인": {
        "name_hanja": "太陽人",
        "description": "폐의 기능은 성하고 간의 기능은 약한 '폐대간소(肺大肝小)'의 장부 구조를 지녔습니다. 기세가 웅장하고 결단성이 뛰어나 대인 관계의 리더십이 탁월하지만, 기운이 위로 쏠려 하체 관절이 쉽게 약해질 수 있는 희귀 체질입니다.",
        "daily_condition": "소변(小便)이 넉넉하고 시원하게 잘 나올 때 체내 순환이 가장 원활한 건강한 상태(완실무병)입니다.",
        "warning_signs": "음식을 삼키기 어렵고 자꾸 입안에 맑은 침이나 거품이 차올라 뱉어내는 열격/반위(噎膈反胃) 증상은 몸의 균형이 깨졌다는 신호입니다. 삼키기 어렵거나 토하는 증상이 계속되면 식도 검사를 위해 반드시 병원에 가세요.",
        "personality": "거침없고 강직한 카리스마로 처음 보는 이들과도 막힘없이 사귑니다. 뒤로 물러서지 않고 과감하게 앞으로 전진하려는 강한 의지와 기상을 품어, 분위기를 주도하는 경향이 뚜렷합니다.",
        "talent": "넓은 사회적 관계망을 형성하고 주도하는 소통·교우(交遇) 능력이 독보적입니다. 다만, 지나치게 서두르는 급박지심(急迫之心)은 하반신 기운을 약하게 하거나 식도 경련(열격반위)을 일으킬 수 있으므로 유의해야 합니다.",
        "acupoints_daily": [
            {"name": "신수 (腎兪, BL23)", "position": "허리 부위, 둘째 허리뼈 가시돌기 아래에서 가쪽으로 1.5치(손가락 두 마디 너비) 부위", "method": "약한 하체의 힘을 보강해 줍니다. 양손을 비벼 따뜻하게 한 뒤 허리를 쓸어내립니다.", "image": "BL23.png"},
            {"name": "삼음교 (三陰交, SP6)", "position": "안쪽 복사뼈 중심에서 위로 3치 올라간 정강이뼈 뒷가장자리 안쪽", "method": "간과 신장의 음액을 자양하여 하체 힘을 기르는 데 도움을 줍니다.", "image": "SP6.png"}
        ],
        "herbs": [
            {"name": "오가피 (五加皮, 가시오갈피)", "efficacy": "약한 간의 기운과 근골을 도와 다리의 무력감을 줄이고 하체 힘을 기르는 데 도움을 줍니다.", "processing": "오가피 가지 껍질을 씻어 잘게 썬 뒤, 소금물에 가볍게 적셔 은근히 볶아내는 '염수초(鹽水炒)' 처리를 거쳐 사용합니다."},
            {"name": "모과 (木瓜)", "efficacy": "기의 흐름을 가라앉히고 식도 경련과 역류를 줄이며, 다리에 쥐가 나는 것을 푸는 데 도움을 줍니다.", "processing": "잘 익은 모과를 잘라 씨를 긁어낸 후, 얇게 썰어 증기에 한 번 찐 다음 햇볕에 바짝 건조해 사용합니다."}
        ],
        "tea_recipe": "염수초 가공한 오가피 12g과 말린 모과 8g에 물 1L를 부어 달인 뒤 물 대용으로 시원하게 마십니다."
    }
}

# ==============================================================================
# 체질별 운동 및 생활습관 데이터 (탭 3)
# ==============================================================================
LIFESTYLE_DATA = {
    "태음인": {
        "exercise_title": "땀을 흠뻑 흘리는 유산소 운동",
        "exercise_body": """
* **추천 종목**: 등산, 달리기, 수영, 자전거, 전신 유산소 운동, 온수욕.
* **이유**: 태음인은 '간대폐소(肝大肺小)'하여 기혈 소통이 안으로 쉽게 정체되고 노폐물이 쌓이기 쉬운 체질입니다. 땀을 개운하게 흘릴 때(완실무병) 순환과 호흡 기능이 좋아지고 체중 관리에도 도움이 됩니다.
* **주의**: 심혈관 질환이 있거나 오랜만에 운동을 시작한다면 강도를 천천히 올리세요.
""",
        "life_title": "겁심(怯心) 다스리기와 과식 절제",
        "life_body": """
* **핵심 수칙**: 심호흡·명상으로 긴장 풀기, 기름진 고기 과식 피하기.
* **이유**: 생각이 깊고 겁이 많은 성정(겁심)이 쌓이면 가슴이 쿵쾅거리는 '정충증(怔忡症)'이 올 수 있습니다. 대범하고 긍정적인 마음가짐이 도움이 됩니다. 식단에서는 볶은 율무차나 익힌 밤을 즐기고, 평소 과식을 경계하세요.
""",
    },
    "소음인": {
        "exercise_title": "땀이 많이 나지 않는 저·중강도 운동",
        "exercise_body": """
* **추천 종목**: 산책, 가벼운 요가, 필라테스, 맨몸 스트레칭, 무리하지 않는 걷기.
* **이유**: 소음인은 양기가 부족하고 체력이 약한 편이라 땀을 많이 흘리면 오히려 기운이 빠지고 쉽게 지칩니다. 체력을 보존하면서 관절과 혈류를 부드럽게 깨우는 운동이 좋습니다.
""",
        "life_title": "불안정지심(不安定之心) 완화와 소식·온식",
        "life_body": """
* **핵심 수칙**: 음식은 조금씩 따뜻하게 먹기, 배꼽 아래(기해혈)에 온팩 대기.
* **이유**: 소음인은 위장 기능이 약해 찬 음식이나 냉수에 급체·설사가 생기기 쉽습니다. 따뜻한 음식을 소량씩 잘 씹어 드세요. 조바심과 긴장(불안정지심)이 계속되면 신경성 위장 장애로 이어지기 쉬우니 마음을 편안하게 다독이는 것이 중요합니다.
""",
    },
    "소양인": {
        "exercise_title": "골반·다리 중심의 하체 근력 운동",
        "exercise_body": """
* **추천 종목**: 스쿼트, 런지, 계단 오르기, 실내 자전거, 보폭을 넓혀 차분히 걷기.
* **이유**: 소양인은 '비대신소(脾大腎小)'하여 상체에 비해 하반신이 약한 편입니다. 허리 통증이나 하체 관절 문제가 생기기 쉬우니 하체 근력을 꾸준히 기르는 것이 건강 유지에 좋습니다.
""",
        "life_title": "구심(懼心) 다스리기와 원활한 배변",
        "life_body": """
* **핵심 수칙**: 물과 채소·섬유질 충분히 섭취, 서두르거나 감정이 폭발하지 않도록 주의.
* **이유**: 소양인은 몸 안에 열(火)이 차기 쉬워 성질이 급하고, 대변이 하루만 막혀도 머리가 아프고 가슴이 답답해집니다. 인삼, 생강, 꿀처럼 더운 음식은 줄이고 보리차, 산수유차, 채소를 즐겨 대변을 시원하게 통하게 하세요. 두려움과 조급함이 뒤섞인 구심(懼心)을 차분히 식히는 여유가 도움이 됩니다.
""",
    },
    "태양인": {
        "exercise_title": "유연성과 코어 균형 위주 운동",
        "exercise_body": """
* **추천 종목**: 평지 걷기, 코어 균형 운동, 부드러운 전신 스트레칭.
* **이유**: 태양인은 '폐대간소(肺大肝小)'하여 위로 솟는 기운은 강하고 하체와 허리가 약한 편이라, 다리에 힘이 풀리는 해역증에 취약합니다. 관절에 무리를 주는 격렬한 운동보다 하체 정렬과 균형을 돕는 운동이 적합합니다.
""",
        "life_title": "급박지심(急迫之心)과 분노 다스리기",
        "life_body": """
* **핵심 수칙**: 담백한 메밀·모과차 섭취, 급하게 서두르는 마음과 솟구치는 분노 다스리기.
* **이유**: 태양인은 화가 치밀거나 슬픔이 쌓이면 기가 위로 솟아 식도가 좁아지고 거품 침을 토하는 '열격반위증(噎膈反胃症)'이 생기기 쉽습니다. 분노는 태양인 건강에 가장 해로운 요인이므로 평정심을 지키는 것이 중요합니다. 기름진 고기 대신 메밀국수나 조개류를 즐기고, 모과·오가피를 활용하며 소변이 원활하도록 살피세요.
""",
    },
}

# ==============================================================================
# 15문항 설문 정의
# - 보기 점수는 모두 1.0으로 통일하고, 문항의 중요도는 weight 하나로만 조절합니다.
# - '특별한 반응 없음' 성격의 보기는 0.5점으로 낮췄습니다.
# - 최종 점수는 체질별 '받을 수 있는 최대 점수' 대비 비율(%)로 계산해 체질 간 유불리를 없앴습니다.
# ==============================================================================
QUESTIONS = [
    {
        "id": 1,
        "category": "체형 및 외모 (실루엣)",
        "question": "거울을 보거나 남들이 내 신체 실루엣을 평가할 때, 가장 강하게 느껴지는 특징은 무엇인가요?",
        "options": [
            {"text": "목덜미 부근(목과 어깨 사이)의 기세는 우뚝 솟아 발달해 보이나, 상대적으로 허리와 하체가 빈약하고 외로워 보인다.", "scores": {"태양인": 1.0}},
            {"text": "가슴둘레(상체) 부위가 떡 벌어지고 실해 보이지만, 상대적으로 엉덩이와 골반 부위가 빈약하여 앉아 있는 자세가 다소 불안정해 보인다.", "scores": {"소양인": 1.0}},
            {"text": "허리둘레와 복부(요척)가 튼튼하게 발달하여 골격이 듬직하고 풍만하지만, 목덜미 기운은 상대적으로 얇고 가냘퍼 보인다.", "scores": {"태음인": 1.0}},
            {"text": "엉덩이와 골반(이둔) 부위가 잘 발달하여 앉아 있는 자세가 매우 안정적이고 아담하지만, 가슴둘레와 상체 기세가 가냘프고 좁아 보인다.", "scores": {"소음인": 1.0}}
        ],
        "weight": 1.0
    },
    {
        "id": 2,
        "category": "체형 및 외모 (피부와 근육)",
        "question": "피부를 만졌을 때 느껴지는 탄력이나 근육 및 살결의 단단함은 어떠한가요?",
        "options": [
            {"text": "살결이 대단히 부드럽고 밀도가 높은 편이며, 손가락으로 누르면 피부와 근육에 매우 조밀하고 야무진 단단함이 전해진다.", "scores": {"소음인": 1.0}},
            {"text": "체구가 풍만하고 살집이 넉넉하지만, 피부 표면은 비교적 야무지게 조여들지 않고 부드러운 스펀지 느낌에 가깝다.", "scores": {"태음인": 1.0}},
            {"text": "근육이 굳세고 살결이 다소 거친 감이 돌며, 걸음걸이가 대단히 민첩하고 상체 골격이 튼튼해 보인다.", "scores": {"소양인": 1.0}},
            {"text": "피부와 살집의 단단함보다는 뼈대(골반, 등뼈)가 매우 건실하고 마른 근육질 형태의 기세를 보인다.", "scores": {"태양인": 1.0}}
        ],
        "weight": 1.5
    },
    {
        "id": 3,
        "category": "체형 및 외모 (걸음걸이와 골격)",
        "question": "보행 시 느껴지는 자세의 무게감이나 하체의 보폭 특징은 무엇인가요?",
        "options": [
            {"text": "상체가 앞으로 쏠리듯 가벼운 발걸음으로 대단히 빠르게 걸으며, 엉덩이를 가볍게 흔드는 기세를 띤다.", "scores": {"소양인": 1.0}},
            {"text": "상체가 우뚝 서 있어 기백이 넘치지만 걸을 때 다리가 다소 휘청거리거나 힘이 쉽게 빠지는 느낌이 든다.", "scores": {"태양인": 1.0}},
            {"text": "가슴과 어깨를 활짝 펴고 걸음걸이가 매우 무겁고 점잖으며, 보폭이 일정하고 안정감이 뚜렷하다.", "scores": {"태음인": 1.0}},
            {"text": "자세가 소박하고 조심스러우며 보폭이 좁고 사뿐사뿐 걷는 단정함이 느껴진다.", "scores": {"소음인": 1.0}}
        ],
        "weight": 1.0
    },
    {
        "id": 4,
        "category": "체형 및 외모 (얼굴형과 이목구비)",
        "question": "거울을 보거나 남들이 내 인상을 말할 때, 가장 가까운 얼굴 분위기는 무엇인가요?",
        "options": [
            {"text": "이목구비가 크고 뚜렷하여 이지적이고 예리해 보이며, 턱선과 뺨 부위의 기세가 다소 굳세 보인다.", "scores": {"소양인": 1.0}},
            {"text": "눈과 코의 선이 둥글둥글하고 넓적하며 귀가 다소 크고 두툼해 전체적으로 무던하고 인자한 인상을 풍긴다.", "scores": {"태음인": 1.0}},
            {"text": "이목구비가 오밀조밀하게 단정하고 세밀하며 눈망울이 순하고 다정한 동양적인 느낌을 많이 준다.", "scores": {"소음인": 1.0}},
            {"text": "이마가 다소 넓고 눈빛이 매섭고 웅장하여 비타협적이고 강직한 카리스마가 인상 전체를 압도한다.", "scores": {"태양인": 1.0}}
        ],
        "weight": 1.0
    },
    {
        "id": 5,
        "category": "성격 및 기질 (추진력)",
        "question": "새로운 대규모 업무나 프로젝트를 시작할 때 나의 실행 성향은 어떠한가요?",
        "options": [
            {"text": "번뜩이는 아이디어로 일단 일을 쾌활하게 벌려 놓는 데 능하지만, 끝 마무리가 흐지부지되거나 지루해하기 쉽다.", "scores": {"소양인": 1.0}},
            {"text": "한 번 정한 목표는 거북이처럼 우직하게 밀어붙이며 끝까지 끈기 있게 완수하는 무던함을 발휘한다.", "scores": {"태음인": 1.0}},
            {"text": "일을 벌이기 전에 사소한 장애물까지 이중 삼중으로 세밀하게 검토하고 기획하며 완벽을 추구한다.", "scores": {"소음인": 1.0}},
            {"text": "남들의 반대나 관습을 단번에 돌파하는 웅장한 추진력과 기백을 발휘해 남의 위에 서기를 주도한다.", "scores": {"태양인": 1.0}}
        ],
        "weight": 1.5
    },
    {
        "id": 6,
        "category": "성격 및 기질 (사회성과 대인관계)",
        "question": "타인과 교류하거나 모임에 참석했을 때의 나의 자연스러운 대화 방식은 무엇인가요?",
        "options": [
            {"text": "사적인 이해관계를 세심히 조율하고 깊이 있는 화합을 추구하며 편을 부드럽게 가르는 내밀함이 있다.", "scores": {"소음인": 1.0}},
            {"text": "처음 만난 사람과도 금세 공적인 용무나 사안을 시원시원하게 논하며 막힘없이 대외적인 사무를 처리한다.", "scores": {"소양인": 1.0}},
            {"text": "말수가 다소 적고 상대의 의견을 묵묵히 들어주는 편이나, 속마음을 쉽게 내비치지 않고 무덤덤하게 행동한다.", "scores": {"태음인": 1.0}},
            {"text": "대인관계(교우)의 기세가 사방으로 널리 열려 있어 누구에게나 결단성 있고 과감하게 다가가는 편이다.", "scores": {"태양인": 1.0}}
        ],
        "weight": 1.0
    },
    {
        "id": 7,
        "category": "성격 및 기질 (스트레스 반응)",
        "question": "예상치 못한 위기나 압박 상황이 닥쳤을 때, 내면에서 가장 먼저 솟구치는 성질은 무엇인가요?",
        "options": [
            {"text": "일이 내 뜻대로 빠르게 풀리지 않으면 참지 못해 조급해지고, 화를 불같이 버럭 냈다가 금세 가라앉는다.", "scores": {"소양인": 1.0}},
            {"text": "마음 한구석에 무언가를 잃거나 지키지 못할까 봐 겁내고 조심하는 겁심(怯心)이 수시로 작동한다.", "scores": {"태음인": 1.0}},
            {"text": "상황이 통제되지 않으면 내면의 불안심(不安心)이 급격히 증가하며, 매사에 극도로 조심스럽고 위축된다.", "scores": {"소음인": 1.0}},
            {"text": "감정을 참지 못하면 분노(怒)를 극도로 크게 폭발시키고, 비타협적인 태도로 끝까지 맞서 싸우려 한다.", "scores": {"태양인": 1.0}}
        ],
        "weight": 1.0
    },
    {
        "id": 8,
        "category": "성격 및 기질 (의사결정 성향)",
        "question": "인생의 중대한 결단을 내리거나 가치관을 선택할 때, 내가 가장 중시하는 기준은 무엇인가요?",
        "options": [
            {"text": "가정과 내 팀의 안전을 최우선으로 확보하고, 그 자리에 안정적으로 거처(居處)하며 실리를 차근차근 쌓는 것.", "scores": {"태음인": 1.0}},
            {"text": "공적인 대의명분과 조화로운 공익을 위해 여러 사람과 동료 관계(당여)를 맺고 화합하는 것.", "scores": {"소음인": 1.0}},
            {"text": "대담한 이상을 바탕으로 세상의 흐름을 대외적으로 개척하고 주도해 큰 족적을 남기는 것.", "scores": {"태양인": 1.0}},
            {"text": "세상의 현안에 실시간으로 개입해 정체된 문제를 시원하고 빠르게 사무(事務)적으로 바로잡는 것.", "scores": {"소양인": 1.0}}
        ],
        "weight": 1.0
    },
    {
        "id": 9,
        "category": "생리 소증 (땀의 반응)",
        "question": "평소 격렬한 활동을 하거나 더운 날씨에 흘리는 나의 '땀(汗)'의 반응과 몸 상태는 어떠한가요?",
        "options": [
            {"text": "땀이 이마, 목덜미, 전신에 고르게 흠뻑 잘 흘러내려야만 온몸의 정체가 풀리고 날아갈 듯 가벼워진다.", "scores": {"태음인": 1.0}},
            {"text": "평소 땀이 거의 나지 않는 편이며, 사우나나 억지 운동으로 땀을 많이 흘리면 몸이 으스스 춥고 극도로 피로해진다.", "scores": {"소음인": 1.0}},
            {"text": "체온이 오르면 땀이 적당하게 고루 나며 피로감은 전혀 없고, 특히 이마나 손발 끝에 가볍게 잘 고인다.", "scores": {"소양인": 1.0}},
            {"text": "땀의 양 자체가 사계절 내내 지극히 적은 편이며, 땀의 유무보다는 소변 순환 상태에 기력이 좌우된다.", "scores": {"태양인": 1.0}}
        ],
        "weight": 1.5
    },
    {
        "id": 10,
        "category": "생리 소증 (소화와 식습관)",
        "question": "평소 나의 소화기 튼튼함 정도나 차가운 음식을 먹었을 때 비위의 반응은 어떠한가요?",
        "options": [
            {"text": "차가운 물이나 아이스크림을 조금만 많이 먹어도 바로 속이 아프고 설사 기운이 돌며 위장이 대단히 약하고 예민하다.", "scores": {"소음인": 1.0}},
            {"text": "소화력이 뛰어나 폭식이나 잡식을 해도 체하는 법이 거의 없으며 무엇이든 꿀맛같이 잘 먹는다.", "scores": {"태음인": 1.0}},
            {"text": "위장에 열이 강해 차갑고 시원한 음식을 선호하고, 기름진 것을 먹으면 가슴에 열이 차면서 가끔 답답해진다.", "scores": {"소양인": 1.0}},
            {"text": "식도가 예민한 편이어서 음식을 급하게 삼키거나 밀가루를 먹으면 명치 부근이 뻑뻑하게 걸려 내려가지 않는 느낌이 흔하다.", "scores": {"태양인": 1.0}}
        ],
        "weight": 1.5
    },
    {
        "id": 11,
        "category": "생리 소증 (대변 상태)",
        "question": "평소 나의 대변 습관이나 대변이 하루만 막혀도 몸에서 일어나는 반응은 어떠한가요?",
        "options": [
            {"text": "대변이 하루나 이틀만 통하지 않아도 아랫배가 더부룩해지면서 가슴이 불타듯 뜨거워지고 머리가 지끈거리며 예민해진다.", "scores": {"소양인": 1.0}},
            {"text": "대변이 평소 묽거나 무르게 자주 나오는 편이며, 몸에 병이 생기면 갑자기 설사로 쏟아져 기운이 쭉 빠진다.", "scores": {"소음인": 1.0}},
            {"text": "대변의 주기가 2~3일 정도로 다소 긴 편이고 단단하게 나오더라도, 가슴 답답함 없이 몸 상태는 늘 시원하고 무던하다.", "scores": {"태음인": 1.0}},
            {"text": "대변 상태는 보통이며 변비나 설사에 의해 전체 컨디션이 심각하게 변하지 않고 비교적 균형적이다.", "scores": {"태양인": 0.5}}
        ],
        "weight": 1.5
    },
    {
        "id": 12,
        "category": "생리 소증 (소변 순환)",
        "question": "평소 소변의 양이나 소변을 보고 난 직후 나의 신체적인 기력 변화는 어떠한가요?",
        "options": [
            {"text": "소변의 양이 매우 풍부하고 막힘없이 시원하게 나올 때 온몸이 개운하고 가벼워지며 기력이 상승한다.", "scores": {"태양인": 1.0}},
            {"text": "밤에 소변을 자주 보러 가거나 피로할 때 소변 횟수가 급증하는 편이며 하체에 약간의 무력감이 생긴다.", "scores": {"소양인": 1.0}},
            {"text": "보통 수준의 양과 횟수를 나타내며, 소변보다는 주로 땀이나 호흡 순환 상태에 더 많은 컨디션 영향을 받는다.", "scores": {"태음인": 0.5}},
            {"text": "소변에 큰 불편함이나 신체 반응 변화를 거의 느끼지 못하는 일반적인 양상을 보인다.", "scores": {"소음인": 0.5}}
        ],
        "weight": 1.5
    },
    {
        "id": 13,
        "category": "특이 병증 (급성 소화기 반응)",
        "question": "몸이 매우 지치거나 아플 때, 소화기 계통에서 유독 먼저 나타나는 증상은 무엇인가요?",
        "options": [
            {"text": "식도가 조여드는 듯 목구멍이 뻣뻣하게 느껴지거나, 음식을 삼켜도 신물이나 거품 섞인 맑은 침이 역류해 토하려 한다.", "scores": {"태양인": 1.0}},
            {"text": "체기가 있을 때 명치 아래가 꽉 막힌 듯 붓고 단단해지며 가슴속이 갑갑해 사소한 소리에도 극도로 민감하고 초조해진다.", "scores": {"소양인": 1.0}},
            {"text": "명치 끝은 편안하나 기가 체한 듯 가슴이 마구 두근거리며, 숨이 차고 눈두덩이나 얼굴 주위가 미세하게 파르르 떨린다.", "scores": {"태음인": 1.0}},
            {"text": "조금만 신경 쓰거나 지쳐도 명치밑에 단단하게 체기가 서며, 한숨을 깊게 몰아쉬어야 숨통이 트이고 명치 부위가 더부룩해진다.", "scores": {"소음인": 1.0}}
        ],
        "weight": 1.5
    },
    {
        "id": 14,
        "category": "특이 병증 (두근거림과 불안)",
        "question": "가슴이 두근거리거나 불안해질 때, 나에게 나타나는 특징은 무엇인가요?",
        "options": [
            {"text": "화가 치밀면 가슴이 벌렁거리며 기운이 머리 위로 확 솟구치고, 목과 가슴이 답답하게 조여드는 느낌이 든다.", "scores": {"태양인": 1.0}},
            {"text": "일이 급해지면 가슴이 뜨겁게 달아오르며 두근거리고, 가만히 있지 못하고 안절부절 움직이거나 말을 쏟아낸다.", "scores": {"소양인": 1.0}},
            {"text": "이유 없이 가슴이 혼자 쿵쾅쿵쾅 뛰며 마음을 제어하기 어려운 불안(정충증, 怔忡症)이 찾아온다.", "scores": {"태음인": 1.0}},
            {"text": "가슴이 철렁 내려앉는 듯한 가벼운 두근거림과 함께 손발 끝이 급격히 차가워지고 이마에서 식은땀이 흐른다.", "scores": {"소음인": 1.0}}
        ],
        "weight": 1.5
    },
    {
        "id": 15,
        "category": "냉열 감각 (추위와 더위 타는 특징)",
        "question": "손발 및 체온의 균형 분포 상태나 평소 추위와 더위를 대하는 나의 신체적 감각은 어떠한가요?",
        "options": [
            {"text": "추위와 더위를 평범하게 타는 편이나, 유독 다리 관절이나 척추가 힘없이 싸늘해지고 다리가 주저앉을 것처럼 허약해질 때가 있다.", "scores": {"태양인": 1.0}},
            {"text": "상체(얼굴, 머리, 가슴)는 늘 화끈화끈 뜨겁게 열감이 쏠려 시원한 환경을 좋아하지만, 반대로 아랫배나 다리는 유난히 차갑고 시리다.", "scores": {"소양인": 1.0}},
            {"text": "피부와 살집이 두꺼워 겨울철 추위는 옷을 잘 입으면 든든히 버티지만, 몸 안의 열이 있어 여름철 더위는 못 참고 땀을 심하게 흘린다.", "scores": {"태음인": 1.0}},
            {"text": "겨울철에 남들보다 손발이 얼음장처럼 차갑게 식어 장갑이 필수이며(수족냉증), 에어컨 바람을 조금만 쐬어도 몸이 으스스 조여들며 추위를 많이 탄다.", "scores": {"소음인": 1.0}}
        ],
        "weight": 1.5
    }
]

# 1위와 2위 점수 차가 이 값(%p)보다 작으면 '경계형'으로 안내합니다.
BORDERLINE_GAP = 5.0


def calculate_scores(answers):
    """선택한 답으로 체질별 점수를 '최대 가능 점수 대비 %'로 계산합니다."""
    raw = {c: 0.0 for c in CONSTITUTIONS}
    max_possible = {c: 0.0 for c in CONSTITUTIONS}
    for q in QUESTIONS:
        w = q["weight"]
        for opt in q["options"]:
            for const, val in opt["scores"].items():
                max_possible[const] += val * w
        for const, val in answers[q["id"]]["scores"].items():
            raw[const] += val * w
    return {c: (raw[c] / max_possible[c] * 100 if max_possible[c] else 0.0) for c in CONSTITUTIONS}


def reset_diagnosis():
    st.session_state.diagnosis_completed = False
    st.session_state.constitution_result = None
    st.session_state.score_pct = None
    st.session_state.result_source = None
    st.session_state.show_questions = False
    for q in QUESTIONS:
        st.session_state.pop(f"q_{q['id']}", None)


# ==============================================================================
# Streamlit 웹 어플리케이션 환경 로드 및 레이아웃 정의
# ==============================================================================
st.set_page_config(
    page_title="사상의학 증상별 큐레이션 및 자가 홈케어 앱",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
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
""", unsafe_allow_html=True)


# ----------------- CSV 데이터 로드 -----------------
@st.cache_data
def load_symptom_db():
    csv_filename = "sasang_symptom_db.csv"
    for path in [csv_filename, os.path.join("/workspace/artifacts", csv_filename)]:
        if os.path.exists(path):
            # utf-8-sig: 파일 맨 앞의 보이지 않는 문자(BOM)를 자동으로 제거합니다.
            df = pd.read_csv(path, encoding="utf-8-sig")
            df.columns = [c.strip() for c in df.columns]
            return df
    return None


symptom_df = load_symptom_db()

# ----------------- 사이드바 설정 -----------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/194/194203.png", width=80)
    st.header("🌿 사상체질 5대 증상 홈케어")
    st.write("본 서비스는 이제마 선생의 **『동의수세보원』** 원전과 한방 침구학 자료를 참고해 만든 홈케어 참고용 앱입니다.")
    st.divider()

    st.markdown("### ⚠️ 자가 지압 안전 주의사항")
    st.warning("""
    1. **식후 지압 금지**: 식후 1시간 이내에는 강한 압박을 피합니다.
    2. **🤰 임산부 금기 혈자리**: **삼음교(SP6)**와 **합곡(LI4)**은 자궁 수축 작용이 있어 임신 중에는 지압·뜸을 하지 않습니다.
    3. **강도 조절**: 멍이 들 정도로 누르지 말고, 3~5초간 살짝 뻐근한 느낌(득기감) 정도로 누릅니다.
    4. **사혈 금지**: 가정에서 침이나 바늘로 피를 내지 마세요.
    """)
    st.divider()
    st.info("💡 이 앱의 설문과 정보는 참고용입니다. 정확한 체질 판별과 치료는 한의사 진료를 받으세요.")

# ----------------- 헤더 타이틀 -----------------
st.markdown('<div class="main-title">🌿 사상체질 맞춤형 5대 증상 큐레이션 시스템</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">체질 설문을 마친 뒤, 지금 가장 불편한 증상(소화불량, 두통, 요통 등)을 골라 체질별 홈케어 방법을 확인해 보세요.</div>', unsafe_allow_html=True)

# Session state initialization
for key, default in [
    ("diagnosis_completed", False),
    ("constitution_result", None),
    ("score_pct", None),
    ("result_source", None),
    ("show_questions", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ----------------- VIEW 1: DIAGNOSIS FORM -----------------
if not st.session_state.diagnosis_completed:
    st.subheader("🌿 사상의학 자가 건강 설문 시작")
    st.write("""
    본 자가 설문은 동무 이제마 선생의 『동의수세보원』에 기록된 진단 지표들을 참고해 구성했습니다.
    총 **15개의 문항**으로 체형, 성격, 평소의 생리 상태, 아플 때 나타나는 특징을 종합해 봅니다.

    결과에 따라 평소 원기를 보하는 **양생 지압과 약차 조제법**, 그리고
    불편한 증상이 있을 때 참고할 수 있는 **5대 증상별 홈케어 카드**를 제공합니다.
    """)
    st.divider()

    st.info("💡 **설문 안내**: 본인의 평소 컨디션과 외형, 기질에 가장 가까운 답을 골라주세요. 모든 문항에 답해야 결과를 볼 수 있습니다.")
    st.write("")

    col_diag, col_direct = st.columns(2)

    with col_diag:
        st.markdown("### 📋 15문항 체질 설문 코스")
        st.write("체형, 성격, 평소 생리 상태를 종합해 가장 가까운 사상체질을 알아보고 싶다면 선택하세요.")
        st.write("")
        st.write("")
        if not st.session_state.show_questions:
            if st.button("🔮 체질 자가 설문 시작하기", type="primary", use_container_width=True):
                st.session_state.show_questions = True
                st.rerun()

    with col_direct:
        st.markdown("### ⚡ 이미 본인의 체질을 아시나요?")
        st.write("한의원에서 체질을 진단받으셨다면, 설문을 건너뛰고 바로 체질별 홈케어를 확인해 보세요.")
        direct_selection = st.selectbox(
            "본인의 체질을 직접 골라주세요:",
            CONSTITUTIONS,
            key="direct_selection_key"
        )
        if st.button("🎯 맞춤 홈케어 바로 보러 가기", use_container_width=True):
            st.session_state.constitution_result = direct_selection
            st.session_state.result_source = "direct"
            st.session_state.score_pct = None
            st.session_state.diagnosis_completed = True
            st.rerun()

    if st.session_state.show_questions:
        st.divider()
        st.subheader("📋 15문항 체질 판별 설문")
        user_answers = {}
        for q in QUESTIONS:
            st.markdown(f"**Q{q['id']}. [{q['category']}] {q['question']}**")
            options_texts = [opt["text"] for opt in q["options"]]

            # index=None: 아무것도 선택되지 않은 상태로 시작합니다.
            choice = st.radio(
                label=f"q_{q['id']}_label",
                options=options_texts,
                index=None,
                key=f"q_{q['id']}",
                label_visibility="collapsed"
            )
            if choice is not None:
                user_answers[q["id"]] = next(opt for opt in q["options"] if opt["text"] == choice)
            st.write("")

        st.divider()
        answered = len(user_answers)
        st.progress(answered / len(QUESTIONS), text=f"응답 진행: {answered} / {len(QUESTIONS)}문항")

        if st.button("🔮 나의 사상체질 결과 확인하기", type="primary", use_container_width=True):
            unanswered = [q["id"] for q in QUESTIONS if q["id"] not in user_answers]
            if unanswered:
                st.error("아직 답하지 않은 문항이 있습니다: " + ", ".join(f"Q{i}" for i in unanswered))
            else:
                score_pct = calculate_scores(user_answers)
                winner = max(score_pct, key=score_pct.get)
                st.session_state.score_pct = score_pct
                st.session_state.constitution_result = winner
                st.session_state.result_source = "survey"
                st.session_state.diagnosis_completed = True
                st.session_state.show_questions = False
                st.rerun()

# ----------------- VIEW 2: RESULTS & SYMPTOM CURATION -----------------
else:
    diagnosed_const = st.session_state.constitution_result or CONSTITUTIONS[0]
    default_idx = CONSTITUTIONS.index(diagnosed_const) if diagnosed_const in CONSTITUTIONS else 0

    final_constitution = st.selectbox(
        "🔍 [체질 변경] 다른 사상체질의 건강 가이드도 구경해 보세요!",
        options=CONSTITUTIONS,
        index=default_idx
    )

    const_data = CONSTITUTION_DATA[final_constitution]
    is_browsing_other = final_constitution != diagnosed_const

    if is_browsing_other:
        st.info(f"💡 실제 결과인 **{diagnosed_const}** 대신, 선택하신 **{final_constitution}**의 건강 가이드를 보고 계십니다.")

    if st.button("⬅️ 처음부터 다시 설문하기", type="secondary"):
        reset_diagnosis()
        st.rerun()

    st.divider()

    # 결과 배너: 설문 결과 / 직접 선택 / 다른 체질 구경 상황에 맞게 문구를 바꿉니다.
    if is_browsing_other:
        banner_title = f"선택하신 <b>{final_constitution} ({const_data['name_hanja']})</b>의 건강 가이드입니다"
    elif st.session_state.result_source == "survey":
        banner_title = f"자가 설문 결과, 가장 가까운 체질은 <b>{final_constitution} ({const_data['name_hanja']})</b>입니다"
    else:
        banner_title = f"선택하신 체질은 <b>{final_constitution} ({const_data['name_hanja']})</b>입니다"

    st.markdown(f"""
    <div class="result-header">
        <h2 style='margin:0; color:#1B5E20;'>{banner_title}</h2>
        <p style='margin-top:10px; font-size:1.15rem; color:#333; line-height:1.6;'>{const_data['description']}</p>
    </div>
    """, unsafe_allow_html=True)

    # 설문 점수와 판별 신뢰도
    score_pct = st.session_state.score_pct
    if score_pct and st.session_state.result_source == "survey":
        ranked = sorted(score_pct.items(), key=lambda x: x[1], reverse=True)
        (top1, p1), (top2, p2) = ranked[0], ranked[1]
        gap = p1 - p2

        if gap == 0:
            st.warning(f"⚖️ **{top1}**와(과) **{top2}**의 점수가 같습니다. 설문만으로는 구분이 어려우니 두 체질의 가이드를 모두 살펴보고, 한의사 진료로 확인해 보세요.")
        elif gap < BORDERLINE_GAP:
            st.warning(f"⚖️ **{top1}** 경향이 가장 높지만 **{top2}**와(과) 차이가 {gap:.1f}%p로 작습니다. 두 체질의 특징이 함께 보이는 경계형일 수 있습니다.")

        with st.expander("📊 체질별 설문 점수 자세히 보기", expanded=gap < BORDERLINE_GAP):
            for const, pct in ranked:
                st.progress(min(pct / 100, 1.0), text=f"{const}: {pct:.1f}%")
            st.caption("각 체질이 받을 수 있는 최대 점수 대비 비율입니다. 설문은 참고용이며, 정확한 체질 판별은 한의사 진료가 필요합니다.")
    elif st.session_state.result_source == "survey":
        st.caption("설문 결과는 참고용이며, 정확한 체질 판별은 한의사 진료가 필요합니다.")

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
            <h4 style="margin:0; color:#C62828;">🔴 몸의 균형이 깨졌다는 신호</h4>
            <p style="margin-top:8px; font-size:0.95rem; color:#444;">{const_data['warning_signs']}</p>
        </div>
        """, unsafe_allow_html=True)

    col_char1, col_char2 = st.columns(2)
    with col_char1:
        st.markdown(f"""
        <div class="info-box" style="border-left-color: #7E57C2; background-color: #F3E5F5;">
            <h4 style="margin:0; color:#5E35B1;">🧠 타고난 성격 및 기질적 특성</h4>
            <p style="margin-top:8px; font-size:0.95rem; color:#444;">{const_data['personality']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_char2:
        st.markdown(f"""
        <div class="info-box" style="border-left-color: #FBC02D; background-color: #FFFDE7;">
            <h4 style="margin:0; color:#F57F17;">✨ 재간(장점) 및 보완점</h4>
            <p style="margin-top:8px; font-size:0.95rem; color:#444;">{const_data['talent']}</p>
        </div>
        """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🌿 1. 평소 건강 관리 및 기본 양생", "🚨 2. 5대 주요 증상별 한방 홈케어", "🏃 3. 체질별 운동 및 생활습관"])

    # [TAB 1] 평소 건강 관리
    with tab1:
        st.markdown(f"### 🍵 {final_constitution}의 평소 양생 가이드")
        st.write("체질적으로 부족한 기운을 부드럽게 채워주는 평소 양생 수칙과 약재 조제법입니다.")
        st.divider()

        st.markdown("#### ① 매일 가볍게 실천하는 2대 양생혈 지압")
        daily_codes = [pt["image"].replace(".png", "") for pt in const_data["acupoints_daily"]]
        show_pregnancy_warning(daily_codes)

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

        st.markdown("#### ② 체질별 기본 맞춤 한방 약재")
        for hb in const_data["herbs"]:
            with st.expander(f"⭐ {hb['name']} (자세히 보기)"):
                st.markdown(f"**효능:** {hb['efficacy']}")
                st.markdown(f"**👑 가공(법제) 요령:** <span class='accent-text'>{hb['processing']}</span>", unsafe_allow_html=True)
        st.divider()
        st.markdown("#### ③ 일상생활 추천 약차(藥茶) 레시피")
        st.success(f"🍵 **약차 조제법:** {const_data['tea_recipe']}")
        show_herb_cautions([hb["name"] for hb in const_data["herbs"]])

    # [TAB 2] 5대 주요 증상별 홈케어 (CSV 연동)
    with tab2:
        st.markdown("### 🏥 지금 겪고 있는 불편한 증상별 체질 맞춤 홈케어")
        st.write("불편한 증상을 하나 선택해 주세요. 해당 체질에 맞춘 지압과 약차 정보를 보여드립니다.")

        selected_symptom = st.selectbox(
            "👉 증상을 선택하세요",
            ["소화불량", "두통", "변비", "두근거림", "요통"],
            index=0
        )

        # 병원 방문 신호를 맨 위에 먼저 보여줍니다.
        show_red_flags(selected_symptom)

        if symptom_df is not None:
            filtered = symptom_df[(symptom_df["symptom"] == selected_symptom) & (symptom_df["constitution"] == final_constitution)]

            if not filtered.empty:
                row = filtered.iloc[0]

                st.markdown(f"""
                <div class="symptom-card">
                    <h3 style="margin:0; color:#33691E;">⚡ {final_constitution}의 '{selected_symptom}' 한의학적 해석과 홈케어</h3>
                    <p style="margin-top:10px; font-size:1.05rem; line-height:1.6; color:#444;">
                        <b>[한의학적 원인]:</b> {row['cause']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                st.write("")

                st.markdown(f"#### 📍 {selected_symptom}에 도움이 되는 2대 지압 자리")
                show_pregnancy_warning([row["acupoint1_code"], row["acupoint2_code"]])

                col_pt1, col_pt2 = st.columns(2)
                for col, n in [(col_pt1, 1), (col_pt2, 2)]:
                    with col:
                        name = row[f"acupoint{n}_name"]
                        code = row[f"acupoint{n}_code"]
                        image = row[f"acupoint{n}_image"]
                        st.markdown(f"##### {n}️⃣ {name} ({code})")
                        img_url = get_gdrive_image_url(image)
                        if img_url:
                            st.image(img_url, caption=f"{name} 경혈 지도", use_container_width=True)
                        else:
                            st.image("https://cdn-icons-png.flaticon.com/512/2855/2855146.png",
                                     caption=f"연동 대기: {image}", width=120)
                        st.write(f"📌 **해부학적 위치:** {row[f'acupoint{n}_position']}")
                        show_method(row[f"acupoint{n}_method"])

                st.divider()

                st.markdown(f"#### 🍯 {selected_symptom} 완화를 위한 체질 맞춤 약차")
                col_hb, col_tea = st.columns([2, 3])
                with col_hb:
                    st.info(f"🌿 **추천 약재:** **{row['herb_name']}**")
                    st.write(f"**효능:** {row['herb_efficacy']}")
                    st.write("**👑 가공(법제)법:**")
                    st.markdown(f"<span class='accent-text'>{row['herb_processing']}</span>", unsafe_allow_html=True)
                with col_tea:
                    st.success("🍵 **가정용 약차 조제법:**")
                    st.write(row["tea_recipe"])
                    show_herb_cautions([row["herb_name"], row["tea_recipe"]])
            else:
                st.error("해당 체질 및 증상에 맞는 데이터가 없습니다.")
        else:
            st.error("⚠️ `sasang_symptom_db.csv` 파일을 찾을 수 없어 증상별 홈케어를 불러오지 못했습니다. 깃허브 저장소에 파일을 함께 업로드해 주세요!")

    # [TAB 3] 체질별 운동 및 생활습관
    with tab3:
        life = LIFESTYLE_DATA[final_constitution]
        st.markdown(f"### 🏃 {final_constitution} 체질을 위한 운동 및 생활 수칙")
        st.write("사상의학 원전을 참고해 체질의 균형을 돕는 일상 수칙을 정리했습니다.")
        st.divider()

        col_ex, col_life = st.columns(2)
        with col_ex:
            st.markdown(f"#### 🏃 추천 운동: **{life['exercise_title']}**")
            st.info(life["exercise_body"])
        with col_life:
            st.markdown(f"#### 🧘 마음과 식습관: **{life['life_title']}**")
            st.success(life["life_body"])
