# Altermagnetic Magnetoelectronic Tunnel Junction (AMTJ) Heat Recuperator Simulator
### Core Computation Engine for the "Cell" Physical Architecture

[![License: MIT](https://shields.io)](https://opensource.org)
[![Physics: Altermagnetism](https://shields.io)](https://wikipedia.org)
[![Zenodo DOI](https://shields.io)] (https://doi.org/10.5281/zenodo.23270717) (https://zenodo.org/records/23270717) "Solid-State Magnonic Heat Recuperator Based on Altermagnetic Tunnel Junctions" 

This repository contains the complete cross-platform numerical simulation environment for the **Solid-State Altermagnetic Magnonic Heat Recuperator** (AMTJ).

The project successfully bridges macro-scale fluid thermodynamics with nanoscale THz magnon kinetics and coherent quantum tunneling to harvest industrial waste heat (150°C - 300°C) into stable DC power (20V / 3.3A at steady state) without any external active cooling loops, achieving an unprecedented equivalent figure of merit ZT ≈ 4.5.

---

## 🛠 Repository Structure

*   `/Cell.zip/` (C# / .NET 8.0) — The core transient numerical solver. Implements a conservative 1D finite-difference scheme with harmonic thermal conductivity averaging at heterogeneous thin-film boundaries (Pt → RuO₂ → Al). Automatically triggers the Python visualizers upon completing the time-steps.
*   `diagrams.py` (Python) — Automatically parses the generated `simulation_data.csv`, standardizes the decimal formatting, and plots smooth logarithmic transient curves for layer temperatures and module power output (66W maximum).
*   `belarus_patent_schema.py` (Python) — Vector CAD visualizer that renders monochrome line-art schematics with standard shelf pointers strictly adhering to regional patent office requirements (Fig 1).
*   `thermal_gradient.py` (Python) — Renders the cross-sectional 2D color temperature maps showcasing exponential heat concentration within the dielectric MgO ridges.
*   `ruo2_magnon_gradient.py` (Python) — Nanoscale resolution visualizer illustrating the altermagnetic RuO₂ barrier, displaying internal vertical ∇ T gradients, alternating spin sublattices, and THz magnonic wave propagation tracks.
*   <img width="3216" height="1640" alt="fig1" src="https://github.com/user-attachments/assets/a55d4312-ce7f-40d0-a289-0beca5a030c7" />


---

## 📊 Physical & Simulation Framework

The execution loop solves the transient Fourier heat equation coupled with non-linear Stefan-Boltzmann volumetric emission terms:

\[T_m^{k+1} = T_m^k + \frac{\Delta t}{c_m(T) \rho_m} \left[ \frac{\kappa_{m+1/2}(T) \cdot (T_{m+1}^k - T_m^k) - \kappa_{m-1/2}(T) \cdot (T_m^k - T_{m-1}^k)}{\Delta y^2} + q_{\text{vol}, m}^k \right]\]

Where the effective boundary conductivities are defined via:
\[\kappa_{m+1/2}(T) = \frac{2 \kappa_m(T) \kappa_{m+1}(T)}{\kappa_m(T) + \kappa_{m+1}(T)}\]

### Key Architectural Enhancements Included:
1. **Bi-Gradient Pump System:** Models spatial horizontal thermal compression via fluid microchannels along with the vertical quantum ∇ T pump across the 2.2 nm RuO₂ layer.
2. **Photonic Recuperation Cavity:** Simulates a 95% reflective Fabry-Perot interference mirror (SiO₂/TiO₂), turning unabsorbed THz photons back into the substrate to maintain an isothermal self-regulating equilibrium plateau.
3. **Z-Cascade Strip Topology:** Simulates the reduction of extreme tunnel currents into safe parameters (20V / 3.3A) via N=100 parallel longitudinal strips connected in a serial "snake" topology.
4. **Cascaded Multi-Layer Scaling:** Supports volumetric expansion modeling via vertical cyclic repetition of the active nanosandwich stack for multi-band IR absorption.

---

## 🚀 Quick Start (Automation Out-Of-The-Box)

The C# engine features built-in process automation that handles Python environments natively via the `uv` tool.

1. Clone the repository and open the solution in Visual Studio 2022 or JetBrains Rider.
2. Ensure your source code files are saved in **UTF-8 with BOM** encoding to prevent Cyrillic comment corruption.
3. Hit **F5** (Run).

The engine will compute 500,000 transient time-steps, output live telemetry to the console, dump `simulation_data.csv`, and silently run background Python scripts to write pristine vector `.svg` and `.png` plots right into your working directory.
---
### Simulation Visualizations
<img width="3860" height="1627" alt="fig4" src="https://github.com/user-attachments/assets/4b118657-422e-4b7a-baf0-f44cf07805b2" />
<img width="2876" height="1770" alt="fig5" src="https://github.com/user-attachments/assets/dada72b5-5e25-4a9d-90f1-b4fa43504cb7" />

---

# Твердотельный магнонный рекуператор тепловой энергии на основе альтимагнитных туннельных переходов (AMJT)
### Вычислительный комплекс и математическая FDTD-модель таблетки

Данный раздел репозитория содержит русскоязычное описание физических принципов и архитектуры многослойного квантового преобразователя.

## 💡 Квантово-физическая суть решения
В отличие от классических элементов Пельтье и термоэлектрических генераторов (ТЭГ), эффективность которых разрушается из-за сквозного макроскопического протекания тепловых фононов (закон Видемана — Франца), данное устройство работает в **квази-изотермическом режиме полного термодинамического равновесия ($$\nabla T = 0$$)**. 

Вертикальный тепловой поток от сгорающего топлива или промышленного теплоносителя канализируется через щелевые ТГц-волноводы монокристаллической подложки оксида магния MgO(001) и ортогонально пересекает горизонтальную ось кристаллографической анизотропии ультратонкого (2.2 нм) барьера диоксида рутения $$\text{RuO}_2$$. Это скрещивание сил вызывает локальное лавинообразное размножение волн магнитных спинов (ТГц-магнонов) атомов рутения. Рожденные магноны формируют мощную спин-расщепленную асимметрию проводимости, которая принудительно заставляет электроны когрентно туннелировать сквозь барьер строго в одном направлении — из нижнего платинового орбитального коллектора в верхние алюминиевые наноантенны, генерируя силовой постоянный ток.

Верхнее интерференционное зеркало Фабри — Перо возвращает 95% непреобразованных ИК-фотонов обратно вниз, замыкая рекуперационный контур тепла и полностью избавляя ячейку от необходимости использовать внешние водяные или воздушные радиаторы охлаждения.

## 📊 Математическое ядро симулятора
Вычислительный C#-компьютер решает нестационарное уравнение теплопроводности Фурье, сопряженное с нелинейными объемными членами излучения Стефана — Больцмана:

$$T_m^{k+1} = T_m^k + \frac{\Delta t}{c_m(T) \rho_m} \left[ \frac{\kappa_{m+1/2}(T) \cdot (T_{m+1}^k - T_m^k) - \kappa_{m-1/2}(T) \cdot (T_m^k - T_{m-1}^k)}{\Delta y^2} + q_{vol, m}^k \right]$$

Для предотвращения расхождения энергии на ультратонких гетерогенных границах сред (интерфейсах Pt → RuO₂ → Al) в разностную схему интегрирован строгий расчет **гармонического среднего** межслойной теплопроводности на гранях смежных узлов:

$$\kappa_{m+1/2}(T) = \frac{2 \kappa_m(T) \kappa_{m+1}(T)}{\kappa_m(T) + \kappa_{m+1}(T)}$$

Суммирование крошечной ЭДС туннельных нанопереходов (0.2 В) до индустриальных параметров силовой электроники (**20 Вольт и 3.3 Ампера / 66 Ватт**) обеспечивается топологическим лазерным разделением матрицы на N=100 продольных стрип-полос шириной 400 мкм, объединенных по принципу каскадной последовательной «змейки» (Z-коммутации).
<img width="3216" height="1640" alt="fig1" src="https://github.com/user-attachments/assets/a0072fa0-8494-4d62-a5f4-45ecfd9056f1" />


---


*   **Международный академический препринт (CERN / Zenodo):** [https://doi.org] https://doi.org/10.5281/zenodo.23270717 (https://zenodo.org/records/23270717) "Solid-State Magnonic Heat Recuperator Based on Altermagnetic Tunnel Junctions" 
*   **Автор и единственный владелец прав:** Зимницкий Дмитрий Валентинович.

---

## ✉️ Контакты и обратная связь (Correspondence)
Для коммерческих предложений, венчурных инвестиций, координации создания физического прототипа в условиях нанотехнологических чистых зон (ALD/DRIE литография) или академического цитирования, пожалуйста, связывайтесь с автором напрямую:

*   **Email:** [abeliar.maksvel@gmail.com](mailto:abeliar.maksvel@gmail.com)
