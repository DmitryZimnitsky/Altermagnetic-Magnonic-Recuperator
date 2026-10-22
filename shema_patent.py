import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_belarus_patent_schema():
    # Создаем холст 12х8 дюймов с высоким разрешением для печати на листах А4
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 100)
    ax.set_aspect('equal')
    ax.axis('off') # Полностью отключаем оси координат

    # -------------------------------------------------------------------------
    # ГЕОМЕТРИЧЕСКИЕ КООРДИНАТЫ СЛОЕВ (СНИЗУ ВВЕРХ)
    # -------------------------------------------------------------------------
    x_min, x_max = 35, 125
    width = x_max - x_min # 90 единиц

    y0 = 10  # Дно медного основания
    y1 = 32  # Стык основания и каналов MgO
    y2 = 47  # Верхняя бровка MgO / Стык нанослоев
    y3 = 50  # Стык нанослоев и зеркала Фабри-Перо
    y4 = 52  # Стык зеркала и изоляционного канта AlN
    y5 = 54  # Стык изолятора и верхней шины наращивания
    y6 = 76  # Верхняя граница алюминиевого блока

    # -------------------------------------------------------------------------
    # ОТРИСОВКА И ШТРИХОВКА МАКРО-СЛОЕВ ПО ГОСТ / ЕСКД
    # -------------------------------------------------------------------------
    
    # 1. Слой основания (Никелированная медь): плотная металлическая штриховка
    rect_base = patches.Rectangle((x_min, y0), width, y1 - y0, fill=False, hatch='///', edgecolor='black', linewidth=1.5)
    ax.add_patch(rect_base)

    # 2. Слой 4 (Кристаллическая подложка MgO) и микроканалы
    # Задаем координаты вертикальных гребней по X
    x_ridges = list([(35, 45), (60, 70), (85, 95), (115, 125)])
    for r_start, r_end in x_ridges:
        # Диэлектрическая штриховка гребней MgO (редкая сетка)
        rect_ridge = patches.Rectangle((r_start, y1), r_end - r_start, y2 - y1, fill=False, hatch='//', edgecolor='black', linewidth=1.2)
        ax.add_patch(rect_ridge)
        
        # Пунктирный зигзаг полного внутреннего отражения фотонов
        x_mid = (r_start + r_end) / 2
        dx = (r_end - r_start) * 0.3
        y_step = (y2 - y1) / 4
        zx = list([x_mid - dx, x_mid + dx, x_mid - dx, x_mid + dx, x_mid - dx])
        zy = list([y1, y1 + y_step, y1 + 2*y_step, y1 + 3*y_step, y2])
        ax.plot(zx, zy, color='black', linestyle='--', linewidth=0.8)

    # Капиллярные микроканалы с теплоносителем (30% заполнение точками)
    x_channels = list([(45, 60), (70, 85), (95, 115)])
    for c_start, c_end in x_channels:
        rect_chan = patches.Rectangle((c_start, y1), c_end - c_start, y2 - y1, fill=False, hatch='...', edgecolor='black', linewidth=1.0)
        ax.add_patch(rect_chan)
        
        # Инженерные стрелки тока теплоносителя
        ch_mid = (c_start + c_end) / 2
        ax.annotate('', xy=(ch_mid, y2 - 3), xytext=(ch_mid, y1 + 3), arrowprops=dict(arrowstyle="->", color="black", linewidth=1.2))

    # 3. Наноструктурный пакет (Коллектор Pt + Барьер RuO₂ + Наноантенны Al)
    # Из-за наномасштаба показываем единым блоком с перекрестной штриховкой
    rect_nano = patches.Rectangle((x_min, y2), width, y3 - y2, fill=False, hatch='xxx', edgecolor='black', linewidth=1.2)
    ax.add_patch(rect_nano)

    # 4. ИК-Зеркало Фабри-Перо
    rect_mir = patches.Rectangle((x_min, y3), width, y4 - y3, fill=False, hatch='\\\\\\', edgecolor='black', linewidth=1.0)
    ax.add_patch(rect_mir)

    # 5. Изолирующий кант AlN (Тонкая горизонтальная полоса)
    rect_iso = patches.Rectangle((x_min, y4), width, y5 - y4, fill=False, hatch='---', edgecolor='black', linewidth=1.0)
    ax.add_patch(rect_iso)

    # 6. Верхняя шина наращивания (Алюминиевый блок): перекрестная редкая штриховка легких металлов
    rect_top = patches.Rectangle((x_min, y5), width, y6 - y5, fill=False, hatch='\\\\', edgecolor='black', linewidth=1.5)
    ax.add_patch(rect_top)

    # -------------------------------------------------------------------------
    # ВЫНОСКИ ПО СТАНДАРТУ БЕЛАРУСИ (ПРЯМАЯ ЛИНИЯ СО СТРЕЛКОЙ -> ПОЛКА С НОМЕРОМ)
    # -------------------------------------------------------------------------
    def draw_belarus_pointer(arrow_x, arrow_y, shelf_x, shelf_y, text_num):
        # Рисуем тонкую прямую линию со стрелкой на конце, утыкающейся в деталь
        ax.annotate('', xy=(arrow_x, arrow_y), xytext=(shelf_x, shelf_y),
                    arrowprops=dict(arrowstyle="-|>", color="black", facecolor="black", linewidth=0.8, mutation_scale=10))
        # Рисуем горизонтальную жесткую полку ЕСКД под номером
        shelf_length = 8
        ax.plot(list([shelf_x, shelf_x + shelf_length]), list([shelf_y, shelf_y]), color='black', linewidth=1.0)
        # Размещаем номер позиции строго НАД полкой
        ax.text(shelf_x + shelf_length/2, shelf_y + 1, text_num, fontsize=11, fontweight='bold', ha='center', va='bottom')

    # Поз. 1 — Медное никелированное основание
    draw_belarus_pointer(50, 20, 15, 20, '1')
    
    # Поз. 2 — Капиллярные микроканалы
    draw_belarus_pointer(52, 38, 15, 34, '2')
    
    # Поз. 3 — Гребни подложки MgO (ТГц-волноводы)
    draw_belarus_pointer(40, 42, 15, 45, '3')
    
    # Поз. 4 — Квантовый наносэндвич (Pt/RuO₂/Al)
    draw_belarus_pointer(65, 48.5, 15, 54, '4')
    
    # Поз. 5 — Интерференционное ИК-зеркало Фабри-Перо
    draw_belarus_pointer(75, 51, 15, 63, '5')
    
    # Поз. 6 — Изолирующий кант из нитрида алюминия (AlN)
    draw_belarus_pointer(85, 53, 140, 46, '6')
    
    # Поз. 7 — Пассивный алюминиевый блок наращивания габарита
    draw_belarus_pointer(70, 68, 140, 68, '7')

    # Название чертежа для патентного дела (Фиг. 1)
    ax.text(80, 2, 'Фиг. 1', fontsize=14, fontweight='bold', ha='center')

    # -------------------------------------------------------------------------
    # СОХРАНЕНИЕ В ДВУХ ОФИЦИАЛЬНЫХ ФОРМАТАХ
    # -------------------------------------------------------------------------
    plt.tight_layout()
    plt.savefig('h:/Rectena/zimnitsky_cell_patent_schema.png', dpi=300, bbox_inches='tight')
    plt.savefig('h:/Rectena/zimnitsky_cell_patent_schema.svg', format='svg', bbox_inches='tight')
    plt.close()
    print("Патентный чертеж по стандартам Республики Беларусь успешно сохранен в PNG и SVG!")

if __name__ == '__main__':
    draw_belarus_patent_schema()
