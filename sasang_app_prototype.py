# -*- coding: utf-8 -*-
import streamlit as st
import os
import sys

# ==========================================
# 🌿 [중요] 구글 드라이브 경혈 이미지 파일 ID 매핑
# ==========================================
# 질문자님의 구글 드라이브 '경혈맵' 폴더에 이미지(LU9.png, LR3.png 등)를 업로드하신 후,
# 각 파일의 공유 링크에서 고유 ID 부분을 추출하여 아래 따옴표 안에 붙여넣어 주세요!
# (공유 설정은 반드시 "링크가 있는 모든 사용자 - 뷰어"로 해두셔야 연동됩니다.)
# 예: https://drive.google.com/file/d/1aBcDeFgHiJ... 에서 '1aBcDeFgHiJ...' 가 고유 ID입니다.
# 빈 칸으로 두면 앱 자체 내장 플레이스홀더 아이콘이 기본 표시됩니다.
GDRIVE_FILE_IDS = {
    "LU9.png": "",    # 태연 (태음인 평소)
    "LU7.png": "",    # 열결 (태음인 평소)
    "LR3.png": "",    # 태충 (태음인 치료)
    "LR2.png": "",    # 행간 (태음인 치료)
    "SP6.png": "",    # 삼음교 (소음인/태양인 평소)
    "CV6.png": "",    # 기해 (소음인 평소)
    "LI4.png": "",    # 합곡 (소음인/태양인 치료)
    "LU11.png": "",   # 소상 (소음인/태양인 치료)
    "SP9.png": "",    # 음릉천 (소양인 평소)
    "PC6.png": "",    # 내관 (소양인 평소)
    "ST36.png": "",   # 족삼리 (소양인 치료)
    "TE6.png": "",    # 지구 (소양인 치료)
    "BL23.png": ""    # 신수 (태양인 평소)
}

def get_gdrive_image_url(image_filename):
    """구글 드라이브 고유 파일 ID를 활용해 직접 스트리밍 링크(Direct Link)를 생성합니다."""
    file_id = GDRIVE_FILE_IDS.get(image_filename, "")
    if file_id and file_id.strip():
        return f"https://lh3.googleusercontent.com/d/{file_id.strip()}"
    return None

