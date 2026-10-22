import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_altermagnetic_gradient():
    # Создаем холст для детального микро-чертежа (с высоким разрешением 300 DPI)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 85)
    ax.set_aspect('equal')
    ax.axis('off')

    # 1. ЗАЛИВКА ФОНА ГЕРМЕТИЧНОГО ВАКУУМНОГО КОРПУСА
    vacuum = patches.Rectangle((5, 5), 135, 75, facecolor='#F8F9F9', edgecolor='#34495E', linewidth=1.5)
    ax.add_patch(vacuum)
    ax.text(8, 77, 'NANOSCALE RESOLUTION VIEW (BARRIER CLOSE-UP)', fontsize=8, color='#34495E', fontweight='bold')

    # 2. ОПРЕДЕЛЕНИЕ ГЕОМЕТРИИ УВЕЛИЧЕННОГО СЛОЯ RuO₂ (30)
    # Искусственно масштабируем толщину барьера на графике для наглядности микро-слоя
    y_bar_bottom = 25
    y_bar_top = 60
    bar_height = y_bar_top - y_bar_bottom
    x_start = 20
    x_end = 105
    bar_width = x_end - x_start

    # 3. ПОСЛОЙНАЯ ОТРИСОВКА ВНУТРЕННЕГО ТЕМПЕРАТУРНОГО ГРАДИЕНТА (230°C -> 232°C)
    # Используем мелкую вертикальную нарезку для создания плавного теплового перелива (палитра Reds)
    steps = 40
    for i in range(steps):
        y1 = y_bar_bottom + (i / steps) * bar_height
        y2 = y_bar_bottom + ((i + 1) / steps) * bar_height
        
        # Экспоненциальный профиль нарастания температуры (от 230.0 до 232.0 градусов)
        factor = (i / steps) ** 2.0
        color_hex = f'#{int(255):02x}{int(220 * (1 - 0.7 * factor)):02x}{int(220 * (1 - 0.7 * factor)):02x}'
        
        rect_layer = patches.Rectangle((x_start, y1), bar_width, y2 - y1, facecolor=color_hex, edgecolor='none')
        ax.add_patch(rect_layer)

    # Внешний фиолетовый контур альтимагнитного барьера (сохраняем цветовую маркировку)
    rect_border = patches.Rectangle((x_start, y_bar_bottom), bar_width, bar_height, fill=False, edgecolor='#8E44AD', linewidth=2.0)
    ax.add_patch(rect_border)

    # -------------------------------------------------------------------------
    # 4. КВАНТОВАЯ КАРТА СПИНОВЫХ ПОДРЕШЕТОК И ВОЗБУЖДЕНИЯ МАГНOHОВ
    # -------------------------------------------------------------------------
    # Рисуем шахматную сетку чередующихся магнитных моментов (спинов) атомов Рутения (Ru)
    for row in range(4):
        y_pos = y_bar_bottom + 5 + row * 10
        for col in range(7):
            x_pos = x_start + 8 + col * 12
            
            # Чередуем направление спинов (вверх/вниз) в шахматном порядке для альтимагнетика
            is_spin_up = (row + col) % 2 == 0
            
            if is_spin_up:
                ax.text(x_pos, y_pos, '↑', fontsize=14, color='#FFFFFF', fontweight='bold', ha='center', va='center')
                ax.text(x_pos + 3, y_pos - 2, 'Ru⁺', fontsize=7, color='#FFFFFF', ha='center', va='center')
            else:
                ax.text(x_pos, y_pos, '↓', fontsize=14, color='#34495E', fontweight='bold', ha='center', va='center')
                ax.text(x_pos + 3, y_pos - 2, 'Ru⁻', fontsize=7, color='#34495E', ha='center', va='center')

    # Рисуем синусоидальные ТГц-волны размножения магнонов, бегущие вдоль градиента
    x_wave = list()
    for x_idx in range(25, 101):
        x_wave.append(x_idx)
        
    y_wave1 = list()
    y_wave2 = list()
    for x_val in x_wave:
        y_wave1.append(42.5 + 3.0 * math.sin(x_val * 0.4))
        y_wave2.append(42.5 - 3.0 * math.sin(x_val * 0.4))
        
    ax.plot(x_wave, y_wave1, color='#8E44AD', linestyle='-', linewidth=1.5, alpha=0.8)
    ax.plot(x_wave, y_wave2, color='#8E44AD', linestyle='--', linewidth=1.2, alpha=0.6)

    # -------------------------------------------------------------------------
    # 5. ГРАНИЦЫ СОПРЯЖЕНИЯ СМЕЖНЫХ СЛОЕВ
    # -------------------------------------------------------------------------
    # Нижний стык: Орбитальный коллектор (230°C)
    ax.fill_between(list([15, 110]), list([12, 12]), list([y_bar_bottom, y_bar_bottom]), facecolor='#BDC3C7', alpha=0.4)
    ax.plot(list([20, 105]), list([y_bar_bottom, y_bar_bottom]), color='#2980B9', linewidth=2.5)
    ax.text(62, 20, 'PLATINUM COLLECTOR INTERFACE (20) — T_bottom = 230.00°C', fontsize=8, color='#2980B9', fontweight='bold', ha='center')

    # Верхний стык: Алюминиевые наноантенны + ИК-зеркало (232°C)
    ax.fill_between(list([15, 110]), list([y_bar_top, y_bar_top]), list([73, 73]), facecolor='#F1C40F', alpha=0.3)
    ax.plot(list([20, 105]), list([y_bar_top, y_bar_top]), color='#1ABC9C', linewidth=2.5)
    ax.text(62, 65, 'ALUMINUM NANOANTENNA INTERFACE (40) — T_top = 232.00°C', fontsize=8, color='#1ABC9C', fontweight='bold', ha='center')

    # -------------------------------------------------------------------------
    # 6. ШКАЛА ТЕМПЕРАТУРНОГО ГРАДИЕНТА (COLORBAR) ДЛЯ АЛЬТИМАГНЕТИКА
    # -------------------------------------------------------------------------
    for i in range(steps):
        y_layer = y_bar_bottom + (i / steps) * bar_height
        f = i / steps
        c_hex = f'#{int(255):02x}{int(220 * (1 - 0.7 * f)):02x}{int(220 * (1 - 0.7 * f)):02x}'
        ax.add_patch(patches.Rectangle((114, y_layer), 4, bar_height/steps, facecolor=c_hex, edgecolor='none'))
    
    ax.add_patch(patches.Rectangle((114, y_bar_bottom), 4, bar_height, fill=False, edgecolor='#34495E', linewidth=1.0))
    ax.text(120, y_bar_bottom, '230.0°C\n(Interface Pt)', fontsize=8, va='center')
    ax.text(120, (y_bar_bottom + y_bar_top)/2, '231.0°C\n(Mid-Barrier)', fontsize=8, va='center')
    ax.text(120, y_bar_top, '232.0°C\n(Interface Al)', fontsize=8, va='center')
    ax.text(116, y_bar_top + 4, 'RuO₂ Internal\nGradient', fontsize=8, fontweight='bold', ha='center')

    # НАУЧНЫЕ ВЫНОСКИ И ПОДПИСИ
    ax.text(62, 81, 'ALTERMAGNETIC BARRIER (RuO₂) MICROSCOPIC TEMPERATURE PROFILE', fontsize=11, color='#2C3E50', fontweight='bold', ha='center')
    
    ax.text(62, 49, 'Coherent THz Magnon\nMultiplication Zone', fontsize=9, color='#8E44AD', fontweight='bold', ha='center', va='center')
    
    # Сохраняем наноразмерный чертеж градиента барьера
    plt.tight_layout()
    plt.savefig('h:/Rectena/ruo2_magnon_gradient.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Микроскопический градиентный чертеж RuO2 успешно сформирован!")

if __name__ == '__main__':
    import math
    draw_altermagnetic_gradient()
