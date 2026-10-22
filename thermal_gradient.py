import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_thermal_gradient():
    # Настройка координатной сетки для патентного листа
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 95)
    ax.set_aspect('equal')
    ax.axis('off')

    # 1. ЗАЛИВКА ВАКУУМНОГО КОРПУСА (ФОН)
    vacuum = patches.Rectangle((5, 5), 135, 85, facecolor='#F4F6F7', edgecolor='#34495E', linewidth=2.0)
    ax.add_patch(vacuum)
    ax.text(8, 87, 'HERMETIC VACUUM SHIELDING CASING', fontsize=9, color='#34495E', fontweight='bold')

    # 2. ГЕНЕРАЦИЯ ДВУМЕРНОГО ГРАДИЕНТА ТЕМПЕРАТУР (от 200°C до 230°C)
    y_mgo_bottom = 15
    y_mgo_top = 45
    mgo_height = y_mgo_top - y_mgo_bottom
    
    # Базовая линия основания подложки
    ax.plot(list(range(20, 106, 85)), list(range(15, 16, 1)) * 2, color='#2C3E50', linewidth=1.5)
    
    # Вертикальные границы разделения гребней и каналов
    # Координаты: 20, 25, 30, 45, 50, 55, 70, 75, 80, 95, 100, 105
    x_borders = list()
    for x_val in range(20, 31, 5): x_borders.append(x_val)
    for x_val in range(45, 56, 5): x_borders.append(x_val)
    for x_val in range(70, 81, 5): x_borders.append(x_val)
    for x_val in range(95, 106, 5): x_borders.append(x_val)
    
    for x in x_borders:
        ax.plot(list([x, x]), list([y_mgo_bottom, y_mgo_top]), color='#7F8C8D', linewidth=1.0)
        
    # Рисуем градиентные полосы в гребнях MgO с помощью послойных полигонов
    ridges = list()
    ridges.append((20, 30))
    ridges.append((45, 55))
    ridges.append((70, 80))
    ridges.append((95, 105))
    steps = 30 
    
    for start, end in ridges:
        for i in range(steps):
            y1 = y_mgo_bottom + (i / steps) * mgo_height
            y2 = y_mgo_bottom + ((i + 1) / steps) * mgo_height
            
            factor = (i / steps) ** 1.5
            red_intensity = 0.4 + 0.6 * factor
            color_hex = f'#{int(255):02x}{int(230 * (1 - factor)):02x}{int(230 * (1 - factor)):02x}'
            
            rect_layer = patches.Rectangle((start, y1), end - start, y2 - y1, facecolor=color_hex, edgecolor='none')
            ax.add_patch(rect_layer)
            
        rect_border = patches.Rectangle((start, y_mgo_bottom), end - start, mgo_height, fill=False, edgecolor='#7F8C8D', linewidth=0.8)
        ax.add_patch(rect_border)

    # 3. ОТРИСОВКА КАНАЛОВ ТЕПЛОНОСИТЕЛЯ (Стабильные 200°C - Темный Бордо)
    channels = list()
    channels.append((30, 45))
    channels.append((55, 70))
    channels.append((80, 95))
    
    for start, end in channels:
        rect_ch = patches.Rectangle((start, y_mgo_bottom), end - start, mgo_height, facecolor='#A93226', edgecolor='#7F8C8D', linewidth=0.8)
        ax.add_patch(rect_ch)
        
        ch_center = (start + end) / 2
        ax.annotate('', xy=(ch_center, 41), xytext=(ch_center, 19),
                    arrowprops=dict(arrowstyle="->", color="#7B241C", linewidth=1.5))

    # 4. ОРБИТАЛЬНЫЙ КОЛЛЕКТОР Pt (45 - 53)
    rect_pt = patches.Rectangle((20, 45), 85, 8, facecolor='#E61A1A', edgecolor='#34495E', linewidth=1.0)
    ax.add_patch(rect_pt)
    ax.plot(list(range(20, 106, 85)), list(range(53, 54, 1)) * 2, color='black', linewidth=1.5)
    
    # Стрелки орбитальной накачки
    for y_arrow in range(47, 51, 3):
        for x_arrow in range(25, 95, 22):
            ax.annotate('', xy=(x_arrow + 10, y_arrow), xytext=(x_arrow, y_arrow),
                        arrowprops=dict(arrowstyle="->", color="#2471A3", linewidth=1.2))

    # 5. АЛЬТИМАГНИТНЫЙ БАРЬЕР RuO₂ (53 - 60)
    rect_ruo2 = patches.Rectangle((20, 53), 85, 7, facecolor='#FF0000', edgecolor='#8E44AD', linewidth=1.2)
    ax.add_patch(rect_ruo2)

    # Значки ТГц магнонных волн
    for x_spin in range(24, 105, 14):
        ax.text(x_spin, 56.5, '∼波∼', fontsize=8, color='#FFFFFF', fontweight='bold', ha='center', va='center')

    # 6. НАНОАНТЕННЫ И ИК-ЗЕРКАЛО (60 - 66)
    y_ant_bottom = 60
    y_ant_top = 66
    ant_x = list()
    ant_y = list()
    ant_y.append(y_ant_bottom)
    
    x_curr = 20
    for _ in range(6):
        ant_x.extend(list([x_curr, x_curr + 9, x_curr + 9, x_curr + 14]))
        ant_y.extend(list([y_ant_top, y_ant_top, y_ant_bottom, y_ant_bottom]))
        x_curr += 14
    ant_x.append(104)
    ant_y.append(y_ant_bottom)
    ant_x.append(105)
    ant_y.append(y_ant_top)
    
    poly_pts = list()
    for x_p, y_p in zip(ant_x, ant_y): poly_pts.append((x_p, y_p))
    poly_pts.append((105, 60))
    poly_pts.append((20, 60))
    ax.add_patch(patches.Polygon(poly_pts, facecolor='#F1C40F', edgecolor='#F39C12', linewidth=1.2, alpha=0.8))
    
    rect_mirror = patches.Rectangle((20, 66), 85, 2, facecolor='#1ABC9C', edgecolor='none')
    ax.add_patch(rect_mirror)

    # 7. СИЛОВЫЕ ПРОВОДНИКИ (Безопасное поштучное добавление через append)
    x_blue = list()
    x_blue.append(105)
    x_blue.append(120)
    x_blue.append(120)
    
    y_blue = list()
    y_blue.append(66)
    y_blue.append(66)
    y_blue.append(11)
    
    ax.plot(x_blue, y_blue, color='#2980B9', linewidth=2.0)
    
    x_red = list()
    x_red.append(105)
    x_red.append(125)
    x_red.append(125)
    
    y_red = list()
    y_red.append(49)
    y_red.append(49)
    y_red.append(8)
    
    ax.plot(x_red, y_red, color='#C0392B', linewidth=2.0)
    
    ax.text(120, 11, '―', fontsize=12, color='#2980B9', fontweight='bold', ha='center', va='center')
    ax.text(125, 8, '+', fontsize=14, color='#C0392B', fontweight='bold', ha='center', va='center')
    ax.text(129, 9.5, 'DC Output\n(20V / 3.3A)', fontsize=9, color='#2C3E50', fontweight='bold', ha='left', va='center')

    # 8. УКАЗАТЕЛИ И НАУЧНЫЕ ВЫНОСКИ ГРАДИЕНТА
    ax.text(62, 85, 'THERMAL GRADIENT & MAGNON GENERATION ZONE', fontsize=12, color='#2C3E50', fontweight='bold', ha='center')
    
    # Шкала температур справа (Colorbar)
    for i in range(steps):
        y_layer = 22 + (i / steps) * 32
        f = i / steps
        c_hex = f'#{int(255):02x}{int(230 * (1 - f)):02x}{int(230 * (1 - f)):02x}'
        ax.add_patch(patches.Rectangle((112, y_layer), 4, 32/steps, facecolor=c_hex, edgecolor='none'))
    
    ax.add_patch(patches.Rectangle((112, 22), 4, 32, fill=False, edgecolor='#34495E', linewidth=0.8))
    ax.text(118, 22, '200°C', fontsize=8, va='center')
    ax.text(118, 38, '215°C', fontsize=8, va='center')
    ax.text(118, 54, '230°C', fontsize=8, va='center')
    ax.text(115, 58, 'Gradient', fontsize=8, fontweight='bold', ha='center')

    ax.text(12, 70, 'Altermagnetic Interface (30)\nMagnon Multiplier Zone (230°C)', fontsize=9, color='#8E44AD', fontweight='bold', ha='right', va='center')
    ax.annotate('', xy=(42, 56.5), xytext=(13, 70), arrowprops=dict(arrowstyle="-|>", color="#8E44AD", linewidth=1.0))

    ax.text(62, 74, '真空 VACUUM INSULATION SPACE', fontsize=9, color='#7F8C8D', ha='center')
    ax.text(62, 18, '10', fontsize=11, color='#7F8C8D', fontweight='bold', ha='center', va='center')

    plt.tight_layout()
    plt.savefig('h:/Rectena/zimnitsky_cell_thermal_gradient.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Градиентный тепловой чертеж успешно сформирован!")

if __name__ == '__main__':
    draw_thermal_gradient()