CONSTITUTION_DATA = {
    '소양인': {
        'acupoints_acute': [
            {
                'method': '급성 소화불량이나 상체의 열을 전신으로 고르게 분산시키는 요혈입니다. 지압봉 등을 사용해 묵직한 자극을 줍니다.',
                'name': '족삼리 (足三里, ST36)', 
                'image': 'ST36.png',
                'position': '독비혈(무릎 바깥쪽 오목한 곳)에서 아래로 3치 내려간 곳, 정강이뼈 가쪽 한 손가락 너비'
            },
            {
                'method': '소양인의 대변 불통 및 변비 증상이 올 때 온몸의 삼초 기운을 소통시켜 변을 시원하게 보게 돕는 특효혈입니다. 손가락으로 강하게 흔들며 압박합니다.',
                'name': '지구 (支溝, TE6)', 
                'image': 'TE6.png',
                'position': '손등 손목 주름에서 위로 3치 올라간 두 뼈 사이의 오목한 곳'
            }
        ],
        'acupoints_daily': [
            {
                'method': '몸 안의 비생리적인 열 독소와 수분을 소통시켜 비뇨기와 위장을 돕습니다. 엄지손가락으로 꾹꾹 눌러 지압해 줍니다.',
                'name': '음릉천 (陰陵泉, SP9)', 
                'image': 'SP9.png',
                'position': '종아리 안쪽 정강이뼈를 따라 위로 올라가다 무릎 관절 바로 아래 오목하게 걸리는 부위'
            },
            {
                'method': '상체로 치솟는 기운을 아래로 내리고 마음을 편안하게 조율합니다. 가슴이 답답하거나 울화가 치밀 때 3분씩 부드럽게 지압합니다.',
                'name': '내관 (內關, PC6)', 
                'image': 'PC6.png',
                'position': '손목 안쪽 주름의 정중앙에서 팔 쪽으로 약 2치(손가락 세 마디 너비) 올라간 두 힘줄 사이'
            }
        ],
        'daily_condition': '대변(大便)이 막히지 않고 하루 한 번 막힘없이 시원하게 잘 통하는 것이 건강의 척도(완실무병)입니다.',
        'description': "비장의 기능은 성하고 신장의 기능은 약한 '비대신소(脾大腎小)'의 장부 구조를 지녔습니다. 매사에 날래고 용맹하며, 공적인 업무를 시원스럽게 돌파하는 추진력이 강합니다.",
        'herbs': [
            {
                'efficacy': '약해지기 쉬운 신장의 기운을 보하고, 체내의 음액(수분)을 채워주어 눈을 밝게 하고 피로를 풉니다.',
                'name': '구기자 (枸杞子)',
                'processing': "가을에 붉게 익은 구기자 열매를 따서 깨끗이 씻은 후, 통풍이 잘되는 그늘에서 반쯤 말렸다가 '막걸리를 살짝 뿌려 시루에 한 번 찐 다음(주증, 酒蒸)' 다시 햇볕에 완벽하게 건조해 사용합니다. 이렇게 하면 신장을 보하는 약성이 훨씬 깊어집니다."
            },
            {
                'efficacy': '정력을 보강하고 오줌이 잦은 증상을 치료하며, 소양인의 하체를 든든하게 받쳐줍니다.',
                'name': '산수유 (山茱萸)',
                'processing': "붉은 산수유 열매에서 '반드시 씨앗을 제거(去核)'해야 합니다. 산수유 씨앗은 정력을 오히려 상하게 하므로 과육만 발라내어 건조한 뒤 사용해야 합니다."
            }
        ],
        'name_hanja': '少陽人',
        'tea_recipe': '주증 가공한 구기자 15g과 씨를 뺀 산수유 10g을 물 1.2L에 넣고 끓여 식힌 뒤, 시원하게 음용하면 상체 열을 내리는 데 탁월합니다.',
        'warning_signs': '대변이 3일 이상 통하지 않으면 가슴속이 불같이 뜨거워지고 머리가 깨질 듯 아프며, 사소한 일에도 가슴이 심하게 답답하고 열이 오릅니다.'
    },
    '소음인': {
        'acupoints_acute': [
            {
                'method': '급체하거나 머리가 아플 때 족삼리와 함께 사용하여 막힌 기를 강하게 뚫어줍니다. 찌릿한 느낌이 손끝까지 가도록 강하게 5초씩 지압합니다.',
                'name': '합곡 (合谷, LI4)', 
                'image': 'LI4.png',
                'position': '엄지와 검지 손가락 뼈가 만나는 부위의 바로 앞 오목한 곳'
            },
            {
                'method': '급성 위장 장애나 고열로 정신이 혼미할 때, 소독된 침으로 한 방울 피를 내는 사혈 요법(사법)으로 구급 치료에 요긴하게 쓰입니다.',
                'name': '소상 (少商, LU11)', 
                'image': 'LU11.png',
                'position': '엄지손가락 손톱 안쪽 모서리에서 옆으로 약 0.1치(약 1mm) 떨어진 지점'
            }
        ],
        'acupoints_daily': [
            {
                'method': '하복부를 따뜻하게 하고 소화기 기운을 북돋우는 핵심 양생혈입니다. 부드러운 뜸(온구법)을 뜨거나 둥글게 원을 그리며 따뜻한 온기가 돌 때까지 마사지합니다.',
                'name': '삼음교 (三陰交, SP6)', 
                'image': 'SP6.png',
                'position': '안쪽 복사뼈 중심에서 위로 3치(본인 손가락 네 마디 너비) 올라간 뼈 뒷가장자리'
            },
            {
                'method': '원기의 바다라 불리는 곳으로 몸의 하초를 따뜻하게 덥혀줍니다. 평소 따뜻한 핫팩이나 뜸 요법을 적용하면 소화력이 몰라보게 좋아집니다.',
                'name': '기해 (氣海, CV6)', 
                'image': 'CV6.png',
                'position': '배꼽 아래로 약 1.5치(본인 검지와 중지 너비) 내려간 부위'
            }
        ],
        'daily_condition': '먹은 음식이 체하지 않고 소화(消化)가 부드럽게 잘 될 때 속이 편안하고 건강한 상태(완실무병)입니다.',
        'description': "신장의 기능은 성하고 비장의 기능은 약한 '신대비소(腎大脾小)'의 장부 구조를 지녔습니다. 성격이 침착하고 꼼꼼하며, 예의가 바르고 다른 이들을 다독이는 일에 뛰어납니다.",
        'herbs': [
            {
                'efficacy': '비위의 약한 기운을 북돋우고 양기를 채워주어 손발을 따뜻하게 하고 소화력을 대폭 끌어올립니다.',
                'name': '인삼 (人參)',
                'processing': "수삼을 깨끗이 씻어 뇌두(머리 부분)를 잘라낸 뒤(뇌두는 구토를 유발할 수 있어 반드시 제거), '얇게 썰어 말리거나', '꿀에 재워 재증(쪄서 말림)'하여 약성을 순하게 만든 뒤 사용합니다."
            },
            {
                'efficacy': '위장을 튼튼하게 하고 뱃속의 차가운 물기를 없애주어 소화불량과 설사를 멈추게 합니다.',
                'name': '백출 (白朮, 삽주뿌리)',
                'processing': "삽주 뿌리를 깨끗이 씻고 겉면의 흙을 제거한 뒤, '쌀뜨물에 하루 동안 담가두어(미감침, 米泔浸)' 기름기를 뺀 다음, 약한 불에 구워 건조하여 사용합니다."
            }
        ],
        'name_hanja': '少陰人',
        'tea_recipe': '인삼 6g과 쌀뜨물 처리한 백출 6g에 대추 2알을 넣고 물 800ml에 달여 따뜻하게 나누어 마십니다.',
        'warning_signs': '평소 한숨을 깊게 자주 쉬거나, 손발이 얼음처럼 차가워지며(수족냉증) 설사를 하고, 식은땀을 흘리면 원기가 손상되었다는 위험한 신호입니다.'
    },
    '태양인': {
        'acupoints_acute': [
            {
                'method': '음식물이 역류하거나 상체에 가래가 끓고 기가 거꾸로 솟구칠 때 지압을 통해 기운을 전신으로 빠르게 하향 소통시켜 줍니다.',
                'name': '합곡 (合谷, LI4)', 
                'image': 'LI4.png',
                'position': '엄지와 검지 사이의 호구 부위 오목한 곳'
            },
            {
                'method': '폐 기운이 과도하게 솟구쳐 숨이 차거나 목구멍이 심하게 붓고 아플 때 가벼운 사혈이나 강한 지압을 통해 급성 압력을 즉각 낮춰줍니다.',
                'name': '소상 (少商, LU11)', 
                'image': 'LU11.png',
                'position': '엄지손가락 손톱 안쪽 모서리 가쪽으로 1mm 지점'
            }
        ],
        'acupoints_daily': [
            {
                'method': '약하기 쉬운 하체와 신장/간 기운을 뒤에서 든든히 받쳐줍니다. 양손을 비벼 따뜻하게 한 뒤 허리 뒤를 쓸어내리거나 지긋이 눌러줍니다.',
                'name': '신수 (腎兪, BL23)', 
                'image': 'BL23.png',
                'position': '허리 부위, 둘째 허리뼈 가시돌기 아래에서 가쪽으로 1.5치(손가락 두 마디 너비) 부위'
            },
            {
                'method': '간과 신장의 음기를 함께 보충하는 자리로, 태양인의 빈약한 하체 기운을 강화하는 데 매일 지압해 주면 훌륭한 효과를 발휘합니다.',
                'name': '삼음교 (三陰交, SP6)', 
                'image': 'SP6.png',
                'position': '안쪽 복사뼈 중심에서 위로 3치 올라간 정강이뼈 뒷가장자리 안쪽'
            }
        ],
        'daily_condition': '소변(小便)이 넉넉하고 시원하게 콸콸 잘 나올 때 하체가 가벼워지고 가장 완벽하게 건강한 상태(완실무병)입니다.',
        'description': "폐의 기능은 성하고 간의 기능은 약한 '폐대간소(肺大肝小)'의 장부 구조를 지녔습니다. 목덜미 기세가 웅장하며 거침없는 소통 능력과 대인 관계 리더십을 발휘합니다. 극히 드문 체질입니다.",
        'herbs': [
            {
                'efficacy': '약한 간 기운과 뼈를 튼튼하게 하여 하체의 힘을 기르고 근육이 마르는 것을 방지합니다.',
                'name': '오가피 (오가피, 가시오갈피 뿌리껍질)',
                'processing': "오가피의 가지나 뿌리 껍질을 채취하여 깨끗이 씻은 후 물기를 빼고 적당한 크기로 썹니다. 약성을 더 부드럽고 따뜻하게 하기 위해 '소금물에 살짝 담갔다가 꺼내어 볶아서(염수초, 鹽水炒)' 사용합니다."
            },
            {
                'efficacy': '기의 흐름을 원활하게 조절하여 식도가 좁아져 음식을 잘 넘기지 못하는 구토 증상을 가라앉히고 하체 다리 근육의 쥐를 풀어줍니다.',
                'name': '모과 (木瓜)',
                'processing': '가을철 잘 익은 모과를 깨끗이 씻어 4등분 한 후 속의 씨를 완전히 긁어냅니다. 얇게 썰어 끓는 물에 살짝 데쳐내거나 증기에 가볍게 찐 다음 햇볕에 건조하여 사용합니다.'
            }
        ],
        'name_hanja': '太陽人',
        'tea_recipe': '염수초한 오가피 12g과 말린 모과 8g에 물 1L를 붓고 은은한 불에 달여 물 대용으로 수시로 섭취합니다.',
        'warning_signs': '음식을 삼키기 어렵고 식도가 조여오는 느낌이 들거나, 자꾸 맑은 침이나 거품을 토하는 역류 증상(열격·반위증)이 생기면 위급한 신호입니다.'
    },
    '태음인': {
        'acupoints_acute': [
            {
                'method': '과열되기 쉬운 간의 열을 내리고 혈압을 안정시킵니다. 다소 강한 압박감(뻐근함)이 느껴질 정도로 5초간 꾹 눌러줍니다.',
                'name': '태충 (太衝, LR3)', 
                'image': 'LR3.png',
                'position': '첫째와 둘째 발가락뼈가 만나는 곳에서 약간 위쪽의 오목하고 맥박이 느껴지는 부위'
            },
            {
                'method': '간 수열(간의 열 독소)을 맑게 식히고 두통과 충혈을 완화해 줍니다. 손끝이나 지압봉으로 강하게 지압(사법)합니다.',
                'name': '행간 (行間, LR2)', 
                'image': 'LR2.png',
                'position': '첫째와 둘째 발가락 사이의 갈라진 경계선 부위'
            }
        ],
        'acupoints_daily': [
            {
                'method': '약해지기 쉬운 폐의 기운을 보강하기 위해, 손가락 끝으로 3초간 지긋이 누르기를 10회 반복합니다. 뜸을 가볍게 뜨는 것도 좋습니다.',
                'name': '태연 (太淵, LU9)', 
                'image': 'LU9.png',
                'position': '손목 안쪽 주름의 요골 쪽(엄지손가락 쪽) 맥박이 뛰는 부위'
            },
            {
                'method': '폐의 소통을 돕고 호흡기를 보호하는 자리입니다. 가볍게 원을 그리며 마사지하듯 눌러줍니다.',
                'name': '열결 (列缺, LU7)', 
                'image': 'LU7.png',
                'position': '양손의 엄지와 검지 사이를 엇갈려 잡았을 때, 집게손가락 끝이 닿는 손목 안쪽의 오목한 틈새'
            }
        ],
        'daily_condition': '땀(汗)이 전신에 잘 나고 소통이 원활할 때 몸이 가장 개운하고 건강한 상태(완실무병)입니다.',
        'description': "간의 기능은 성하고 폐의 기능은 약한 '간대폐소(肝大肺小)'의 장부 구조를 타고났습니다. 체구가 듬직하고 기세가 장대하며, 무엇이든 묵묵히 성취해 내는 끈기가 있습니다.",
        'herbs': [
            {
                'efficacy': '비위(위장)와 폐의 습한 기운을 없애주고 노폐물 배출을 도와 자양강장 및 체중 조절에 좋습니다.',
                'name': '의이인 (薏苡仁, 율무)',
                'processing': "껍질을 벗긴 율무를 흐르는 물에 깨끗이 씻어 말린 뒤, 가마솥이나 팬에 '약한 불로 노릇노릇해질 때까지 볶아서(초법, 炒法)' 사용합니다. 볶으면 찬 성질이 완화되고 고소해집니다."
            },
            {
                'efficacy': '간에 쌓인 열과 독소를 풀어주고 땀구멍을 열어주어 주독(술독) 및 초기 감기 발열을 가라앉힙니다.',
                'name': '갈근 (葛根, 칡뿌리)',
                'processing': "가을에 캔 칡뿌리를 깨끗이 씻어 겉껍질을 벗긴 후, 얇게 썰어 '햇볕에 바짝 건조'하여 사용합니다. 수분이 있으면 약효가 변질되므로 완전히 건조하는 것이 핵심입니다."
            }
        ],
        'name_hanja': '太陰人',
        'tea_recipe': '볶은 율무 20g과 건조한 갈근 10g에 물 1L를 붓고, 약한 불에서 물이 반으로 줄 때까지 은근히 끓여 하루 2-3회 차처럼 음용합니다.',
        'warning_signs': '피부가 야무지고 딴딴해지며 땀이 나지 않거나, 가슴이 심하게 두근거리며 울렁거리는 증상(정충증)이 생기면 몸의 순환이 막히고 있다는 위험 신호입니다.'
    }
}

