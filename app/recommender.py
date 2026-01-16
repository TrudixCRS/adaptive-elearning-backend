def score_candidate(mastery: float, attempts: int, pref_weight: float, difficulty: int) -> tuple[float, str]:
    need = 1.0 - mastery
    struggle = min(attempts / 3.0, 1.0)

    if mastery < 0.40:
        dmatch = 1.0 if difficulty == 1 else 0.3
    elif mastery < 0.75:
        dmatch = 1.0 if difficulty == 2 else 0.6
    else:
        dmatch = 1.0 if difficulty == 3 else 0.6

    score = 0.45*need + 0.20*pref_weight + 0.20*(1.0 - struggle) + 0.15*dmatch
    reason = f"need={need:.2f}, pref={pref_weight:.2f}, attempts={attempts}, dmatch={dmatch:.2f}"
    return score, reason
