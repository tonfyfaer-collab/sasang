# -*- coding: utf-8 -*-
def calculate_scores(answers):
    """답변 데이터를 받아 각 체질별 점수를 정밀 계산합니다."""
    scores = {"태음인": 0.0, "소음인": 0.0, "소양인": 0.0, "태양인": 0.0}
    for q_id, opt in answers.items():
        # opt는 선택된 option 딕셔너리
        weight = opt.get("weight", 1.0)
        for const, val in opt.get("scores", {}).items():
            scores[const] += val * weight
    return scores