QUESTIONS = [
    {
        'category': '체형 및 외모 (기상)',
        'id': 1,
        'options': [
            {'scores': {'태양인': 1.0}, 'text': '목덜미 부근(목과 어깨 사이)의 기세는 우뚝 솟아 발달해 보이나, 상대적으로 엉덩이와 하체가 외롭고 빈약해 보인다.'},
            {'scores': {'소양인': 1.0}, 'text': '가슴둘레(상체) 부위가 떡 벌어지고 실해 보이나, 엉덩이와 골반 부위가 빈약하여 앉아 있는 자세가 다소 불안정해 보인다.'},
            {'scores': {'태음인': 1.0}, 'text': '허리둘레와 복부(요척)가 튼튼하게 발달하여 골격이 듬직하고 기세가 장대하지만, 상대적으로 목덜미 기운은 약해 보인다.'},
            {'scores': {'소음인': 1.0}, 'text': '엉덩이와 골반(이둔) 부위가 잘 발달하여 앉아 있는 자세가 매우 안정적이고 아담하지만, 가슴둘레와 상체 기세가 좁고 빈약해 보인다.'}
        ],
        'question': '거울을 보거나 남들이 말할 때, 나의 전체적인 신체 실루엣과 가장 가까운 것은 무엇인가요?',
        'weight': 1.0
    },
    {
        'category': '성격 및 재간 (성정)',
        'id': 2,
        'options': [
            {'scores': {'태양인': 1.0}, 'text': '새로운 사람들과 막힘없이 적극적으로 소통하고 대인 관계를 넓히는 일(교우)에 뛰어난 과단성이 있다.'},
            {'scores': {'소양인': 1.0}, 'text': '행동이 민첩하고 굳세며, 공적인 업무나 어려운 사무를 시원시원하고 빠르게 처리하는 데 유능하다.'},
            {'scores': {'태음인': 1.0}, 'text': '한 번 정착한 곳에서 묵묵하게 일을 꾸준히 진행하며, 어떤 난관이 있어도 끝까지 일(거처)을 완수해 내는 인내심이 있다.'},
            {'scores': {'소음인': 1.0}, 'text': '매사에 온화하고 침착하며 치밀하게 생각하고 계획을 짜며, 내적인 무리를 조화롭게 조직하고 이끄는 데 장점이 있다.'}
        ],
        'question': '업무를 처리하거나 대인 관계에서 나타나는 나만의 가장 돋보이는 행동 스타일은 무엇인가요?',
        'weight': 1.0
    },
    {
        'category': '완실무병 (건강할 때의 핵심 지표)',
        'id': 3,
        'options': [
            {'scores': {'태양인': 1.5}, 'text': '소변이 막힘없이 시원하게 아주 잘 나오고 양이 넉넉할 때 몸이 가볍다.'},
            {'scores': {'소양인': 1.5}, 'text': '대변이 하루라도 거르지 않고 막힘없이 아주 부드럽고 시원하게 매일 잘 나온다.'},
            {'scores': {'태음인': 1.5}, 'text': '운동이나 목욕(사우나)을 통해 전신 땀구멍이 열려 땀을 흠뻑 개운하게 흘리고 나도 피곤하지 않고 몸이 개운하다.'},
            {'scores': {'소음인': 1.5}, 'text': '음식을 찬 것이든 뜨거운 것이든 가리지 않고 맛있게 먹고, 체기 없이 소화가 아주 훌륭하게 잘 된다.'}
        ],
        'question': "몸 컨디션이 최고조로 좋아 '아주 건강하다'고 느낄 때 나타나는 대표적인 내 몸의 신호는 무엇인가요?",
        'weight': 1.5
    },
    {
        'category': '특이 병증 (몸이 지치거나 아플 때)',
        'id': 4,
        'options': [
            {'scores': {'태양인': 1.5}, 'text': '음식물을 삼키는 목구멍이나 식도가 뻑뻑하게 좁아지는 느낌이 들거나, 속에서 신침이나 맑은 침이 솟구쳐 토하려 한다.'},
            {'scores': {'소양인': 1.5}, 'text': '대변이 하루이틀만 통하지 않아도 아랫배가 더부룩해지면서 가슴 속이 불이 붙는 듯이 뜨거워지고 머리가 지끈거린다.'},
            {'scores': {'태음인': 1.5}, 'text': '기가 위로 솟구치며 이유 없이 가슴이 쿵쾅거리고 울렁거리거나(정충증), 눈꺼풀이 미세하게 떨리고 눈 속 깊은 곳이 쏘듯이 아프다.'},
            {'scores': {'소음인': 1.5}, 'text': '가끔 평소에 깊은 한숨을 크게 쉬며, 몸살 기운에 억지로 땀을 흘리고 나면 힘이 쏙 빠지고 몸이 더 처지고 극도로 피로해진다.'}
        ],
        'question': '극도로 피곤하거나 컨디션이 악화되었을 때 몸에서 즉각적으로 나타나는 고유한 불편함은 무엇인가요?',
        'weight': 1.5
    },
    {
        'category': '피부 및 뼈마디의 감각 (정밀 확인)',
        'id': 5,
        'options': [
            {'scores': {'태양인': 1.5}, 'text': '피부나 근육질이 비교적 조밀하지 못하고 살결이 거칠거나 보통이며, 서 있는 하반신의 관절이 쉽게 떨리거나 허약하다.'},
            {'scores': {'소양인': 1.5}, 'text': '상반신(어깨, 가슴)에 힘이 많이 들어가며 뼈대가 견고하나, 상대적으로 발이 다소 가볍고 걸음걸이가 매우 빠르다.'},
            {'scores': {'태음인': 1.5}, 'text': '피부 가죽이 연하지 않고 비교적 두껍거나 듬직하며, 피부가 야무지게 단단하고 조여드는 느낌이 들면 몸에 병이 있는 신호이다.'},
            {'scores': {'소음인': 1.5}, 'text': '살결이 대단히 부드럽고 고우며, 손끝으로 만졌을 때 살가죽과 근육이 매우 짜임새 있고 야무지게 단단해야 건강한 상태이다.'}
        ],
        'question': '나의 피부 상태 및 만졌을 때의 탄력, 뼈마디의 전반적인 결합 상태는 어떠한가요?',
        'weight': 1.5
    }
]

