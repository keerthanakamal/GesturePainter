def fingers_up(lm_list):
    fingers = []

    if not lm_list or len(lm_list) < 21:
        return [0, 0, 0, 0, 0]

    # Thumb
    fingers.append(1 if lm_list[4][1] > lm_list[3][1] else 0)

    # Other fingers
    tips = [8, 12, 16, 20]
    for tip_id in tips:
        fingers.append(1 if lm_list[tip_id][2] < lm_list[tip_id - 2][2] else 0)

    return fingers
