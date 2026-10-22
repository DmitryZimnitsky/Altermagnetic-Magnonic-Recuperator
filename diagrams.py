import pandas as pd
import matplotlib.pyplot as plt

def generate_transient_plots():
    csv_path = 'h:/Rectena/simulation_data.csv'
    
    try:
        # Читаем идеально чистый файл (теперь по умолчанию с точкой)
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути {csv_path}. Проверьте работу C# симулятора.")
        return

    # Очищаем заголовки колонок от случайных пробелов
    df.columns = df.columns.str.strip()

    # Настройка академического стиля графиков (крупные шрифты, четкие линии)
    plt.rcParams.update({
        'font.size': 11,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'figure.titlesize': 14
    })

    # Создаем двухпанельное поле (1 строка, 2 колонки)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)
    
    # -------------------------------------------------------------------------
    # ЛЕВАЯ ПАНЕЛЬ (а): ТЕМПЕРАТУРНЫЙ РАЗГОН НАНОСЛОЕВ
    # -------------------------------------------------------------------------
    ax1.plot(df['Time(ms)'], df['T_MgO_center(C)'], color='#E67E22', linewidth=2.0, label='MgO Substrate Core')
    ax1.plot(df['Time(ms)'], df['T_Barrier(C)'], color='#8E44AD', linewidth=2.0, label='Altermagnetic Barrier (RuO₂)')
    ax1.plot(df['Time(ms)'], df['T_Antenna(C)'], color='#F1C40F', linewidth=1.8, linestyle='--', label='Aluminum Nanoantennas')
    
    # Горизонтальная линия целевой температуры теплоносителя (200°C)
    ax1.axhline(200.0, color='#C0392B', linestyle=':', linewidth=1.2, label='Thermal Buffer Target (200°C)')

    ax1.set_title('(a) Layer Temperature Transient State', fontsize=12, fontweight='bold', pad=10)
    ax1.set_xlabel('Time (ms)', labelpad=8)
    ax1.set_ylabel('Temperature (°C)', labelpad=8)
    ax1.set_xlim([0, df['Time(ms)'].max()])
    ax1.set_ylim([20, 240])
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9)

    # -------------------------------------------------------------------------
    # ПРАВАЯ ПАНЕЛЬ (б): ВЫХОДНАЯ ЭЛЕКТРИЧЕСКАЯ МОЩНОСТЬ МОДУЛЯ (66 Вт)
    # -------------------------------------------------------------------------
    # График строит интегральное значение мощности напрямую из отсортированного лога C#
    ax2.plot(df['Time(ms)'], df['Output_Power(W)'], color='#2980B9', linewidth=2.5, label='AMTJ Module Power Output')
    
    # Линия проектного максимума для инвесторов
    ax2.axhline(66.0, color='#2C3E50', linestyle='--', linewidth=1.0, alpha=0.7, label='Target Specification (66 W)')

    ax2.set_title('(b) Integrated Electrical Power Generation', fontsize=12, fontweight='bold', pad=10)
    ax2.set_xlabel('Time (ms)', labelpad=8)
    ax2.set_ylabel('Active Power Output (W)', labelpad=8)
    ax2.set_xlim([0, df['Time(ms)'].max()])
    ax2.set_ylim([0, 75])
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9)

    # Общий заголовок инфографики
    plt.suptitle('Zimnitsky Cell (AMTJ-Recuperator) Transient Analysis', fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    # Сохраняем графики в папку
    output_png = 'h:/Rectena/zimnitsky_cell_transient_plots.png'
    output_svg = 'h:/Rectena/zimnitsky_cell_transient_plots.svg'
    
    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    plt.savefig(output_svg, format='svg', bbox_inches='tight')
    plt.close()
    
    print("Научные графики успешно сгенерированы в идеальном качестве!")

if __name__ == '__main__':
    generate_transient_plots()