# Page Configuration
st.set_page_config(
    page_title="사상의학 자가 진단 및 한방 홈케어 가이드",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
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
    
    st.markdown("### ⚠️ 자가 지압 시 주의사항")
    st.warning("""
    - **식사 직후**: 식후 1시간 이내에는 소화에 지장을 줄 수 있으므로 강한 지압을 피합니다.
    - **임산부 금기**: '합곡(LI4)'과 '삼음교(SP6)'는 자궁을 수축시키는 작용이 있어 임산부는 절대 지압하거나 침뜸을 하지 않습니다.
    - **자극 강도**: 너무 아프게 누르기보다 3-5초간 뻐근한 느낌(득기감)이 드는 수준으로 부드럽게 지긋이 누르세요.
    - **상처 부위**: 염증, 상처, 혹은 부어오른 관절 부위는 직접 압박하지 않습니다.
    """)
    st.divider()
    st.markdown("### 📱 주요 기능")
    st.write("1. 사상체질 정밀 진단")
    st.write("2. 평소 양생 가이드 (보법)")
    st.write("3. 아플 때 긴급 가이드 (사법)")
    st.write("4. 약재 법제(가공) 및 한방 차 조제")

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
                img_url = get_gdrive_image_url(pt.get('image', ''))
                if img_url:
                    st.image(img_url, caption=f"{pt['name']} 실시간 연동 이미지", use_container_width=True)
                else:
                    # Default Placeholder Image
                    st.image("https://cdn-icons-png.flaticon.com/512/10415/10415848.png", 
                             caption=f"연동 대기: {pt.get('image', 'img.png')}", width=120)
                    st.caption("💡 구글 드라이브 고유 파일 ID를 매핑하면 실시간 이미지가 로드됩니다.")
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
                img_url = get_gdrive_image_url(pt.get('image', ''))
                if img_url:
                    st.image(img_url, caption=f"{pt['name']} 실시간 연동 이미지", use_container_width=True)
                else:
                    # Default Placeholder Image
                    st.image("https://cdn-icons-png.flaticon.com/512/2855/2855146.png", 
                             caption=f"연동 대기: {pt.get('image', 'img.png')}", width=120)
                    st.caption("💡 구글 드라이브 고유 파일 ID를 매핑하면 실시간 이미지가 로드됩니다.")
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
