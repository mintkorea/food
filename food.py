# [4번 섹션: 배식 안내 및 자동 식사 선택 로직 수정]

def get_meal_schedule(is_weekend):
    lunch_start = time(11, 30) if is_weekend else time(11, 20)
    return {
        "조식": {"start": time(7, 0), "end": time(9, 0)},
        "간편식": {"start": time(7, 0), "end": time(11, 0)}, 
        "중식": {"start": lunch_start, "end": time(14, 0)},
        "석식": {"start": time(17, 20), "end": time(19, 20)},
        "야식": {"start": time(18, 0), "end": time(19, 20)}
    }

def get_realtime_status(selected_meal, meal_exists):
    if d != today_date:
        return f"📅 {d.strftime('%m월 %d일')} {selected_meal} 식단입니다."
    
    now_t = get_now().time()
    schedule = get_meal_schedule(d.weekday() >= 5)
    
    # --- A. 간편식 또는 야식을 명시적으로 선택한 경우 ---
    if selected_meal in ["간편식", "야식"]:
        sched = schedule[selected_meal]
        if sched["start"] <= now_t <= sched["end"]:
            return f"✅ 지금은 <span style='color:#8BC34A;'>{selected_meal} 배식 중</span>입니다."
        if now_t < sched["start"]:
            diff = datetime.combine(today_date, sched["start"], tzinfo=KST) - get_now()
            m = int(diff.total_seconds() // 60)
            return f"⏳ {selected_meal} 제공까지 {m//60}시간 {m%60}분 남았습니다."
        return f"🏁 {selected_meal} 배식이 종료되었습니다."

    # --- B. 기본 식단(조식, 중식, 석식) 로직 ---
    # 1. 현재 선택한 식단이 배식 중인지 확인
    curr_sched = schedule[selected_meal]
    if curr_sched["start"] <= now_t <= curr_sched["end"]:
        return f"✅ 지금은 <span style='color:#8BC34A;'>{selected_meal} 배식 중</span>입니다."

    # 2. 배식 종료 후 다음 메인 식사 안내 (조식->중식->석식->종료)
    main_order = ["조식", "중식", "석식"]
    
    # 현재 시간 기준 다음에 올 메인 식사 찾기
    next_main = None
    for m_name in main_order:
        if now_t < schedule[m_name]["start"]:
            next_main = m_name
            break
            
    if next_main:
        target_dt = datetime.combine(today_date, schedule[next_main]["start"], tzinfo=KST)
        diff = target_dt - get_now()
        total_m = int(diff.total_seconds() // 60)
        h, m = divmod(total_m, 60)
        t_str = f"{h}시간 {m}분" if h > 0 else f"{m}분"
        
        # 선택한 식단이 이미 지난 경우와 아직 안 온 경우 구분
        if now_t > curr_sched["end"]:
            return f"🏁 {selected_meal} 종료! 다음 {next_main}까지 {t_str} 남음"
        else:
            return f"⏳ {selected_meal} 제공까지 {t_str} 남았습니다."
    
    return "🌙 오늘 모든 배식이 종료되었습니다."

# [3-1번 섹션: 초기 접속 시 자동 식사 선택 수정]
if "meal" not in params and d == today_date:
    now_t = get_now().time()
    schedule = get_meal_schedule(today_date.weekday() >= 5)
    
    # 기본값은 조식, 시간대에 따라 중식/석식으로 자동 전환 (간편식/야식은 자동선택 제외)
    if now_t <= schedule["조식"]["end"]:
        selected = "조식"
    elif now_t <= schedule["중식"]["end"]:
        selected = "중식"
    else:
        selected = "석식"
