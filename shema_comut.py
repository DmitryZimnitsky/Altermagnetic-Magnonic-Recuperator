import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_commutation_schema():
    # Создаем холст для двух патентных фигур (ЕСКД / Белгосдело)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 11), dpi=300)
    
    # -------------------------------------------------------------------------
    # ФИГ. 2: ТОПОЛОГИЯ СЕГМЕНТИРОВАНИЯ СВЕРХУ (СТРИП-ПОЛОСЫ)
    # -------------------------------------------------------------------------
    ax1.set_xlim(0, 140)
    ax1.set_ylim(0, 50)
    ax1.set_aspect('equal')
    ax1.axis('off')
    
    # Контур модуля 40х40 мм
    ax1.add_patch(patches.Rectangle((30, 5), 80, 40, fill=False, edgecolor='black', linewidth=1.5))
    
    # Отрисовка стрип-полос (показываем первые несколько и схематичный разрыв)
    for i in range(5):
        x_pos = 30 + i * 8
        ax1.add_patch(patches.Rectangle((x_pos, 5), 8, 40, fill=False, edgecolor='black', linewidth=0.8, linestyle='-'))
        # Стрелка направления тока внутри полосы (вверх/вниз)
        ax1.annotate('', xy=(x_pos + 4, 38), xytext=(x_pos + 4, 12), arrowprops=dict(arrowstyle="->", color="black", linewidth=0.8))
    
    # Символический разрыв матрицы (показываем, что полос много)
    ax1.text(74, 25, '. . . . . . . . . . . . . . . . .', fontsize=14, fontweight='bold', ha='center', va='center')
    
    # Конечные полосы
    for i in range(2):
        x_pos = 94 + i * 8
        ax1.add_patch(patches.Rectangle((x_pos, 5), 8, 40, fill=False, edgecolor='black', linewidth=0.8, linestyle='-'))
        ax1.annotate('', xy=(x_pos + 4, 38), xytext=(x_pos + 4, 12), arrowprops=dict(arrowstyle="->", color="black", linewidth=0.8))

    # Выноски для Фиг. 2
    ax1.annotate('', xy=(34, 40), xytext=(15, 43), arrowprops=dict(arrowstyle="-|>", color="black", facecolor="black", linewidth=0.8))
    ax1.plot(list([10, 15]), list([43, 43]), color='black', linewidth=1.0)
    ax1.text(12, 44, '8', fontsize=10, fontweight='bold') # Поз. 8 - Стрип-полоса
    
    ax1.text(70, -2, 'Фиг. 2', fontsize=12, fontweight='bold', ha='center')

    # -------------------------------------------------------------------------
    # ФИГ. 3: ПРОФИЛЬНЫЙ РАЗРЕЗ И СХЕМА ПОСЛЕДОВАТЕЛЬНОЙ КОММУТАЦИИ (Z-КАСКАД)
    # -------------------------------------------------------------------------
    ax2.set_xlim(0, 140)
    ax2.set_ylim(0, 50)
    ax2.set_aspect('equal')
    ax2.axis('off')
    
    # Рисуем 3 изолированные последовательные полосы
    # Каждая полоса состоит из Нижнего коллектора (+), Барьера и Наноантенн (-)
    strip_widths = 25
    gap = 6
    
    for s in range(3):
        x_s = 25 + s * (strip_widths + gap)
        
        # Нижний коллектор (Плюс полосы)
        ax2.add_patch(patches.Rectangle((x_s, 15), strip_widths, 4, fill=False, hatch='///', edgecolor='black', linewidth=1.0))
        # Активный альтимагнитный барьер
        ax2.add_patch(patches.Rectangle((x_s, 19), strip_widths, 2, facecolor='black', alpha=0.1, edgecolor='black', linewidth=0.8))
        # Верхние наноантенны (Минус полосы)
        ax2.add_patch(patches.Rectangle((x_s, 21), strip_widths, 3, fill=False, hatch='\\\\\\', edgecolor='black', linewidth=1.0))
        
        # Внутренние маркеры полярности полосы
        ax2.text(x_s + 4, 17, '+', fontsize=9, ha='center', va='center')
        ax2.text(x_s + strip_widths - 4, 22.5, '−', fontsize=11, ha='center', va='center')

        # ПОСЛЕДОВАТЕЛЬНАЯ СВЯЗЬ: Минус предыдущей идет на Плюс следующей (Z-коммутация)
        if s > 0:
            x_prev_minus = x_s - gap
            # Проводник связи «Змейка»
            ax2.plot(list([x_prev_minus, x_prev_minus + gap/2, x_prev_minus + gap/2, x_s]), 
                     list([22.5, 22.5, 17, 17]), color='black', linewidth=1.2, linestyle='-')
            # Стрелка течения перетекающего тока
            ax2.annotate('', xy=(x_s - 1, 17), xytext=(x_prev_minus + 2, 22.5),
                        arrowprops=dict(arrowstyle="->", color="black", connectionstyle="arc3,rad=.2", linewidth=1.0))

    # Магистральные выводы модуля
    # Главный минус (−) с левого края первой полосы
    ax2.plot(list([25, 10, 10]), list([22.5, 22.5, 5]), color='black', linewidth=1.5)
    ax2.text(10, 3, '−', fontsize=14, fontweight='bold', ha='center')
    
    # Главный плюс (+) с правого края последней полосы
    ax2.plot(list([112, 125, 125]), list([17, 17, 5]), color='black', linewidth=1.5)
    ax2.text(125, 3, '+', fontsize=12, fontweight='bold', ha='center')

    # Выноски для Фиг. 3
    # Линия к верхнему минусовому слою полосы
    ax2.annotate('', xy=(38, 22.5), xytext=(15, 33), arrowprops=dict(arrowstyle="-|>", color="black", facecolor="black", linewidth=0.8))
    ax2.plot(list([10, 15]), list([33, 33]), color='black', linewidth=1.0)
    ax2.text(12, 34, '9', fontsize=10, fontweight='bold') # Поз. 9 - Верхний токосъем полосы (Минус)

    # Линия к нижнему плюсовому слою соседней полосы
    ax2.annotate('', xy=(62, 17), xytext=(15, 10), arrowprops=dict(arrowstyle="-|>", color="black", facecolor="black", linewidth=0.8))
    ax2.plot(list([10, 15]), list([10, 10]), color='black', linewidth=1.0)
    ax2.text(12, 11, '10', fontsize=10, fontweight='bold') # Поз. 10 - Нижний коллектор полосы (Плюс)
    
    # Линия к коммутационному мостику
    ax2.annotate('', xy=(53, 20), xytext=(70, 38), arrowprops=dict(arrowstyle="-|>", color="black", facecolor="black", linewidth=0.8))
    ax2.plot(list([70, 75]), list([38, 38]), color='black', linewidth=1.0)
    ax2.text(72, 39, '11', fontsize=10, fontweight='bold') # Поз. 11 - Последовательный Z-мостик

    ax2.text(70, -2, 'Фиг. 3', fontsize=12, fontweight='bold', ha='center')

    # Сохранение листов
    plt.tight_layout()
    plt.savefig('h:/Rectena/zimnitsky_cell_commutation.png', dpi=300, bbox_inches='tight')
    plt.savefig('h:/Rectena/zimnitsky_cell_commutation.svg', format='svg', bbox_inches='tight')
    plt.close()
    print("Схемы коммутации Фиг. 2 и Фиг. 3 успешно сгенерированы в PNG и SVG!")

if __name__ == '__main__':
    draw_commutation_schema()
