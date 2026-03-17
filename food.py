def render_guide(selected_meal, date):
    bold_c, soft_c = color_map[selected_meal]
    menu = menu_data[date].get(selected_meal, ["정보 없음"])
    
    # 인덱스 버튼 HTML 생성
    tabs_html = ""
    meals = ["조식", "간편식", "중식", "석식", "야식"]
    
    for label in meals:
        b_color, _ = color_map[label]
        is_selected = (label == selected_meal)
        
        # 선택된 메뉴는 더 튀어나오게, 아니면 살짝 가려지게
        margin_left = "-2px" if is_selected else "0px"
        z_index = "10" if is_selected else "1"
        opacity = "1.0" if is_selected else "0.7"
        font_size = "14px" if is_selected else "12px"
        
        tabs_html += f"""
        <div style="
            background-color:{b_color}; 
            flex: 1; 
            width: 40px; 
            color: white; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            writing-mode: vertical-rl; 
            text-orientation: upright; 
            font-weight: bold; 
            font-size: {font_size}; 
            opacity: {opacity};
            border-radius: 0 10px 10px 0; 
            margin-left: {margin_left};
            z-index: {z_index};
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            border-bottom: 1px solid rgba(255,255,255,0.2);
        ">
            {label}
        </div>
        """

    # 카드 + 인덱스 통합 HTML
    full_html = f"""
    <div style="display: flex; width: 100%; min-height: 380px; font-family: 'Pretendard', sans-serif; align-items: stretch;">
        <div style="
            flex: 1; 
            background-color: {soft_c}; 
            border: 3px solid {bold_c}; 
            border-radius: 20px 0 20px 20px; 
            padding: 25px 15px; 
            text-align: center;
            display: flex; 
            flex-direction: column; 
            justify-content: center;
            box-shadow: -4px 4px 10px rgba(0,0,0,0.05);
            z-index: 5;
        ">
            <span style="color: {bold_c}; font-size: 16px; font-weight: bold; border: 1px solid {bold_c}; padding: 2px 10px; border-radius: 10px; width: fit-content; margin: 0 auto 15px;">{selected_meal}</span>
            <h2 style="font-size: 24px; font-weight: 900; color: #333; margin: 10px 0;">{menu[0]}</h2>
            <div style="width: 30px; height: 2px; background-color: {bold_c}; margin: 15px auto; opacity: 0.5;"></div>
            <p style="font-size: 16px; color: #555; line-height: 1.8; word-break: keep-all;">
                {'<br>'.join(menu[1:]) if len(menu) > 1 else ""}
            </p>
        </div>
        
        <div style="display: flex; flex-direction: column; width: 40px;">
            {tabs_html}
        </div>
    </div>
    """
    return full_html
